
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import requests
import re
from urllib.parse import urlparse
load_dotenv()
TWITTER_API_KEY = os.environ.get("TWITTER_API")
SERPER_API_KEY = os.environ.get("SERPER")
def download_twitter_image(image_url, filename):
    if image_url is None:
        return


    # Full path INCLUDING the output filename
    save_path = r"C:\Users\Emilio GR\Downloads\cand_img" + "\\" + filename

    img_data = requests.get(image_url).content
    with open(save_path, "wb") as f:
        f.write(img_data)

    print("Saved:", save_path)



def download_web_image(url, filename):
    if url is None:
        return

    save_path = r"C:\Users\Emilio GR\Downloads\cand_img" + "\\" + filename
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(r.content)

        return True

    except Exception as e:
        print(f"Skipping image {url} — {e}")
        return False

def upgrade_twitter_image_quality(url: str) -> str:
    if "name=" in url:
        # Replace size with highest quality
        return url.replace("name=normal", "name=orig")\
                  .replace("name=bigger", "name=orig")\
                  .replace("name=small", "name=orig")\
                  .replace("name=mini", "name=orig")

    # Legacy format: remove "_normal", "_bigger", etc.
    return (
        url.replace("_normal", "")
           .replace("_bigger", "")
           .replace("_mini", "")
    )


def get_twitter_profile_image(profile_url: str) -> str | None:
    """
    Takes a Twitter/X profile URL and returns the direct profile image URL.
    Example input: https://x.com/elonmusk
    """

    # Extract username from nearly any Twitter/X URL
    match = re.search(r"x\.com/(@?[\w\.]+)", profile_url)
    if not match:
        match = re.search(r"twitter\.com/(@?[\w\.]+)", profile_url)
    if not match:
        print("Invalid profile URL.")
        return None

    username = match.group(1).lstrip("@")

    # Call twitterapi.io
    url = f"https://api.twitterapi.io/twitter/user/info?userName={username}"
    headers = {"X-API-Key": TWITTER_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # The field that contains the image URL
        image_url = data.get("data").get("profilePicture")
        return image_url

    except Exception as e:
        print("Error:", e)
        return None


def get_candidate_image_url(person_name: str) -> str | None:
    """
    Searches Google Images via Serper API and returns the first usable image URL.
    """

    url = "https://google.serper.dev/images"

    query = f"{person_name} candidato Peru"
    payload = {
        "q": query
    }

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # data["images"] is a list of image results
        images = data.get("images", [])
        if not images:
            print("No images found.")
            return None

        # Choose best candidate
        # Each item usually contains: imageUrl, thumbnailUrl, title, source
        for img in images:
            if "imageUrl" in img:
                return img["imageUrl"]

        return None

    except Exception as e:
        print("Error:", e)
        return None



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

def get_candiate_twitter(id):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None
    try:
        # Connect to the DB
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        query = """SELECT twitter FROM candidate_data.social_media WHERE candidate_id=%s"""
        cur.execute(query,(id,))

        twitter = cur.fetchone()[0]
        cur.close()
        conn.close()
        return twitter
    except Exception as e:
        print("Error inserting party:", e)
        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return None

def main():
    candidates = get_candidates_id()
    for id, candidate in candidates:
        if candidate == "Pendiente":
            continue
        candidate_twitter = get_candiate_twitter(id)
        candidate+=".jpg"
        if candidate_twitter is None:
            img_url = get_candidate_image_url(candidate)
            download_web_image(img_url, candidate)
        else:
            img_url = get_twitter_profile_image(candidate_twitter)
            if img_url is None:
                continue
            img_url = upgrade_twitter_image_quality(img_url)
            download_twitter_image(img_url, candidate)


if __name__ == "__main__":
    main()