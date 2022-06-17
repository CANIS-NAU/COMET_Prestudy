#!/usr/bin/env bash

# global consts
TEMP_ID_FOLDER=${PWD}/.temp_conv_id_store
PER_CALL_LIMIT=10
TWEET_LIMIT=2

function create_temp_store {
    if [[ ! -d ${TEMP_ID_FOLDER} ]]; then
        mkdir -p ${TEMP_ID_FOLDER}
    fi
}

function delete_temp_store {
    if [[ -d ${TEMP_ID_FOLDER} ]]; then
        rm -rf ${TEMP_ID_FOLDER}
    fi
}

function usage {

    printf \
        "
TweetConversationScraper - Gather full conversation chain via extracted conversation_id

Usage:
$0  [ -h | --help ] [-i TWITTER_DATA_DIR]  [-o OUTPUT_DIR]

    Where:
        TWITTER_DATA_DIR is the directory where twitter csv files are located
        OUTPUT_DIR is where you wish to store the newly created conversation data."

    exit 0
}

# Handle command line arguments
while getopts ":i:o:" args; do
    case "${args}" in
    i)
        TWITTER_DATA_DIR=${OPTARG}
        if [[ ! -d ${TWITTER_DATA_DIR} ]]; then
            echo "[ERROR] Twitter CSV Data Not Found..."
            exit 1
        fi
        ;;
    o)
        OUTPUT_DIR=${OPTARG}
        if [[ ! -d $OUTPUT_DIR ]]; then
            mkdir -p ${OUTPUT_DIR}
        fi
        ;;
    *)
        usage
        ;;
    esac
done

shift $((OPTIND - 1))

if [[ -z "${TWITTER_DATA_DIR}" ]] || [[ -z "${OUTPUT_DIR}" ]]; then
    usage
fi

declare CONV_ID_ITER

# for each csv file in the input directory
for data_file in ${TWITTER_DATA_DIR}/*.csv; do

    # Identify the conversation_id column
    CONV_ID_ITER=$(awk -F "\"*,\"*" '{if (NR!=1) {print $2}}' ${data_file})

    # create temporary storage area to hold identified conversation_ids
    create_temp_store

    # generate new txt-based filename for the new output file
    new_filename="$(basename "${data_file/.csv/.txt}")"

    for element in ${CONV_ID_ITER}; do
        # Write respective conversation IDs to file
        echo "${element}" >>${TEMP_ID_FOLDER}/${new_filename}
    done

    # Now with all the conversation IDs extracted, enter them into twarc

    # TODO execute twarc search for the conversation_id and store the resulting conversation data in output directory
    twarc2 conversations --archive --limit ${TWEET_LIMIT} --max-results=${PER_CALL_LIMIT} ${TEMP_ID_FOLDER}/${new_filename} ${OUTPUT_DIR}/${new_filename/.txt/.json}
done

# convert all json files to csv and delete remaining json
for file in ${OUTPUT_DIR}/*.json; do
    fn=$(basename ${file})
    twarc2 csv ${file} "$OUTPUT_DIR/${fn/json/csv}"
done

# remove the unwanted JSON files
#echo "[INFO] Removing JSON files"
#rm ${OUTPUT_DIR}/*.json

# Delete temporary storage file
#delete_temp_store
