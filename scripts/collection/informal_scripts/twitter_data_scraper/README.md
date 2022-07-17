# Twitter data scraping workflow summary
For the sake of this part of the project, all operations will be
conducted using the `twarc` utility. This is a command line tool
built by Twitter to interact with their API with only a few commands.

The version of twarc we will be using is V2, the latest version as of 
writing this. 

## 1. Collecting the data
There are some utility scripts already located in this directory (See: `TweetArchiveScrape.sh`). However, in the end,
the operation essentially boils down to automating the command:

`twarc2 searches \
            --combine-queries \ # Optimize search queries to use less requests
            --archive \ # utilize the research track to access all historical tweets
            --granularity day \ # data will be distinguished by days
            --limit "$TWEET_LIMIT" \ # hard limit of max tweets collected for one run (eg. 2mil)
            --start-time "$START_DATE" \ # earliest historical date to search from
            --end-time "$END_DATE" \ # most recent date to end search (ie. now)
            "$KEYWORDS_FILE" \ # line-separated file of keywords/queries that will be used for filtering
            "$(gen_file_name "$START_DATE" "$END_DATE")"` # resulting output file name

Where: 

- `$TWEET_LIMIT` is the hard limit for maximum tweets that are allowed to be collected. I chose to divide
this value up based on the number of years that will be collected. Eg. collecting posts
from 2017 to 2022, that's a five year difference. Tweet quota will be calculated:
`quota = 10,000,000 "Academic Quota" // (2022 - 2017)`

- `$START_DATE` is the earliest date you wish to capture (ie. 2017)

- `$END_DATE` is the most recent date you wish to capture (ie. now)

- `$KEYWORDS_FILE` is the line-separated list of keywords that will be passed into the program (.txt is fine)

- `gen_file_name` is a helper function written to automatically create a name for the resulting output file.



