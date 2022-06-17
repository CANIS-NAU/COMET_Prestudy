#!/usr/bin/env bash

function usage {

    printf \
"TweetConversationScraper - Gather full conversation chain via extracted conversation_id

Usage:
$0  [ -h | --help ] [-i TWITTER_DATA_DIR]  [-o OUTPUT_DATA_DIR]

    Where:
      TWITTER_DATA_DIR is the directory where twitter csv files are located
      OUTPUT_DATA_DIR is where you wish to store the newly created conversation data."

    exit 0
}

# function to check that twarc is installed/accessible


main() {
    # Handle command line arguments
    while getopts ":i:o:" args; do
        case "${args}" in
            i)
                TWITTER_DATA_DIR=${OPTARG}
                if [[ ! -d $TWITTER_DATA_DIR ]]; then
                    mkdir -p ${TWITTER_DATA_DIR}
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

    shift $((OPTIND-1))

    if [[ -z "${i}" ]] || [[ -z "${o}" ]]; then
        usage
    fi


    # for each csv file in the input directory
    for data_file in ${TWITTER_DATA_DIR}/*.csv; do

        # for each conversation_id from chosen csv file
        for line in $(awk -F "\"*,\"*" '{print $2}' ${data_file}); do
            echo ${line}

            # identify the conversation_id column ()
            # execute twarc search for the conversation_id
            # store the resulting conversation data in output directory
        done
    done
}

# Execute main function
main "$@"
