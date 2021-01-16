import argparse
from github import Github
import yaml
import git
import os
import shutil

def check_ros_packages(token, yaml_path):
    workflow_dict = {"foxy" : "ROS2-Foxy.yaml", "dashing" : "ROS2-Dashing.yaml"}
    g = Github(token)
    with open(yaml_path) as file:
        config = yaml.safe_load(file)
        for user in config["ros"]:
            for package in config["ros"][user]:
                url = "https://github.com/" + user + "/" + package + ".git"
                print("scanning -> " + url)
                support_platforms = []
                repo = g.get_repo(user + "/" + package)
                if config["ros"][user][package] is None:
                    support_platforms = list(workflow_dict.keys())
                elif "rosdistro" not in config["ros"][user][package]:
                    support_platforms = list(workflow_dict.keys())
                else:
                    support_platforms = config["ros"][user][package]["rosdistro"]
                for platfrom in support_platforms:
                    if str("workflow/" + platfrom) not in repo.get_branches():
                        check_ci_template(package, platfrom, repo)

def check_ci_template(package, rosdistro, repo):
    repo_path = os.path.join('./', 'ros_packages/' + package)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    git_repo = git.Repo.clone_from(repo.clone_url, repo_path, branch=repo.default_branch)
    branch = "workflow/" + rosdistro
    git_repo.git.branch(branch)
    git_repo.git.checkout(branch)
    workflow_dict = {"foxy" : "ROS2-Foxy.yaml", "dashing" : "ROS2-Dashing.yaml"}
    if rosdistro not in workflow_dict:
        raise Exception("rosdistro key is invalid")
    else:
        with open("./ci_templates/" + workflow_dict[rosdistro], mode='r') as f:
            workflow_string_valid = f.read()
        workflow_string_valid = workflow_string_valid.replace("${package_name}", package)
        modified_files = []
        if not os.path.exists(repo_path + "/dependency.repos"):
            shutil.copyfile("./ci_templates/dependency.repos", repo_path + "/dependency.repos")
            modified_files.append(repo_path + "/dependency.repos")
        if os.path.exists(repo_path + "/.github/workflows/" + workflow_dict[rosdistro]):
            with open(repo_path + "/.github/workflows/" + workflow_dict[rosdistro], mode='r+') as f:
                workflow_string = f.read()
                if workflow_string != workflow_string_valid:
                    f.write(workflow_string_valid)
                    modified_files.append(repo_path + "/.github/workflows/" + workflow_dict[rosdistro])
        else:
            with open(repo_path + "/.github/workflows/" + workflow_dict[rosdistro], mode='w') as f:
                f.write(workflow_string_valid)
                modified_files.append(repo_path + "/.github/workflows/" + workflow_dict[rosdistro])
        if len(modified_files) != 0:
            for modified_file in modified_files:
                modified_file = modified_file.replace("./ros_packages/"+package+"/","")
                git_repo.git.add(modified_file)
                git_repo.git.commit(modified_file, message='update ' + modified_file)
            git_repo.git.push('origin', branch)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    args = parser.parse_args()
    check_ros_packages(args.token, args.yaml_path)
