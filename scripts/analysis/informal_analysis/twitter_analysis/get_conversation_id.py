#!/usr/bin/env python3

import argparse
import pathlib
import sys
import pandas as pd


def extract_conv_id(file: pathlib.Path):
    conv_ids = pd.read_csv(file.resolve(), low_memory=False)["conversation_id"]
    conv_ids.to_string(sys.stdout, index=False, header=False)


parser = argparse.ArgumentParser(
    description="Extracts conversation ids from single twitter csv file. Outputs to stdout for piping."
)
parser.add_argument("twitter_csv", help="twitter csv file to process")
args = parser.parse_args()
path = pathlib.Path(args.twitter_csv)

if path.is_file():
    extract_conv_id(path)
else:
    sys.stderr.write("[ERROR] File not found...\n")
