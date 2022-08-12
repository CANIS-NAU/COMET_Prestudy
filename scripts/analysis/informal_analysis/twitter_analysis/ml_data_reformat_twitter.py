#!/usr/bin/env python3

import pandas as pd
import argparse
import sys
from pprint import pprint

# this is here just in case we need it
df_indices = [
    "id",
    "Advice",
    "Call to measure",
    "Community Engagement",
    "Comparison",
    "Complaint",
    "Configuration",
    "Cost Comparison",
    "Data Analysis",
    "Data Cap",
    "Data Processing",
    "Disconnection",
    "Explanation",
    "Gaming",
    "Hardware",
    "Inconsistency",
    "ISP",
    "News",
    "Not Related",
    "Outage",
    "Payment Issues",
    "Policy",
    "Promotion",
    "Security",
    "Seeking Feedback",
    "Seeking Recommendations",
    "Slow Internet",
    "Tech Support",
    "Test Results",
    "Tool",
    "Troubleshooting",
]

######## Supporting functions will be placed here ########
def reformat(data: pd.DataFrame):
    # Structure for new dataframe
    new_data = []
    # for each post
    for _ , row in data.iterrows():
        new_data.append(row[-5:].value_counts().rename(row['id']))

    new_data = pd.DataFrame(new_data).fillna(0).astype(int).sort_index(axis=1)
    return new_data

######## End of supporting functions ########

######## Actual script starts here ########
parser = argparse.ArgumentParser(description="Takes a CSV file with labelled posts, outputs newly formatted csv to stdout")
parser.add_argument("input_data", help="Data CSV that will be reformatted", type=str)
args = parser.parse_args()
input_file = args.input_data

# load the file with some slight pre-processing
csv_data = pd.read_csv(input_file).drop(columns=["QJ", "KC", "MV"])
# reformat the file
reformatted_data = reformat(csv_data)

# send new data to stdout for piping
reformatted_data.to_csv(sys.stdout)

exit(0)
