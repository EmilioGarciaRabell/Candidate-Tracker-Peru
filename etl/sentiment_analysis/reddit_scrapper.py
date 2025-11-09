import praw
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID_REDDIT")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET_REDDIT")
USER_AGENT = os.environ.get("USER_AGENT_REDDIT")
# Initialize Reddit client

def get_reddit_posts_and_comments(candidate, subreddit_name):
    processed_results = []

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )

    subreddit = reddit.subreddit(subreddit_name)

    results = subreddit.search(candidate, sort="new", limit=30)

    for result in results:
        # Safely replace 'MoreComments' objects
        result.comments.replace_more(limit=0)
        
        comments = []
        for comment in result.comments.list():
            # Skip any non-standard comment objects (like MoreComments)
            if hasattr(comment, "body"):
                comments.append(comment.body)
        
        processed_result = {
            "title": result.title,
            "text": result.selftext or "",
            "comments": comments[:10],  # limit to 10 to avoid overload
            "author": str(result.author) if result.author else "Unknown",
            "score": result.score,
            "url": result.url,
            "created_utc": result.created_utc,
        }

        processed_results.append(processed_result)
    
    return processed_results
    
#get_reddit_posts_and_comments( "Rafael Lopez Aliaga", "Lima_Peru")
