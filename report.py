from get_issues import get_issues
from get_github_action_results import get_ros_ci_results
import os
import pandas as pd
import argparse
import datetime
from pytz import timezone, utc
from tzlocal import get_localzone

def report(token, yaml_path):
    f = open('docs/report.md', 'w')
    f.write("# Reports  \n")
    ja = timezone('Asia/Tokyo')
    time = datetime.datetime(2017, 11, 12, 9, 55, 28, tzinfo=ja)
    f.write("last update " + str(time) + "  \n")
    f.write("## Support Status  \n")
    f.write(pd.DataFrame(get_ros_ci_results(token, yaml_path), columns=['package', 'foxy', 'dashing']).to_markdown(index = False))
    f.write("  \n   \n")
    f.write("## Issues/Pull Requests  \n")
    f.write(pd.DataFrame(get_issues(token, yaml_path), columns=['package','issue']).to_markdown(index = False))
    f.write("  \n   \n")
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scripts for getting issues')
    parser.add_argument('token', help='token of the github')
    parser.add_argument('yaml_path', help='path to the packages.yaml file')
    args = parser.parse_args()
    report(args.token, args.yaml_path)