#!/usr/bin/env fish

set -l usage "Usage:
get_conversations [ -h | --help ] [ -o OUTPUT_DIR ] [ CONVERSATION_ID_FILES... ]"

argparse -i 'h/help' 'o='  -- $argv

if set -q _flag_h; or set -q _flag_help
    echo $usage
    return 1
end

if not set -q _flag_o; or test -z $argv
    echo -e "
    [ERROR] Invalid Input Parameters...
    "
    echo $usage
    return 1
end

for directory in $argv
    if test -e $directory
        twarc2 conversations --archive --conversation-limit 5 $directory $_flag_o/(string replace .txt .jsonl (basename $directory))
    else
        echo "Not valid conversation_id file. Skipping..."
    end
end


