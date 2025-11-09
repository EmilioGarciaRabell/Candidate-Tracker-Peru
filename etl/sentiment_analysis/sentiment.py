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


def process_content_sentimnent(content:list[dict]):
   
    posts_info = []

    overall_sentiment = {"negative":0, "neutral":0, "positive":0}
    
    for item in content:
        analyzed_comments = 0
        comments_sentiment = {"negative":0, "neutral":0, "positive":0}

        post_content = item.get("text")
        if not post_content:
            break
        
        label, _ = predict_sentiment(post_content)
        overall_sentiment[label] += 1

        # Get comments sentiment
        comments = item.get("comments", [])
        
        for comment in comments:
            if not comment:
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

import os
import psycopg2
from psycopg2.extras import Json

import os
import psycopg2

import os
import psycopg2


def get_candidate_sentiment(candidate:str, id: int):
    # get content
    
    reddit_content = reddit_scrapper.get_reddit_posts_and_comments(candidate, "Lima_Peru")
    twitter_content = twitter_scrapper.get_tweets_and_comments(candidate)

    overall_content = reddit_content + twitter_content
    
    # Apply sentiment analysis 
    overall_sentiment, posts_info = process_content_sentimnent(overall_content)
    sentiment_result = llm.get_twitter_summary(candidate, overall_sentiment, posts_info)
    
    

    insert_sentiment(id, sentiment_result)

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
        query = sql.SQL(f"SELECT id, name FROM candidate_data.candidate_info")
        cur.execute(query)

        candidates = cur.fetchall()
        print(candidates)
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

    text_result = content.get("content", {})
    title = text_result.get("title", "") if isinstance(text_result, dict) else ""
    summary = text_result.get("summary", "") if isinstance(text_result, dict) else ""
    body = text_result.get("content", "") if isinstance(text_result, dict) else ""

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        sql = """
            UPDATE candidate_data.sentiment_analysis
            SET
                negative = %s,
                positive = %s,
                neutral  = %s,
                title = %s,
                summary = %s,
                content = %s
            WHERE id = %s
            RETURNING id;
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

        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if row:
            return {"status": "success", "updated_id": row[0]}
        else:
            return {"status": "error", "message": "No row updated (id not found)."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    candidates = get_candidates_id()
    for candidate, id in candidates:
        candidate_sentiment = get_candidate_sentiment(candidate, id)
        insert_sentiment(candidate_sentiment, id)

