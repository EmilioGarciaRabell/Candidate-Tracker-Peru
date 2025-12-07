import requests
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor



load_dotenv()
TWITTER_API_KEY = os.environ.get("TWITTER_API")


def get_tweets_and_comments(candidate):
    endpoint = "https://api.twitterapi.io/twitter/tweet/advanced_search"

    query = f'"{candidate}" lang:es -is:retweet'
    params = {
        "query": query,
        "queryType": "Latest",
        "cursor": ""
    }
    headers = {"X-API-Key": TWITTER_API_KEY}

    all_tweets = []
    conversation_ids = []

    now = datetime.now(timezone.utc)
    page = 1
    in_this_week = True
    while in_this_week:
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        tweets = data.get("tweets", [])

        print(f"Page {page}: Retrieved {len(tweets)} tweets")
        page += 1

        for t in tweets:
            created_at_str = t.get("createdAt")
            if not created_at_str:
                continue

            created_at = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")

            # If sorted newest → oldest, this means ALL NEXT tweets are even older
            if now - created_at > timedelta(days=7):
                in_this_week = False
                break

            conversation_id = t.get("conversationId")
            if conversation_id:
                conversation_ids.append(conversation_id)

            author = t.get("author", {})
            all_tweets.append({
                "author": author,
                "username": author.get("username") or author.get("name") or "unknown",
                "text": t.get("text", ""),
                "likes": t.get("likeCount", 0),
                "retweets": t.get("retweetCount", 0),
                "created": created_at_str,
                "conversationId": conversation_id
            })

        if not data.get("has_next_page"):
            break

        params["cursor"] = data.get("next_cursor", "")
        if not params["cursor"]:
            break

    # === Fetch replies in parallel ===
    print("processing comments")
    def fetch_replies(cid):
        return cid, get_tweet_replies(cid, headers)

    replies_map = {}

    with ThreadPoolExecutor(max_workers=15) as pool:
        for cid, comments in pool.map(fetch_replies, conversation_ids):
            replies_map[cid] = comments

    # Attach comments
    for tweet in all_tweets:
        cid = tweet["conversationId"]
        tweet["comments"] = replies_map.get(cid, [])

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





