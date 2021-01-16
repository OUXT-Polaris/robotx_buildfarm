import argparse
from github import Github
import yaml
import markdown
#import pandas as pd

def get_issue(token, yaml_path):
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
    return data
    #with open("issues.md", mode='w') as f:
        #df = pd.DataFrame(data, columns=['package','issue'])
        #f.write(df.to_markdown())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    args = parser.parse_args()
    get_issue(args.token, args.yaml_path)