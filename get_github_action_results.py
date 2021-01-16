import argparse
from github import Github
import yaml

def get_ros_ci_results(token, yaml_path, distribution):
    g = Github(token)
    data = []
    workflow_dict = {"foxy" : "ROS2-Foxy.yaml", "dashing" : "ROS2-Dashing.yaml"}
    if distribution not in workflow_dict:
        raise Exception("distribution " + distribution + " does not exist")
    with open(yaml_path) as file:
        config = yaml.safe_load(file)
        for user in config["ros"]:
            for package in config["ros"][user]:
                url = "https://github.com/" + user + "/" + package + ".git"
                print("scanning -> " + url)
                repo = g.get_repo(user + "/" + package)
                try:
                    print(repo.get_workflow(workflow_dict[distribution]))
                except:
                    pass
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    parser.add_argument('distribution', help='ROS2 distribution')
    args = parser.parse_args()
    data = get_ros_ci_results(args.token, args.yaml_path, args.distribution)
    print(data)