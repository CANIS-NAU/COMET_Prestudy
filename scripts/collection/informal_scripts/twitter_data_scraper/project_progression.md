# Project progression plan - Twitter Scraper

## Step-by-step

0. Overhaul existing list of keywords to follow Twitter query syntax.
    - By doing this, we should be able to make each request more efficient by
    narrowing the search parameters and getting more relevent tweets.

1. Gather all tweets that are within the age-range of "2017-01-01" up to now
    - To keep things organized, the data will be divided into 1 year increments, 
    each increment getting its own dedicated file.
 

2. Implement cron job to automatically ping for more tweets after X seconds/minutes/hours
    2.1 There is also the possibility to use Twarc's 'Stream' capability. We can stream 
    new tweets for a specified time interval, then sleep for another time interval. 
    The cycle can continue.

3. Convert the generated JSON file to a properly formatted CSV (tab-separated)
    - for each increment data file, collect the data we want from the JSON, and 
    organize it into a CSV (tab-separated) file for actual analysis.

    - twarc has 'twarc-csv' command for conversions like this

4. Using a secondary script, extract the conversation ids from the original posts to reconstruct the whole conversation
