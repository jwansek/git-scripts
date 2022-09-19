import configparser
import waitress
import klaus
import os

def get_repo_paths(metadata_path):
    repo_paths = []
    for filename in os.listdir(metadata_path):
        if filename.endswith(".git.conf"):
            meta = configparser.ConfigParser()
            meta.read(os.path.join(metadata_path, filename))
            repo_name = filename[:-5]

            if meta.getboolean(repo_name, "visible"):
                repo_paths.append(meta.get(repo_name, "path"))

    return repo_paths

if __name__ == "__main__":
    repositories = get_repo_paths("/srv/repos")
    print("Using repository paths: %s" % " ".join(repositories))
    app = klaus.make_app(repositories, "Eden's git server - Repositories")
    waitress.serve(app, host = "0.0.0.0", port = 80, threads = int(os.environ["APP_THREADS"]))

