#!/usr/bin/env python3

from datetime import datetime, timedelta

import pandas as pd
from dateutil import parser
from os import path
from searchtweets import collect_results, gen_request_parameters, load_credentials

from BaseScraper import Scraper

# Glob Constants
# TODO - Finalize file naming convention
FILENAME_CONVENTION = (
    "{}_{}_twitter_scrape_data.csv"  # {date-start}_{date-end}_twitter_scrape_data.csv
)
ATTRIB_STR = "id,text,attachments,author_id,conversation_id,created_at,in_reply_to_user_id,lang,public_metrics,referenced_tweets"
EXPANSIONS = "author_id,in_reply_to_user_id,attachments.media_keys"
USER_FIELDS = "id,name,username"
MEDIA_FIELDS = "media_key,type,url,variants"

MAX_PER_CALL = 5
MAX_TWEETS = 5


def daterange(start_date: datetime, end_date: datetime) -> tuple[datetime, datetime]:
    """Take a date range from start to finish, then generate an iterable that
    increments over those date ranges at 1 year intervals

    Parameters
    ----------
    start_date : datetime
        the earliest date in the range
    end_date : datetime
        the most recent date in the range (usually "now")

    Yields
    ------
    Iterator[tuple[datetime, datetime]]
        generated start/end dates exactly 1 year apart. If the time difference is
        less than 1 year between the start date and end date, the specified end date
        will be used. 

        ex.
            ``start = datetime(2020, 1, 1)
            end = datetime(2022, 2, 22)

            for item in daterange(start, end):
                print(item)``

            result:

                ``(datetime.datetime(2020, 1, 1, 0, 0), datetime.datetime(2020, 12, 31, 0, 0))``
                ``(datetime.datetime(2020, 12, 31, 0, 0), datetime.datetime(2021, 12, 31, 0, 0))``
                ``(datetime.datetime(2021, 12, 31, 0, 0), datetime.datetime(2022, 2, 22, 0, 0))``

    """
    while start_date <= end_date:
        new_start_end_tuple = (
            start_date,
            start_date
            + (
                timedelta(365)
                if (end_date - start_date) > timedelta(365)
                else (end_date - start_date)
            ),
        )
        yield new_start_end_tuple
        start_date = start_date + timedelta(365)


