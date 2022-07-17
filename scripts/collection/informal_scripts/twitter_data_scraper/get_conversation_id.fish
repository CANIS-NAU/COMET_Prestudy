#!/usr/bin/env fish

set -l usage "Usage:

    get_conversation_id [ -h | --help ] [ -f | --file TWITTER_CSV_FILE ]"

argparse -i 'h/help' 'f=' -- $argv

if set -q _flag_h; or set -q _flag_help
    echo $usage
    return 1
end

if not set -q _flag_f
    echo "Missing Input File...
    "
    echo $usage
    return 1
end

awk -F "\"*,\"*" '{if (NR!=1) {print $2}}' $_flag_f
