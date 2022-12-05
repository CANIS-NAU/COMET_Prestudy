import praw, pandas as pd, time, pprint, copy
from psaw import PushshiftAPI
from praw.models import MoreComments
from datetime import datetime as dt
import datetime, os

# create API instance
api = PushshiftAPI()

# create the reddit instance
reddit = praw.Reddit(
    client_id = 'IpDUzS3J1px-puPjB-Tocw',
    client_secret = 'OkGB3gaRRIsdyJVMqsk9vwnXhZVKyg',
    user_agent = 'COMET Data Gathering by ApartmentBrief8132'
)

# initialize last date variable and post id
last_date = None
post_id = 1

def get_query(keywords_file: str) -> str:
    """Creates the query string with the provided keywords to use with the Reddit API

    Args:
        keywords_file (str): The file path and name to the keywords file

    Returns:
        str: The query string created with the provided keywords
    """

    # initialize the query string
    query = ''
    # open the provided keywords file to read
    file = open(keywords_file, 'r')
    # create a list from the keywords file
    keywords = list(file)

    # loop through the keywords file
    for keyword in keywords:

        # if the keyword is not the last keyword in the file
        # get rid of the new line character and strip the line
        # append the keyword and or character to the query
        if keyword != keywords[-1]:

            keyword = keyword.replace('\n', '').strip()
            query += str(keyword) + '|'

        # otherwise
        # get rid of the new line character and strip the line
        # append the keyword to the query
        else:

            keyword = keyword.replace('\n', '')
            query += str(keyword)

    # close the file
    file.close()

    # return the query
    return query

def update_output(data: list, date: str):
    """Creates and or updates the correct file with the data provided

    Args:
        data (list): The data of the post/comment/reply provided
        date (str): The date of the original post that the post/comment/reply data came from
    """

    # get the date from the data
    date = date.split(' ')[0]
    date = date.replace('-', '')
    output_file = 'reddit_' + date + '.tsv'

    # check to see if the correct file exists
    if os.path.exists(output_file):
        # if it does, update the file
        df = pd.DataFrame(data)
        df.to_csv(output_file, mode = 'a', sep = '\t', header = False)

    # if not, create the correct file and update it
    else:
        dataframe = pd.DataFrame(columns=['post_id', 'subreddit', 'author', 'date', 'title', 'text',
                             'media', 'comment ids', 'url', 'upvotes', 'downvotes', 'score', '# comments'])
        dataframe.to_csv(output_file, sep='\t')
        df = pd.DataFrame(data)
        df.to_csv(output_file, mode = 'a', sep = '\t', header = False)

def get_reply_data(comment: object, comment_id: str):
    """Retrieves the reply data of the provided comment

    Args:
        comment (object): The provided comment object
        comment_id (str): The provided comment id
    """

    # get the replies of the comment and turn it into a list
    replies = comment.replies
    replies = list(replies)

    # initialize the reply id
    reply_id = 1

    # loop through each reply
    # get the data from each reply
    for reply in replies:

        try:

            data = [{
            'post_id': comment_id + '_' + str(reply_id),
            'subreddit': reply.subreddit_name_prefixed,
            'author': reply.author.name,
            'date': str(dt.fromtimestamp(reply.created_utc)) if reply.created_utc != None else None,
            'title': None,
            'text': reply.body,
            'media': None,
            'comment ids': None,
            'url': None,
            'upvotes': reply.ups,
            'downvotes': reply.downs,
            'score': reply.score,
            '# comments': None
            }]

            # add the data into the correct file
            update_output(data, last_date)

            # increment the reply id
            reply_id += 1
        
        except:

            continue


