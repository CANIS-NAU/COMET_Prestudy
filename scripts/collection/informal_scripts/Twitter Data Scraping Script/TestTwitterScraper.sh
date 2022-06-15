#!/usr/bin/env bash

# Constant Values
START_DATE="2017-01-01" # date format: YYYY-mm-dd
DATE_NOW=$(date +%Y-%m-%d)
KEYWORDS_FILE=$1
TWEET_LIMIT=10

TWARC_CONFIG="$HOME/.config/twarc/config"

function gen_file_name {
    local START=$1
    local END=$2

    printf "%s_%s_twitter_data.csv" "$START" "$END"
}

function help_output {
    printf "\nTwitter Scraper - Scrapes tweets from $START_DATE to Now. Start date can be changed.\n\nUsage:\n\ntwitterscraper.sh [ --help | -h ] {KEYWORD_FILE_DIR}"

}

function inc_date_by_X_year {
    local DATE_STR=$1
    local NUM_YEARS=$2

    local NEW_DATE=$(date +%Y-%m-%d -d "$DATE_STR + $NUM_YEARS year")
    echo "$NEW_DATE"
}

function gen_one_yr_inc {
    local DATE_STR=$(date +%Y-%m-%d -d "$1")
    local INC=$(inc_date_by_X_year "$DATE_STR" 1)
    

    if [ "$(date +%s -d $INC)" -ge "$(date +%s -d $DATE_NOW)" ]
    then 
        echo "$DATE_NOW"

    else
        echo "$INC"
    fi
}

main() {

    if [ "$KEYWORDS_FILE" = "--help" ] || [ "$KEYWORDS_FILE" = "-h" ]; then
        help_output
        exit 1
    fi



    if ! command -v twarc2 &>/dev/null; then

        echo "Twarc utility not installed..."
        echo "Install with 'pip install twarc'"
        exit 1
    fi

    if ! [[ -f "$TWARC_CONFIG" ]]; then
        echo "Don't forget to configure twitter keys/secrets with **twarc2**"
        echo "https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/#configure"
        exit 1
    fi



    # Now we can get into the program iteration
    local END_DATE=$(gen_one_yr_inc $START_DATE)

    while [ "$(date +%s -d "$END_DATE")" -lt "$(date +%s -d "$DATE_NOW")" ]; do

        # use twarc to grab historical tweets from 01/2017 to now
        # TODO - Determine optimal settings for twarc
        echo "twarc2 searches --archive --counts-only --granularity day --limit $TWEET_LIMIT --start-time $START_DATE --end-time $END_DATE $KEYWORDS_FILE $(gen_file_name $START_DATE $END_DATE)"
        twarc2 searches --combine-queries --archive --granularity day --limit "$TWEET_LIMIT" --start-time "$START_DATE" --end-time "$END_DATE" "$KEYWORDS_FILE" "$(gen_file_name $START_DATE $END_DATE)"
        START_DATE=$(gen_one_yr_inc $START_DATE)
        END_DATE=$(gen_one_yr_inc $END_DATE)

    done

    exit 0
}


main
