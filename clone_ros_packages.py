import argparse
from github import Github
import yaml
import git
import os

def clone_ros_packages(token, yaml_path):
    g = Github(token)
    with open(yaml_path) as file:
        config = yaml.safe_load(file)
        for user in config["ros"]:
            for package in config["ros"][user]:
                repo_path = os.path.join('./', 'ros_packages/' + package)
                url = "https://github.com/" + user + "/" + package + ".git"
                print("scanning -> " + url)
                repo = g.get_repo(user + "/" + package)
                git_repo = git.Repo.clone_from(repo.clone_url, repo_path, branch=repo.default_branch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    args = parser.parse_args()
    clone_ros_packages(args.token, args.yaml_path)
