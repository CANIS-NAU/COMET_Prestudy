import praw, pandas as pd, time, pprint, copy
from psaw import PushshiftAPI
from praw.models import MoreComments
from datetime import datetime as dt

subreddits = ['Flagstaff', 'NAU']
start_year = 2017
end_year = 2022

api = PushshiftAPI()

reddit = praw.Reddit(
    client_id = 'IpDUzS3J1px-puPjB-Tocw',
    client_secret = 'OkGB3gaRRIsdyJVMqsk9vwnXhZVKyg',
    user_agent = 'COMET Data Gathering by ApartmentBrief8132'
)

keywords = open('clean_keywords.txt', 'r')

time.sleep(60)

for year in range(start_year, end_year+1):
    database_id = 1

    ts_after = int(dt(year, 1, 1).timestamp())
    ts_before = int(dt(year+1, 1, 1).timestamp())

    for subreddit in subreddits:
        result_file = str(year) + '_' + subreddit + '_results.csv'
        dataframe = pd.DataFrame(columns = ['id', 'subreddit', 'author', 'time and date created', 'title', 'text', 'media', 'number of comments', 'comment ids', 'url', 'likes', 'upvotes', 'downvotes', 'score'])
        dataframe.to_csv(result_file)

        for keyword in keywords:

            while True:

                results = api.search_submissions(
                    after = ts_after,
                    before = ts_before,
                    q = keyword,
                    filter = ['id'],
                    sort = 'asc',
                    subreddit = subreddit,
                    limit = 100
                )

                results = list(results)
                # get the last post date and make it the timestamp to search after
                last_post = results[-1]
                last_post_id = last_post.d_['id']
                last_post = reddit.submission(id=last_post_id)
                ts_after = last_post.created_utc

                for result in results:
                    id = result.d_['id']
                    post = reddit.submission(id=id)
                    database_subreddit = post.subreddit_name_prefixed
                    database_author = post.author
                    database_time_created = dt.fromtimestamp(post.created_utc)
                    database_title = post.title
                    database_text = post.selftext
                    database_media = None
                    database_number_of_comments = post.num_comments
                    database_comment_ids = [str(database_id) + '_' + str(num) for num in range(1, database_number_of_comments + 1)]
                    database_url = post.url
                    database_likes = post.likes
                    database_upvotes = post.ups
                    database_downvotes = post.downs
                    database_score = post.score
                    dataframe = pd.DataFrame([[database_id, database_subreddit, database_author, database_time_created, database_title, database_text, database_media, database_number_of_comments, database_comment_ids, database_url, database_likes, database_upvotes, database_downvotes, database_score]])
                    dataframe.to_csv(result_file, mode='a', header=False)

                    comments = post.comments
                    comments = list(comments)

                    for comment in comments:
                        database_comment_id = database_comment_ids[comments.index(comment)]
                        database_subreddit = comment.subreddit_name_prefixed
                        database_author = comment.author
                        database_time_created = dt.fromtimestamp(comment.created_utc)
                        database_title = None
                        database_text = comment.body
                        database_media = None
                        database_number_of_comments = 0
                        database_comment_ids_comment = []
                        database_url = None
                        database_likes = comment.likes
                        database_upvotes = comment.ups
                        database_downvotes = comment.downs
                        database_score = comment.score
                        dataframe = pd.DataFrame([[database_comment_id, database_subreddit, database_author, database_time_created, database_title, database_text, database_media, database_number_of_comments, database_comment_ids_comment, database_url, database_likes, database_upvotes, database_downvotes, database_score]])
                        dataframe.to_csv(result_file, mode='a', header=False)

                    database_id += 1

                # sleep to make sure we stay at the 100 post limit per minute
                time.sleep(60)

                # if the list of results is less than 100, there are no more results, so go to the next subreddit
                if len(results) < 5:
                    continue
            
        break
    break