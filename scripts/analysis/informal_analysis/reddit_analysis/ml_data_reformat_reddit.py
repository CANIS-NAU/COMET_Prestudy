#!/usr/bin/env python3

import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("input_data", help="Data CSV that will be reformatted", type=str)
args = parser.parse_args()
input_file = args.input_data

# load the file

# reformat the file

# send new data to stdout for piping


######## Supporting functions will be placed at the end ########
def reformat(data):
    raise NotImplementedError


