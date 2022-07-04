#!/usr/bin/env bash

function get_conversation_ids {
    # has to be csv file for now
    local filename=$1

    conversation_ids=$(awk -F "\"*,\"*" '{if (NR!=1) {print$2}}' ${filename})
    
    for item in ${conversation_ids}; do
        echo ${item} >> ${PWD}/test_conversations_$(basename "${filename/.*/}").txt
    done
}

get_conversation_ids $1
