#!/usr/bin/env bash

# Constant Values
START_DATE="2017-01-01"
DATE_NOW=$(date +%Y-%m-%d)
KEYWORDS_FILE=$1
TWEET_LIMIT=10

TWARC_CONFIG="$HOME/.config/twarc/config"

gen_file_name() {
    local START=$1
    local END=$2

    printf "%s_%s_twitter_data.csv" "$START" "$END"
}

inc_date_by_X_year(){
    local DATE_STR=$1
    local NUM_YEARS=$2

    local NEW_DATE=$(date +%Y-%m-%d -d "$DATE_STR + $NUM_YEARS year")
    echo "$NEW_DATE"
}

gen_one_yr_inc(){
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

    echo "Current Dir: $PWD"

    if ! command -v twarc2 &>/dev/null; then

        echo "Twarc utility not installed..."
        echo "Install with 'pip install twarc'"
        exit 1
    fi

    if ! [[ -f "$TWARC_CONFIG" ]]; then
        echo "Don't forget to configure twitter keys/secrets with twarc"
        echo "https://twarc-project.readthedocs.io/en/latest/twarc2_en_us/#configure"
        exit 1
    fi

    gen_one_yr_inc 2022-01-01

    # use twarc to grab historical tweets from 01/2017 to now
    #twarc2 searches --archive --counts-only --granularity day --limit "$TWEET_LIMIT" --start-time "$START_DATE" --end-time "$END_DATE" "$KEYWORDS_FILE" "$(gen_file_name $START_DATE $DATE_NOW)"

}


main
