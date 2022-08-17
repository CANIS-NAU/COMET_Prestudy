#!/usr/bin/env python3

import pandas as pd
import argparse
import sys

# this list is here just in case we need it
df_indices = [
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

df_indices = [x.lower() for x in df_indices]

######## Supporting functions will be placed here ########
def reformat(data: pd.DataFrame):
    new_data = []

    for _ , row in data.iterrows():
        val_counts = row[-5:].value_counts()
        text = pd.Series([row["text"]], index=['text'])
        new_data.append(pd.concat([text, val_counts]))

    new_data = pd.DataFrame(new_data, index=data['id']).fillna(0)
    new_data.loc[:, 'not related':] = new_data.loc[:, 'not related':].astype(int)
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
