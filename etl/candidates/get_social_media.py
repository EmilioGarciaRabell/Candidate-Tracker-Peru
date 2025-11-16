import requests
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse, parse_qs, unquote

load_dotenv()
API_KEY = os.environ.get("SERAPI")
SERPER_API_KEY = os.environ.get("SERPER")

SERPER_URL = "https://google.serper.dev/search"


SOCIAL_SITES = [         # Twitter now redirects here
    "twitter.com",
    "instagram.com",
    "facebook.com",

]

BAD_PATH_HEADS = {
    "twitter.com": {"search", "hashtag", "explore", "i", "home", "compose", "notifications", "messages", "settings"},
    "instagram.com": {"explore", "reels", "stories", "p", "accounts", "directory", "developer", "about"},
    "facebook.com": {"search", "marketplace", "events", "watch", "groups", "pages"},
}

# Only accept these hosts for each site (prevents help.instagram.com, l.instagram.com, etc.)
ALLOWED_HOSTS = {
    "twitter.com": {"twitter.com", "www.twitter.com"},
    "instagram.com": {"instagram.com", "www.instagram.com"},
    "facebook.com": {"facebook.com", "www.facebook.com", "m.facebook.com", "web.facebook.com"},
}

# Quick per-site “looks like a profile” checks
def _looks_like_profile(url: str) -> bool:
    try:
        u = urlparse(url)
        host = u.netloc.lower().replace("www.", "")
        path = u.path or "/"
        parts = [p for p in path.split("/") if p]

        # Gate 1: host allowlist
        # (special-case: allow m./web. for fb, but not link shims like l.instagram.com)
        if host not in {h.replace("www.", "") for hs in ALLOWED_HOSTS.values() for h in hs}:
            return False

        # Figure which site we're on via suffix
        site = None
        for base_site, hosts in ALLOWED_HOSTS.items():
            if host in {h.replace("www.", "") for h in hosts}:
                site = base_site
                break
        if site is None:
            return False

        if not parts:
            return False  # bare domain

        head = parts[0].lower()

        # Reject obvious non-profile heads
        if head in BAD_PATH_HEADS.get(site, set()):
            # Instagram login redirect edge-case handled below
            if not (site == "instagram.com" and head == "accounts" and parts[:2] == ["accounts", "login"]):
                return False

        # Instagram: accept /<username>/, and also /accounts/login/?next=/username/
        if site == "instagram.com":
            # login redirect to profile?
            if parts[:2] == ["accounts", "login"]:
                nxt = parse_qs(u.query or "").get("next", [""])[0]
                nxt = unquote(nxt)
                # next should be like /<username>/ ...
                n_parts = [p for p in nxt.split("/") if p]
                return len(n_parts) == 1
            # normal profile: one segment
            return len(parts) == 1

        # Facebook: accept /profile.php?id=... or exactly one segment (page/username)
        if site == "facebook.com":
            if path.startswith("/profile.php"):
                q = parse_qs(u.query or "")
                return "id" in q and q["id"][0].isdigit()
            # exclude obvious content subpaths
            if len(parts) >= 2 and parts[1].lower() in {"photos", "photo.php", "posts", "videos", "permalink.php"}:
                return False
            return len(parts) == 1

        # Twitter: one segment username; avoid deep paths like /status/...
        if site == "twitter.com":
            return len(parts) == 1

        return False
    except Exception:
        return False


def get_social_links(person):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    links = {}

    for site in SOCIAL_SITES:
        # Try a strict and a relaxed query
        queries = [
            f'site:{site} "{person}"',
            f"site:{site} {person}",
        ]
        best = None

        for query in queries:
            payload = {"q": query, "num": 20}  # small bump helps
            try:
                r = requests.post(SERPER_URL, json=payload, headers=headers, timeout=10)
                r.raise_for_status()
            except requests.RequestException:
                continue

            data = r.json()
            results = data.get("organic", []) or data.get("organic_results", [])
            if not results:
                continue

            # First: pick the first result that looks like a profile on the same site
            for item in results:
                link = item.get("link", "")
                if not link:
                    continue
                # ensure the link host matches the site we're searching (no shims)
                h = urlparse(link).netloc.lower().replace("www.", "")
                if h not in {hh.replace("www.", "") for hh in ALLOWED_HOSTS[site]}:
                    continue
                if _looks_like_profile(link):
                    best = link
                    break

            if best:
                break

            # If nothing matched strictly, skip fallback for IG/FB (to avoid posts/images)
            # Keep fallback for Twitter only (your Twitter results are good).
            if site == "twitter.com" and results:
                best = results[0].get("link")

        if best:
            links[site] = best

    return links

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




def insert_social_media(content, candidate_id):
    """
    """

    # Defensive extraction (matches expected structure)
    twitter = content.get("twitter.com")
    facebook = content.get("facebook.com")
    instagram = content.get("instagram.com")
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        sql = """
            INSERT INTO candidate_data.social_media(candidate_id,twitter, instagram, facebook)
            VALUES (%s,%s,%s,%s);
                
        """

        cur.execute(sql, (
            candidate_id,
            twitter,
            instagram,
            facebook
            
        ))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    candidates = get_candidates_id()
    for id, candidate in candidates:
        if candidate == "Pendiente":
            continue
        candidate_social_media = get_social_links(candidate)
        if len(candidate_social_media) == 0:
            continue
        insert_social_media(candidate_social_media, id)
    return

if __name__ == "__main__":
    main()