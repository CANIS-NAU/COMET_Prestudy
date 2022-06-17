import praw, pandas as pd, time, pprint, copy
from psaw import PushshiftAPI
from praw.models import MoreComments
from datetime import datetime as dt

# years to search between
start_year = 2017
end_year = 2022

last_date = '0000-00-00'

# create API instance
api = PushshiftAPI()

# create the reddit instance
reddit = praw.Reddit(
    client_id = 'IpDUzS3J1px-puPjB-Tocw',
    client_secret = 'OkGB3gaRRIsdyJVMqsk9vwnXhZVKyg',
    user_agent = 'COMET Data Gathering by ApartmentBrief8132'
)

# read through keywords and create query 
f = open('clean_keywords.txt', 'r')
keywords = list(f)
query = ''
for keyword in keywords:
    if keyword != keywords[-1]:
        keyword = keyword.replace('\n', '').strip()
        query += keyword + '|'   
f.close() 


# loop through years
for year in range(start_year, end_year+1):
    ts_after = int(dt(year, 1, 1).timestamp())
    ts_before = int(dt(year+1, 1, 1).timestamp())

    # loop while true
    while True:
        # get reddit search results
        results = api.search_submissions(
            after = ts_after,
            before = ts_before,
            q = query,
            filter = ['id'],
            sort = 'asc',
            limit = 100
        )
        print(dt.fromtimestamp(ts_after), dt.fromtimestamp(ts_before))

        # turn result into a list
        results = list(results)

        # if the num of results > 0
        if len(results) > 0:

            while True and len(results) > 0:
                try:
                    # get the last post date and make it the timestamp to search after
                    last_post = results[-1]
                    last_post_id = last_post.d_['id']
                    last_post = reddit.submission(id=last_post_id)
                    ts_after = int(last_post.created_utc)
                    break
                except:
                    results = results[0:len(results)-1]
                    continue 

            # loop through each submission
            for result in results:

                # try statement to avoid errors due to private subreddits or posts
                try:

                    # get the main submission data
                    id = result.d_['id']
                    post = reddit.submission(id=id)
                    database_subreddit = post.subreddit_name_prefixed
                    database_author = post.author
                    database_time_created = dt.fromtimestamp(post.created_utc)
                    date_created = str(database_time_created).split(' ')[0]

                    # if this submission month does not equal the last one, then create a new csv file to work with
                    if last_date != date_created:
                        year = date_created.split('-')[0]
                        month = date_created.split('-')[1]
                        day = date_created.split('-')[2]
                        result_file = 'reddit_' + year + month + day + '.tsv'
                        dataframe = pd.DataFrame(columns = ['id', 'subreddit', 'author', 'time and date created', 'title', 'text', 'media', 'number of comments', 'comment ids', 'url', 'upvotes', 'downvotes', 'score'])
                        dataframe.to_csv(result_file, sep='\t')
                        database_id = 1
                        last_date = date_created

                    # continue getting main submission data
                    database_title = post.title
                    database_text = post.selftext
                    database_media = post.media
                    database_number_of_comments = post.num_comments
                    database_comment_ids = [str(database_id) + '_' + str(num) for num in range(1, database_number_of_comments + 1)]
                    database_url = post.url
                    database_upvotes = post.ups
                    database_downvotes = post.downs
                    database_score = post.score
                    dataframe = pd.DataFrame([[database_id, database_subreddit, database_author, database_time_created, database_title, database_text, database_media, database_number_of_comments, database_comment_ids, database_url, database_upvotes, database_downvotes, database_score]])
                    dataframe.to_csv(result_file, mode='a', header=False, sep='\t')

                    # get the submission comments
                    comments = post.comments
                    comments = list(comments)
                    count = 1

                    # loop through submission comments
                    for comment in comments:

                        # get main comment data
                        database_comment_id = str(database_id) + '_' + str(count)
                        database_comment_ids.append(database_comment_id)
                        database_subreddit = comment.subreddit_name_prefixed
                        database_author = comment.author
                        database_time_created = dt.fromtimestamp(comment.created_utc)
                        database_title = None
                        database_text = comment.body
                        database_media = None
                        database_number_of_replies = len(list(comment.replies))
                        database_reply_ids = [str(database_id) + '_' + str(num + count) for num in range(1, database_number_of_replies + 1)]
                        database_url = None
                        database_upvotes = comment.ups
                        database_downvotes = comment.downs
                        database_score = comment.score
                        dataframe = pd.DataFrame([[database_comment_id, database_subreddit, database_author, database_time_created, database_title, database_text, database_media, database_number_of_replies, database_reply_ids, database_url, database_upvotes, database_downvotes, database_score]])
                        dataframe.to_csv(result_file, mode='a', header=False, sep='\t')
                        count += 1

                        # get the comment replies
                        replies = comment.replies
                        replies = list(replies)

                        # loop through the comment replies
                        for reply in replies:
                            database_reply_id = str(database_id) + '_' + str(count)
                            database_reply_ids.append(database_reply_id)
                            database_subreddit = reply.subreddit_name_prefixed
                            database_author = reply.author
                            database_time_created = dt.fromtimestamp(reply.created_utc)
                            database_title = None
                            database_text = reply.body
                            database_media = None
                            database_number_of_replys = 0
                            database_reply_ids_reply = []
                            database_url = None
                            database_upvotes = reply.ups
                            database_downvotes = reply.downs
                            database_score = reply.score
                            dataframe = pd.DataFrame([[database_reply_id, database_subreddit, database_author, database_time_created, database_title, database_text, database_media, database_number_of_replys, database_reply_ids_reply, database_url, database_upvotes, database_downvotes, database_score]])
                            dataframe.to_csv(result_file, mode='a', header=False, sep='\t')
                            count+= 1

                    # increment post submission 
                    database_id += 1
                
                # continue if the private error occurs
                except:
                    continue

        # if the list of results is less than 100, there are no more results, so go to the next subreddit
        elif len(results) == 0:
            break
        # otherwise, keep looking between the new ts_after and the same ts_before
        else:
            continue    