def get_comment_data(post: object):
    """Retrieve the comment data from the provided post

    Args:
        post (object): The provided post object
    """

    # get the comments from the provided post
    # turn the comments into a list
    comments = post.comments
    comments = list(comments)

    # initialize the comment id
    comment_id = 1

    # loop through each comment
    # retrieve the comment data
    for comment in comments:

        try:

            data = [{
            'post_id': str(post_id) + '_' + str(comment_id),
            'subreddit': comment.subreddit_name_prefixed,
            'author': comment.author.name,
            'date': str(dt.fromtimestamp(comment.created_utc)) if comment.created_utc != None else None,
            'title': None,
            'text': comment.body,
            'media': None,
            'comment ids': [str(post_id) + '_' + str(comment_id) + '_' + str(num) for num in range(1, len(list(comment.replies)) + 1)] if len(list(comment.replies)) > 0 else None,
            'url': None,
            'upvotes': comment.ups,
            'downvotes': comment.downs,
            'score': comment.score,
            '# comments': len(list(comment.replies))
            }]

            # add the data to the correct file
            update_output(data, last_date)

            # get reply data
            get_reply_data(comment, data[0]['post_id'])

            # increment the comment id
            comment_id += 1

        except:

            continue

def get_post_data(post: object) -> int:
    """Retrieves the provided post objects data

    Args:
        post (object): The provided post object

    Returns:
        int: The date of the post object
    """

    # declare global variables
    global post_id, last_date

    # get the post id and the post from reddit
    id = post.d_['id']
    post = reddit.submission(id=id)

    # get the post data
    data = [{
        'post_id': post_id,
        'subreddit': post.subreddit_name_prefixed,
        'author': post.author.name,
        'date': str(dt.fromtimestamp(post.created_utc)) if post.created_utc != None else None,
        'title': post.title,
        'text': post.selftext,
        'media': post.media,
        'comment ids': [str(post_id) + '_' + str(num) for num in range(1, post.num_comments + 1)] if int(post.num_comments) > 0 else None,
        'url': post.url,
        'upvotes': post.ups,
        'downvotes': post.downs,
        'score': post.score,
        '# comments': post.num_comments
    }]

    # get the last date
    last_date = data[0]['date']

    # update tsv file
    update_output(data, last_date)

    # get comment data
    get_comment_data(post)

    # increment the post id variable
    post_id += 1

    # return the post date
    return int(post.created_utc)


def get_posts(ts_after: int, ts_before: int, query: str) -> list:
    """Uses the Pushshiftapi to gather submissions based on the provided parameters

    Args:
        ts_after (int): The date to start collecting posts
        ts_before (int): The date to stop collecting posts
        query (str): The string of keywords to look for in posts

    Returns:
        list: A list of post results
    """

    # get results
    results = api.search_submissions(
        after = ts_after,
        before = ts_before,
        q = query,
        filter = ['id'],
        sort = 'asc',
        limit = 100
    )

    # return result list
    return list(results)

def RedditScraper(after_date: str, before_date: str, keywords_file: str): 

    # get the keyword query
    query = get_query(keywords_file)

    # turn provided dates into timestamps
    ts_after = int(dt.strptime(after_date, '%m/%d/%Y').timestamp())
    ts_before = int(dt.strptime(before_date, '%m/%d/%Y').timestamp())

    while True:

        # retrieve submission results and turn results into a list
        posts = get_posts(ts_after, ts_before, query)

        # if results exist
        # loop through each result
        # gather data
        if len(posts) > 0:

            for post in posts:

                try:

                    ts_after = get_post_data(post)
                
                except:

                    continue

        else:

            break

    print('All done!')
    quit()

def main():

    import argparse

    parser = argparse.ArgumentParser(
        description = 'Reddit data collector with praw and psaw APIs'
    )

    parser.add_argument(
        '-ad',
        '--after_date',
        help = 'The date of posts to start collecting from, ex: MM/DD/YYY',
        type = str,
        required = True
    )

    parser.add_argument(
        '-bd',
        '--before_date',
        help = 'The date of posts to stop collecting from, ex: MM/DD/YYYY',
        type = str,
        required = True
    )

    parser.add_argument(
        '-k',
        '--keywords_file',
        help = 'The file path and name to get keywords from',
        type = str,
        required = True
    )

    args = parser.parse_args()

    RedditScraper(
        args.after_date,
        args.before_date,
        args.keywords_file
    )

if __name__ == '__main__':
    main()