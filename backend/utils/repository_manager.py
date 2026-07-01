import os
import shutil
import subprocess

REPO_DIR = "repositories"


def clone_repository(repo_url: str):

    os.makedirs(REPO_DIR, exist_ok=True)

    repo_name = repo_url.split("/")[-1]

    repo_name = repo_name.replace(".git", "")

    repo_path = os.path.join(
        REPO_DIR,
        repo_name
    )

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    subprocess.run(
        [
            "git",
            "clone",
            repo_url,
            repo_path
        ],
        check=True
    )

    return repo_path