import requests
from bs4 import BeautifulSoup
import pandas as pd
from serpapi import GoogleSearch
import re
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
load_dotenv()
BASE_URL = "https://rpp.pe/politica/elecciones/elecciones-2026-conoce-cuales-son-los-partidos-politicos-inscritos-y-los-que-estan-en-proceso-de-inscripcion-noticia-1572877"

def fetch_page(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def find_ol(html):
    soup = BeautifulSoup(html, "lxml")
    ol_tag = soup.find("ol")
    return ol_tag

def format_names_list_from_ol(data):
    parties = []
    if data:
        items = [li.get_text(strip=True) for li in data.find_all("li")]

        for item in items:
     
            name = item.lower().split("fecha de inscripción")[0].strip()
            parties.append({"name": name})
        return parties

def get_wiki_link(party_name):
    query = f'"{party_name} (partido PERU)" site:es.wikipedia.org'
    params = {
    "engine": "google",
    "q": query,
    "api_key": os.environ.get('SERAPI')
    }
    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])

    if results:
        return results[0].get("link")
    else:
        return None


def get_party_info(wiki_link):
    if not wiki_link:
        return {"summary": None, "position": None, "ref": None, "error": "No link found"}

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/141.0.0.0 Safari/537.36"
        )
    }

    try:
        res = requests.get(wiki_link, headers=headers, timeout=5)
        res.raise_for_status()
    except requests.RequestException as e:
        return {"summary": None, "position": None, "error": str(e)}

    soup = BeautifulSoup(res.text, "html.parser")

    # --- Summary ---
    first_p = soup.select_one("p")
    if first_p:
        summary = first_p.get_text(" ", strip=True)
        # Replace multiple whitespace or zero-width characters
        summary = re.sub(r"[\u200b]+", " ", summary)
        summary = re.sub(r"\s+", " ", summary)
    else:
        summary = "No summary found."

    # --- Political Position ---
    position_cell = soup.find(
        "th", string=lambda t: t and ("Position" in t or "Posición" in t)
    )
    if position_cell:
        position_td = position_cell.find_next("td")
        if position_td:
            # Remove reference tags
            for sup in position_td.find_all("sup"):
                sup.decompose()
            position = position_td.get_text(" ", strip=True)
            # Remove zero-width spaces
            position = re.sub(r"[\u200b]+", " ", position)
            # Remove faction notes if present
            position = re.split(r"Facciones?:", position)[0].strip()
            # Collapse multiple spaces
            position = re.sub(r"\s+", " ", position)
        else:
            position = "Not listed."
    else:
        position = "Not listed."

    return {"summary": summary, "position": position, "ref": wiki_link}

def insert_into_table(party_dict):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    # Ensure required keys exist
    required_keys = ["name", "position", "summary", "ref"]
    if not all(key in party_dict for key in required_keys):
        print("Dictionary is missing required keys")
        return None

    try:
        # Connect to the DB
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        insert_query = sql.SQL("""
            INSERT INTO candidate_data.parties (name, position, summary, ref)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """)

        cur.execute(
            insert_query,
            (party_dict["name"], party_dict["position"], party_dict["summary"], party_dict["ref"])
        )
        party_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        print(f"Inserted party with id {party_id}")
        return party_id

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
    html = fetch_page(BASE_URL)
    data = find_ol(html)
    parties = format_names_list_from_ol(data)
    
    for party in parties:
        name = party.get('name')
        if not name:
            continue
        link = get_wiki_link(name)
        party_info = get_party_info(link) if link else {"summary": "not found", "position": "not found", "ref": "not_found"}
        if isinstance(party_info, dict):
            party.update(party_info)
            
        else:
            # fallback if something went wrong
            party.update({"summary": "not found", "position": "not found", "ref": "not_found"})
        insert_into_table(party)

            



if __name__ == "__main__":
    main()
