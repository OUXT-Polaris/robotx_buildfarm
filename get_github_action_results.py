import argparse
from github import Github
import yaml

def get_ros_package_issues(token, yaml_path):
    g = Github(token)
    data = []
    with open(yaml_path) as file:
        config = yaml.safe_load(file)
        for user in config["ros"]:
            for package in config["ros"][user]:
                url = "https://github.com/" + user + "/" + package + ".git"
                print("scanning -> " + url)
                repo = g.get_repo(user + "/" + package)
                open_issues = repo.get_issues(state='open')
                for issue in open_issues:
                    issue_url = "https://github.com/" + user + "/" + package + "/issues/" + str(issue.number)
                    issue_string = "[" + issue.title + "](" + issue_url + ")"
                    data.append([package, issue_string])
        for user in config["others"]:
            for package in config["others"][user]:
                url = "https://github.com/" + user + "/" + package + ".git"
                print("scanning -> " + url)
                repo = g.get_repo(user + "/" + package)
                open_issues = repo.get_issues(state='open')
                for issue in open_issues:
                    issue_url = "https://github.com/" + user + "/" + package + "/issues/" + str(issue.number)
                    issue_string = "[" + issue.title + "](" + issue_url + ")"
                    data.append([package, issue_string])
    return data

if __name__ == "__main__":
    pass