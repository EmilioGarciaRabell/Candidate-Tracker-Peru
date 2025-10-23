import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("BEARER_TOKEN_TWITTER")
client = tweepy.Client(bearer_token=key)

query = "Pedro Castillo -is:retweet lang:es"
tweets = client.search_recent_tweets(
    query=query,
    tweet_fields=["created_at", "public_metrics", "text", "author_id"],
    max_results=100
)

if tweets.data:
    sorted_tweets = sorted(
        tweets.data,
        key=lambda x: x.public_metrics['like_count'] + x.public_metrics['retweet_count'],
        reverse=True

    )
    top_100 = sorted_tweets[:100]
    for i, t in enumerate(top_100[:10], 1):
        print(f"{i}. {t.text}\nLikes: {t.public_metrics['like_count']}, RTs: {t.public_metrics['retweet_count']}\n")
else:
    print("No tweets found.")