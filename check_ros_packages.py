import argparse
from github import Github
import yaml
import git
import os
import shutil

def check_ros_packages(token, yaml_path):
    g = Github(token)
    workflow_dict = {"foxy" : "ROS2-Foxy.yaml", "dashing" : "ROS2-Dashing.yaml"}
    with open(yaml_path) as file:
        config = yaml.safe_load(file)
        for user in config["ros"]:
            for package in config["ros"][user]:
                repo_path = os.path.join('./', 'ros_packages/' + package)
                shutil.rmtree(repo_path)
                url = "https://github.com/" + user + "/" + package + ".git"
                print("scanning -> " + url)
                repo = g.get_repo(user + "/" + package)
                git_repo = git.Repo.clone_from(repo.clone_url, repo_path, branch=repo.default_branch)
                support_platforms = []
                if config["ros"][user][package] is None:
                    support_platforms = list(workflow_dict.keys())
                elif "rosdistro" not in config["ros"][user][package]:
                    support_platforms = list(workflow_dict.keys())
                else:
                    support_platforms = config["ros"][user][package]["rosdistro"]
                for platfrom in support_platforms:
                    check_ci_template(package, repo, repo_path, platfrom)

def check_ci_template(package, repo, repo_path, rosdistro):
    workflow_dict = {"foxy" : "ROS2-Foxy.yaml", "dashing" : "ROS2-Dashing.yaml"}
    if rosdistro not in workflow_dict:
        raise Exception("rosdistro key is invalid")
    else:
        f = open("./ci_templates/" + workflow_dict[rosdistro], 'r')
        workflow_string = f.read()
        f.close()
        workflow_string = data.replace("${package_name}", package)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    args = parser.parse_args()
    check_ros_packages(args.token, args.yaml_path)
