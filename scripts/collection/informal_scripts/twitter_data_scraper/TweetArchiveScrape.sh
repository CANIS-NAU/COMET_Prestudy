#!/usr/bin/env bash

# ------------------------------------------------------------------
# [Quinton Jasper] TweetArchiveScrape.sh

#      This script will handle the scraping and organizing of
#      Twitter data from the time period: START_DATE to DATE_NOW
#      (ie. the current date upon script execution).
#
#      Each year increment will get its own dedicated CSV file,
#      This will keep individual file-sizes from getting too large.
#      
#      This script will also prevent complete quota usage before
#      all queries are sent. The academic research track of the
#      Twitter API v2.0 allows for 10,000,000 tweets to be grabbed
#      per month. 
#
#      This script will do the math to calculate how
#      many tweets can be gathered for each year increment before
#      hitting the tweet quota. 

#      *** This script will utilize the 10,000,000 tweet quota in a single run.***
#      *** Use wisely. ***
# ------------------------------------------------------------------

######## Constant Values ########
START_DATE="2017-01-01" # date format: YYYY-mm-dd
DATE_NOW=$(date +%Y-%m-%d)

KEYWORDS_FILE=$1

TOTAL_TWEET_QUOTA=10000000

# Divide monthly quota amongst num years to scrape
# ie. (DATE_NOW - START_DATE) / 10,000,000 (Academic Quota)
YEAR_DIFF=$(expr $(date +%Y -d ${DATE_NOW}) - $(date +%Y -d ${START_DATE}))
TWEET_LIMIT=$(expr ${TOTAL_TWEET_QUOTA} / ${YEAR_DIFF})


FILENAME_SUFFIX="twitter_data"
JSON_DIR=$PWD/json_data
CSV_DIR=$PWD/converted_csv

TWARC_CONFIG="$HOME/.config/twarc/config"

######## Functions ########
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

######## Entrypoint ########
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
        twarc2 searches \
            --combine-queries \
            --archive \
            --granularity day \
            --limit "$TWEET_LIMIT" \
            --start-time "$START_DATE" \
            --end-time "$END_DATE" \
            "$KEYWORDS_FILE" \
            "$(gen_file_name "$START_DATE" "$END_DATE")"

        # increment start and end date by one year, or until end date == now
        START_DATE=$(gen_one_yr_inc "$START_DATE")
        END_DATE=$(gen_one_yr_inc "$END_DATE")

    done

    # When all is done, convert all json files to csv in their own folder
    json_to_csv

    exit 0
}

main
