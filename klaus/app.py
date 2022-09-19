import configparser
import waitress
import klaus
import os

repositories = ["/srv/git/git-scripts.git", "/srv/git/anExampleRepo%21.git"]


if __name__ == "__main__":
    app = klaus.make_app(repositories, "Eden's git server - Repositories")
    waitress.serve(app, host = "0.0.0.0", port = 80, threads = int(os.environ["APP_THREADS"]))

