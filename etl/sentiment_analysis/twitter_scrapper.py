import requests
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv


load_dotenv()
TWITTER_API_KEY = os.environ.get("TWITTER_API")


def get_tweets_and_comments(candidate):
    endpoint = "https://api.twitterapi.io/twitter/tweet/advanced_search"

    query = f'"{candidate}" lang:es -is:retweet'
    params = {
        "query": query,
        "queryType": "Top",
        "cursor": ""
    }
    headers = {"X-API-Key": TWITTER_API_KEY}

    all_tweets = []
    page = 1

    while True:
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        tweets = data.get("tweets", [])

        print(f"Page {page}: Retrieved {len(tweets)} tweets")
        page += 1

        for t in tweets:
            author = t.get("author", {})
            created_at_str = t.get("createdAt", "N/A")
            text = t.get("text", "")


            if created_at_str:
                created_at = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")

                # Compare using UTC
                now = datetime.now(timezone.utc)

                if now - created_at > timedelta(days=15):
                    return all_tweets  # tweet is older than 15 days


                conversation_id = t.get("conversationId")
                comments = []
                if conversation_id:
                    comments =  get_tweet_replies(conversation_id, headers)
                
                
                all_tweets.append({
                    "author": author,
                    "username": author.get("username") or author.get("name") or "unknown",
                    "text": text,
                    "likes": t.get("likeCount", 0),
                    "retweets": t.get("retweetCount", 0),
                    
                    "created":created_at_str,
                    "comments": comments
                })

        # Pagination: Stop if no next page
        if not data.get("has_next_page"):
            print("No more pages.")
            break

        # Update cursor for next request
        params["cursor"] = data.get("next_cursor", "")
        if not params["cursor"]:
            print("Cursor missing, stopping.")
            break
    return all_tweets


def get_tweet_replies(tweet_id, headers, max_replies=100):
    endpoint = "https://api.twitterapi.io/twitter/tweet/replies"
   

    params = {
        "tweetId": tweet_id,
        "cursor": ""
    }

    all_replies = []

    while True:
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        replies = data.get("tweets", [])

        for r in replies:
            all_replies.append({
                "id": r.get("id"),
                "text": r.get("text"),
                "author": r.get("author", {}).get("userName"),
                "createdAt": r.get("createdAt")
            })

        if not data.get("has_next_page"):
            break

        params["cursor"] = data.get("next_cursor", "")
        if not params["cursor"]:
            break

        if len(all_replies) > max_replies:
            break

    return all_replies
