from searchtweets import load_credentials, gen_request_parameters, collect_results
import pprint

conversation_ids = []


def get_tweet_data(tweet):
    global conversation_ids
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

    conversation_id = tweet["conversation_id"] if "conversation_id" in tweet else None
    conversation_ids.append(conversation_id)
    created_at = tweet["created_at"] if "created_at" in tweet else None
    in_reply_to_user_id = (
        tweet["in_reply_to_user_id"] if "in_reply_to_user_id" in tweet else None
    )
    lang = tweet["lang"] if "lang" in tweet else None
    public_metrics = tweet["public_metrics"] if "public_metrics" in tweet else None
    referenced_tweets = (
        tweet["referenced_tweets"] if "referenced_tweets" in tweet else None
    )

    data = [
        id,
        text,
        attachments,
        author_id,
        author_name,
        author_username,
        conversation_id,
        created_at,
        in_reply_to_user_id,
        lang,
        public_metrics,
        referenced_tweets,
    ]

    pprint.pprint(conversation_id)
    return data


def collect_tweets(query):

    search_args = load_credentials(
        "twitter_keys.yaml", yaml_key="search_tweets_v2", env_overwrite=False
    )

    query = gen_request_parameters(
        query,
        results_per_call=10,
        granularity=None,
        tweet_fields="id,text,attachments,author_id,conversation_id,created_at,in_reply_to_user_id,lang,public_metrics,referenced_tweets",
        expansions="author_id,in_reply_to_user_id,attachments.media_keys",
        user_fields="id,name,username",
        media_fields="media_key,type,url,variants",
    )

    results = collect_results(query, max_tweets=10, result_stream_args=search_args)

    return results


results = collect_tweets("internet")

if len(results) > 0:
    tweets = results[0]["data"] if "data" in results[0] else None
    media = (
        results[0]["includes"]["media"] if "media" in results[0]["includes"] else None
    )
    users = (
        results[0]["includes"]["users"] if "users" in results[0]["includes"] else None
    )

    for tweet in tweets:
        get_tweet_data(tweet)

for conversation_id in conversation_ids:
    results = collect_tweets(conversation_id)

    if len(results) > 0:
        tweets = results[0]["data"] if "data" in results[0] else None
        media = (
            results[0]["includes"]["media"]
            if "media" in results[0]["includes"]
            else None
        )
        users = (
            results[0]["includes"]["users"]
            if "users" in results[0]["includes"]
            else None
        )

        for tweet in tweets:
            get_tweet_data(tweet)