class TwitterScraper(Scraper):
    def __init__(
        self,
        keywords_file: str | None,
        credentials_file: str,
        age_threshold: str | None,
        output_dir: str,
    ) -> None:

        super().__init__(keywords_file, age_threshold)
        self.credentials = load_credentials(
            filename=credentials_file, yaml_key="search_tweets_v2", env_overwrite=False
        )
        self.output_dir = output_dir

    def format_collected_data(self, data):
        """Formats the raw twitter data into desired datapoints that we can understand and parse

        Thx Kylie :)

        Parameters
        ----------
        data : dict
            The JSON object returned from the collect_results function.
        """

        def get_tweet_data(tweet):

            id = tweet["id"] if "id" in tweet else None
            text = tweet["text"] if "text" in tweet else None
            attachments = None  # if there are attachments find them and place them here or none
            
            # if there are attachments in the tweet
            if "attachments" in tweet:
                # get the media keys
                media_keys = tweet["attachments"]["media_keys"]
                # match the media keys with the correct media data
                for media_key in media_keys:
                    attachments = []
                    # loop through media variable to match the media_key
                    for item in media:
                        if item["media_key"] == media_key:
                            if item["type"] == "video":
                                data = {
                                    "media_key": media_key,
                                    "type": "video",
                                    "url": item["variants"][0]["url"],
                                }
                                attachments.append(data)
                            else:
                                attachments.append(item)
                            break

            author_id = tweet["author_id"] if "author_id" in tweet else None
            author_name = None  # compare author_id with ids in users for name
            author_username = None  # compare author_id with ids in users for username

            if author_id != None:
                for user in users:
                    if user["id"] == author_id:
                        author_name = user["name"]
                        author_username = user["username"]

            conversation_id = (
                tweet["conversation_id"] if "conversation_id" in tweet else None
            )
            created_at = tweet["created_at"] if "created_at" in tweet else None
            in_reply_to_user_id = (
                tweet["in_reply_to_user_id"] if "in_reply_to_user_id" in tweet else None
            )
            lang = tweet["lang"] if "lang" in tweet else None
            public_metrics = (
                tweet["public_metrics"] if "public_metrics" in tweet else None
            )
            referenced_tweets = (
                tweet["referenced_tweets"] if "referenced_tweets" in tweet else None
            )

            datetime_created_at = parser.parse(created_at)
            formatted_data = {
                "id": id,
                "text": text,
                "attachments": attachments,
                "author_id": author_id,
                "author_name": author_name,
                "author_username": author_username,
                "conversation_id": conversation_id,
                "created_at_ymd": datetime_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "created_at_epoch": datetime_created_at.timestamp(),
                "in_reply_to_user_id": in_reply_to_user_id,
                "lang": lang,
                "public_metrics": public_metrics,
                "referenced_tweets": referenced_tweets,
                "responses": self.search(conversation_id, None, None) # TODO - Ask Kylie about how to implement this here.
            }

            yield formatted_data

        if data:
            tweets = data[0]["data"] if "data" in data[0] else None
            media = data[0]["includes"]["media"] if "media" in data[0]["includes"] else None
            users = data[0]["includes"]["users"] if "users" in data[0]["includes"] else None

            return list(get_tweet_data(tweets))

    def search(self, keyword, start_time: datetime, end_time: datetime):
        """Gather data between provided date ranges using Twitter API function
        gen_request_parameters();

        Sane defaults will be passed

        Parameters
        ----------
        keyword : str
            keyword(s) that will be used for the search query

        Returns
        -------
        str
            Collected results of the request to the Twitter API.
        """

        query = gen_request_parameters(
            query=keyword,
            expansions=EXPANSIONS,
            user_fields=USER_FIELDS,
            media_fields=MEDIA_FIELDS,
            granularity=None,
            start_time=start_time.strftime("%Y-%m-%d"),
            end_time=end_time.strftime("%Y-%m-%d"),
            results_per_call=MAX_PER_CALL,
            tweet_fields=ATTRIB_STR,
        )

        collected_results = collect_results(
            query=query, result_stream_args=self.credentials, max_tweets=MAX_TWEETS
        )

        return collected_results

    def scrape(self) -> None:

        # for date in date range
        for start_date, end_date in daterange(self.age_threshold, datetime.now()):

            # get data with specified keywords
            data = self.search(" OR ".join(self.keywords), start_date, end_date)

            # properly format data
            new_dataset = self.format_collected_data(data)
            new_dataset = pd.DataFrame(new_dataset)

            # flush data to file (with date range in filename)
            self.flush_posts(
                path.join(
                    self.output_dir,
                    FILENAME_CONVENTION.format(
                        start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
                    ),
                ),
                new_dataset,
            )


def main():

    import argparse

    parser = argparse.ArgumentParser(description="Scraper for scraping Twitter Posts")
    parser.add_argument(
        "-d",
        "--start_date",
        type=str,
        help="Earliest date range you wish to gather data from; Format: MM/YYYY ; None == Beginning of history",
        default=None,
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        required=True,
        type=str,
        help="Directory where the output data file(s) will be stored",
    )
    parser.add_argument(
        "-k",
        "--keywords_file",
        help="File path where list of keywords is stored",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-c",
        "--credentials",
        help="File path where the credentials.yaml file is located",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    twitter_scraper = TwitterScraper(
        args.keywords_file,
        args.credentials,
        args.start_date,
        args.output_dir,
    )
    twitter_scraper.scrape()


if __name__ == "__main__":
    main()
