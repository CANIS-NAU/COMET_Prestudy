#!/usr/bin/env python3

import pandas as pd
from pprint import pprint
import pathlib
import argparse
import sys

parser = argparse.ArgumentParser(
    description="Script that takes N number of twitter csv files, and counts number of unique users involved in each file. Prints csv-formatted output to stdout for piping."
)
parser.add_argument("twitter_csv", nargs="+", help="twitter csv file(s) for processing")
args = parser.parse_args()
dirs = [pathlib.Path(path) for path in args.twitter_csv]

author_ids = {}

for dir in dirs:
    if dir.is_file():
        data = pd.read_csv(dir.resolve(), low_memory=False).to_dict()
        # use set to remove duplicate user ids
        author_ids.update({f"{dir.name}": len(set(dict(data["author_id"]).values()))})

    else:
        sys.stderr.write(f"[WARNING] File: '{dir.resolve()}' not found, skipping...")

pd.DataFrame({"file_name": author_ids.keys(), "num_users": author_ids.values()}).to_csv(
    sys.stdout
)
