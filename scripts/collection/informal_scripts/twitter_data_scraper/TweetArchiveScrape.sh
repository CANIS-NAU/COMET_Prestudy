#!/usr/bin/env bash

# Constant Values
START_DATE="2017-01-01" # date format: YYYY-mm-dd
DATE_NOW=$(date +%Y-%m-%d)
KEYWORDS_FILE=$1
PER_CALL_LIMIT=10
TWEET_LIMIT=2


FILENAME_SUFFIX="twitter_data"
JSON_DIR=$PWD/json_data
CSV_DIR=$PWD/converted_csv

TWARC_CONFIG="$HOME/.config/twarc/config"

function json_to_csv {
    for file in "$JSON_DIR"/*.json; do
        filename="$(basename "$file")"
        twarc2 csv "$file" "$CSV_DIR/${filename/json/csv}"
    done
}

function gen_file_name {
    local START=$1
    local END=$2

    local FILENAME_FORMAT="$JSON_DIR"/"$START"_"$END"_"$FILENAME_SUFFIX".json

    echo "$FILENAME_FORMAT"
}

function help_output {
    printf \
        "\nTwitter Scraper - Scrapes tweets from %s to Now. Start date can be changed.\n\nUsage:\n\ntwitterscraper.sh [ --help | -h ] {KEYWORD_FILE_DIR}" "$START_DATE"

}

function inc_date_by_X_year {
    local DATE_STR=$1
    local NUM_YEARS=$2

    local NEW_DATE
    NEW_DATE=$(date +%Y-%m-%d -d "$DATE_STR + $NUM_YEARS year")
    echo "$NEW_DATE"
}

function gen_one_yr_inc {
    local DATE_STR
    DATE_STR=$(date +%Y-%m-%d -d "$1")
    local INC
    INC=$(inc_date_by_X_year "$DATE_STR" 1)

    local NEW_DATE

    if [ "$(date +%s -d "$INC")" -ge "$(date +%s -d "$DATE_NOW")" ]; then
        NEW_DATE="$DATE_NOW"

    else
        NEW_DATE="$INC"
    fi

    echo "$NEW_DATE"
}

main() {

    if [[ "$KEYWORDS_FILE" == "--help" ]] || [[ "$KEYWORDS_FILE" == "-h" ]]; then
        help_output
        exit 1

    elif [[ "$KEYWORDS_FILE" == "" ]]; then
        echo "[ERROR] Keywords File not specified, try again..."
        exit 1
    fi

    if ! command -v twarc2 &>/dev/null; then

        echo "[ERROR] Twarc utility not installed..."
        echo "Install with 'pip install twarc && pip install twarc-csv"
        exit 1
    fi

    if ! [[ -f "$TWARC_CONFIG" ]]; then
        echo "[ERROR] Don't forget to configure twitter keys/secrets with **twarc2**"
        echo "https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/#configure"
        exit 1
    fi

    # Now we can get into the program iteration

    # create the directory for storing csv files, if not already made
    if [ ! -d "$CSV_DIR" ]; then
        mkdir "$CSV_DIR"
    fi

    # create the directory for storing json files, if not already made
    if [[ ! -d "$JSON_DIR" ]]; then
        mkdir "$JSON_DIR"
    fi

    local END_DATE
    END_DATE=$(gen_one_yr_inc $START_DATE)

    while [ "$(date +%s -d "$END_DATE")" -le "$(date +%s -d "$DATE_NOW")" ]; do

        if [[ $START_DATE == "$END_DATE" ]]; then
            break
        fi

        # use twarc to grab historical tweets from 01/2017 to now
        # TODO - Determine optimal settings for twarc
        twarc2 searches \
            --combine-queries \
            --archive \
            --granularity day \
            --max-results $PER_CALL_LIMIT \
            --limit "$TWEET_LIMIT" \
            --start-time "$START_DATE" \
            --end-time "$END_DATE" \
            "$KEYWORDS_FILE" \
            "$(gen_file_name "$START_DATE" "$END_DATE")"

        START_DATE=$(gen_one_yr_inc "$START_DATE")
        END_DATE=$(gen_one_yr_inc "$END_DATE")

    done

    json_to_csv

    exit 0
}

main
