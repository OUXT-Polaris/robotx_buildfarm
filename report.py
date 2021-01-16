from get_issues import get_issues
import os
import pandas as pd
import argparse
import datetime

def report(token, yaml_path):
    f = open('docs/report.md', 'w')
    f.write("# Reports  \n")
    f.write("last update " + str(datetime.datetime(2017, 11, 12, 9, 55, 28)) + "  \n")
    f.write("## Issues/Pull Requests  \n")
    f.write(pd.DataFrame(get_issues(token, yaml_path), columns=['package','issue']).to_markdown())
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    args = parser.parse_args()
    report(args.token, args.yaml_path)