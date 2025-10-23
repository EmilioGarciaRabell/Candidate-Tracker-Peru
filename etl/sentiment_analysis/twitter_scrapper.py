import requests
from datetime import datetime, timedelta, timezone
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
TWITTER_API_KEY = os.environ.get("TWITTER_API")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
tok = AutoTokenizer.from_pretrained(MODEL)
mdl = AutoModelForSequenceClassification.from_pretrained(MODEL)
mdl.eval()

@torch.inference_mode()
def predict_sentiment(text):
    inputs = tok(text, return_tensors="pt", truncation=True)
    probs = torch.softmax(mdl(**inputs).logits, dim=-1).flatten()
    labels = ["negative", "neutral", "positive"]
    return labels[probs.argmax()], probs.tolist()


def get_candidate_twits_and_sentiment_analysis(candidate):
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

    overall_sentiment = {"positive":0,"negative":0,"neutral":0,"total":0}
    while True:
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code != 200:
            print("❌ Error:", response.status_code, response.text)
            break

        data = response.json()
        tweets = data.get("tweets", [])

        print(f"✅ Page {page}: Retrieved {len(tweets)} tweets")
        page += 1

        for t in tweets:
            author = t.get("author", {})
            created_at_str = t.get("createdAt", "N/A")
            text = t.get("text", "")
            all_tweets.append({
                "author": author,
                "username": author.get("username") or author.get("name") or "unknown",
                "text": text,
                "likes": t.get("likeCount", 0),
                "retweets": t.get("retweetCount", 0),
                "created":created_at_str,
            })

            # sentiment analysis
            if len(text) > 1200:
                continue
            sentiment = predict_sentiment(text)[0]
            overall_sentiment[sentiment] += 1
            overall_sentiment["total"] += 1

            if created_at_str:
                created_at = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")

                # Compare using UTC
                now = datetime.now(timezone.utc)
                print(f"date:  {created_at}")

                if now - created_at > timedelta(days=15):
                    return  # tweet is older than 15 days

        # Pagination: Stop if no next page
        if not data.get("has_next_page"):
            print("🚫 No more pages.")
            break

        # Update cursor for next request
        params["cursor"] = data.get("next_cursor", "")
        if not params["cursor"]:
            print("🚫 Cursor missing, stopping.")
            break
        
    return all_tweets, overall_sentiment


def get_twitter_summary(candidate, tweets, sentiment):
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
                You are an expert political sentiment analyst.

                Task:
                Analyze public sentiment about the Peruvian presidential candidate **{candidate}** using ONLY the information from:
                1️⃣ The tweets provided
                2️⃣ The aggregated sentiment analysis statistics

                Do NOT use external knowledge or make assumptions beyond the data.

                Please provide a structured analysis including:
                - 🧠 **Overall sentiment** (how positive/negative/mixed?)
                - 🔑 **Top themes** mentioned in the tweets (bullet points)
                - 🎯 **Most common praise** (bullet points)
                - ⚠️ **Most common criticisms** (bullet points)
                - 📊 A clear **sentiment score interpretation** based on the provided sentiment structure
                - 📝 3–5 short **representative example tweet summaries** (not direct quotes)

                Here is the tweet dataset:
                {tweets}

                Here is the sentiment analysis summary:
                {sentiment}

                Make the report concise, insightful, and data-driven. Please respond in spanish.
                """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print(response.text)


def main():
    candidate = "Rafael Lopez Aliaga"
    all_tweets, sentiment = get_candidate_twits_and_sentiment_analysis(candidate)
    get_twitter_summary(candidate, all_tweets, sentiment)

if __name__ == "__main__":
    main()