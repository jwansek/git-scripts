#!/usr/bin/env python3

import subprocess
import configparser
import datetime
import tempfile
import urllib
import shutil
import jinja2
import os

class ChangeCWD:
    def __init__(self, new_cwd):
        self.new_cwd = new_cwd
        self.old_cwd = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_cwd)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_cwd)

conf_path = os.path.join(os.path.dirname(__file__), "gitscripts.conf")
if not os.path.exists(conf_path):
    conf_path = os.path.join(os.path.dirname(os.readlink(__file__)), "gitscripts.conf")

CONFIG = configparser.ConfigParser()
CONFIG.read(conf_path)

repo_name = urllib.parse.quote_plus(input("Input repository name: "))
if not repo_name.endswith(".git"):
    repo_name += ".git"
repo_dir = os.path.join(CONFIG.get("git", "repo_path"), repo_name)
repo_url = "git@%s:%s" % (CONFIG.get("git", "domain"), repo_name)

if os.path.exists(repo_dir):
    print("ERROR: A repository with that name already exists. Please try another")
    exit()
os.mkdir(repo_dir)

subprocess.run(["ln", "-s", repo_dir, repo_name[:-4]])
subprocess.run(["ln", "-s", repo_dir, repo_name])

private = input("Would you like the repository to appear on the web version %s? <y/n>: " % CONFIG.get("git", "domain")).lower() == "n"

with ChangeCWD(repo_dir):
    subprocess.run(["git", "init", "--bare"])

    description = input("Input repository description: ")
    author = input("Input repository author: ")
    author_email = input("Input author email: ")
    
    with open(os.path.join(repo_dir, "description"), "w") as f:
        f.write(description)
   
    with open(os.path.join(repo_dir, "author"), "w") as f:
        f.write(author)

    with open(os.path.join(repo_dir, "url"), "w") as f:
        f.write(repo_url)

    with open(os.path.join(repo_dir, "config"), "a") as f:
        f.write("[gitweb]\n\towner = %s <%s>" % (author, author_email))

subprocess.run(["ln", "-s", os.path.join(os.path.dirname(conf_path), "post-receive-hook.sh"), os.path.join(repo_dir, "hooks", "post-receive")])

if input("Would you like the repository to remain bare? Useful for making mirrors of Github repos. <y/n>: ").lower() != "y": 
    with tempfile.TemporaryDirectory() as tempdir:
        subprocess.run(["git", "clone", repo_url, tempdir])
        with ChangeCWD(tempdir):
            
            with open("README.md", "w") as f:
                f.write("# %s\n\n%s\n" % (repo_name, description))

            gitignore_templates_dir = CONFIG.get("git", "gitignore_templates")
            templates = sorted([f[:-10] for f in os.listdir(gitignore_templates_dir) if f.endswith(".gitignore")])
            templates.insert(0, "[None]")
            for i, template in enumerate(templates, 1):
                print("%3d: %-23s" % (i, template), end = "")
                if i % 3 == 0:
                    print("")

            selected_index = int(input("\nSelect .gitignore template: "))
            if selected_index != 0:
                shutil.copy(os.path.join(gitignore_templates_dir, templates[selected_index - 1]) + ".gitignore", ".gitignore", follow_symlinks = True)

            licenses_templates_dir =  CONFIG.get("git", "license_templates")
            templates = sorted([f[:-4] for f in os.listdir(licenses_templates_dir) if not f.endswith("-header.txt")])
            templates.insert(0, "[None]")
            for i, template in enumerate(templates, 1):
                print("%2d: %-22s" % (i, template), end = "")
                if i % 4 == 0:
                    print("")
            
            selected_index = int(input("\nSelect license template: "))
            if selected_index != 0:
                with open(os.path.join(licenses_templates_dir, templates[selected_index - 1]) + ".txt", "r") as f:
                    jinja_template = jinja2.Template(f.read())

                with open("LICENSE", "w") as f:
                    f.write(jinja_template.render(**{
                        "year": str(datetime.datetime.today().year),
                        "organization": author,
                        "project": repo_name
                    }))

            subprocess.run(["git", "add", "-A"])
            subprocess.run(["git", "commit", "-m", "Initialized repository"])
            subprocess.run(["git", "push", "origin", "master"])

print("""
Repository created. You can now clone or add remote:
    git remote add other %s
    git clone %s
And add github mirror (insecure method, keys are stored locally):
    git remote add github https://%s:%s@github.com/%s/%s
Add a github mirror (secure method using SSH):
    git remote add github git@github.com:%s/%s
To add a `git pushall` alias to push to all remotes:
    git config --global alias.pushall '!git remote | xargs -L1 git push --all'
    """ % (
        repo_url, repo_url, CONFIG.get("github", "user"), CONFIG.get("github", "key"), 
        CONFIG.get("github", "user"), repo_name, CONFIG.get("github", "user"), repo_name
    ))





