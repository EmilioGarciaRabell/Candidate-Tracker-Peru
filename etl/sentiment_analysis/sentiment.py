from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import twitter_scrapper, reddit_scrapper,llm
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()
MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
tok = AutoTokenizer.from_pretrained(MODEL)
mdl = AutoModelForSequenceClassification.from_pretrained(MODEL)
mdl.eval()

@torch.inference_mode()
def predict_sentiment(text):
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=512)
    probs = torch.softmax(mdl(**inputs).logits, dim=-1).flatten()
    labels = ["negative", "neutral", "positive"]
    return labels[probs.argmax()], probs.tolist()


def process_content_sentiment(content: list[dict]):
   
    posts_info = []

    overall_sentiment = {"negative":0, "neutral":0, "positive":0}
    
    for item in content:
        if item is None or len(item) == 0:
            continue
        analyzed_comments = 0
        comments_sentiment = {"negative":0, "neutral":0, "positive":0}

        post_content = item.get("text")
        if not post_content or type(post_content) != str:
            continue
        
        label, _ = predict_sentiment(post_content)
        overall_sentiment[label] += 1

        # Get comments sentiment
        comments = item.get("comments", [])
        
        for comment in comments:
            if not comment or type(comment) != str:
                continue

            c_label, _ = predict_sentiment(comment)
            comments_sentiment[c_label] += 1
            analyzed_comments += 1

        for key,value in  comments_sentiment.items():
            overall_sentiment[key] += value

        post_info = {
            "text" : post_content,
            "comments_sentiment" : comments_sentiment,
            "analyzed_comments": analyzed_comments,
            "post_sentiment" : label
        }
        
        posts_info.append(post_info)
    
    return overall_sentiment, posts_info


def get_candidate_sentiment(candidate:str, id: int):
    # get content
    sub_reddits = ["Lima_Peru", "PERU"]
    reddit_content = []
    print(f"getting {candidate} reddit content")
    for reddit in sub_reddits:
        reddit_content += reddit_scrapper.get_reddit_posts_and_comments(candidate, reddit)

    print(f"getting {candidate} twitter content")
    twitter_content = twitter_scrapper.get_tweets_and_comments(candidate)

    overall_content = reddit_content + twitter_content
    
    # Apply sentiment analysis 
    overall_sentiment, posts_info = process_content_sentiment(overall_content)
    sentiment_result = llm.get_sentiment_summary(candidate, overall_sentiment, posts_info)
    return sentiment_result

def get_candidates_id():
    # get canditate name and ID
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None
    try:
        # Connect to the DB
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        query = sql.SQL(f"SELECT id, name FROM candidate_data.candidate_info ORDER BY id asc")
        cur.execute(query)

        candidates = cur.fetchall()
        cur.close()
        conn.close()
        return candidates
    except Exception as e:
        print("Error inserting party:", e)
        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return None



def insert_sentiment(content, candidate_id):
    """
    Inserts or updates sentiment and extracted summary data for a given candidate.
    
    Expects content in this format:
    {
        "negative": float,
        "positive": float,
        "neutral": float,
        "content": {
            "title": str,
            "summary": str,
            "content": str
        }
    }
    """

    # Defensive extraction (matches expected structure)
    negative = content.get("negative")
    positive = content.get("positive")
    neutral = content.get("neutral")

    
    title = content.get("title", "")
    summary = content.get("summary", "")
    body = content.get("content", "") 
    
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        sql = """
            UPDATE candidate_data.sentiment_analysis
            SET
                negative = %s,
                positive = %s,
                neutral = %s,
                title = %s,
                summary = %s,
                content = %s
            WHERE candidate_id = %s;
        """

        cur.execute(sql, (
            
            negative,
            positive,
            neutral,
            title,
            summary,
            body,
            candidate_id
            
        ))

        conn.commit()
        cur.close()
        conn.close()

       

    except Exception as e:
        print("Error puto")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    candidates = get_candidates_id()
    for id, candidate in candidates:
        if candidate == "Pendiente":
            continue
        candidate_sentiment = get_candidate_sentiment(candidate, id)
        insert_sentiment(candidate_sentiment, id)

