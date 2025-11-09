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
from google import genai
import wikipediaapi
import os

# --- Setup ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

BASE_URL = "https://elcomercio.pe/elecciones/elecciones-2026-jne-candidatos-presidenciales-estos-son-los-mas-de-60-aspirantes-que-se-proyectan-hacia-el-sillon-presidencial-en-las-proximas-elecciones-del-12-de-abril-elecciones-primarias-noticia/"

def fetch_page(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def get_parties(html):
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"aria-label": "Organizaciones políticas y candidatos"})
    if not table:
        raise Exception("No se encontró la tabla de candidatos.")

    parties = set()
    list_candidates = []
    # get all the tr tags
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td"])

        partido = cols[0]
        if partido:
            parties.add(partido.text)
    
    for party in parties:
        list_candidates.append({"name":party})

    return list_candidates

def get_wikipedia_page(name: str):
    wiki = wikipediaapi.Wikipedia(
        language='es',
        user_agent='candidate-info-fetcher/1.0 (contact@example.com)'
    )
    page = wiki.page(name)
    if not page.exists():
        return None, None, []
    
    # Collect reference links if available
    references = []
    for link_title in page.references.keys() if hasattr(page, "references") else []:
        link = page.references[link_title]
        if link and link.startswith("http"):
            references.append(link)

    return page.text, page.fullurl, references


def get_party_info(wiki_link):
    if not wiki_link:
        return {"summary": None, "position": None, "ref": ["not_found"], "error": "No link found"}

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
        summary = re.sub(r"\u200b+", " ", summary)
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
    
    return {"summary": summary, "position": position, "ref": [wiki_link]}

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
    parties = get_parties(html)
    
    for party in parties:
        name = party.get('name')
        if not name:
            continue
        link = get_wiki_link(name)
        party_info = get_party_info(link) if link else {"summary": "not found", "position": "not found", "ref": ["not_found"]}
        if isinstance(party_info, dict):
            party.update(party_info)
            
        else:
            party.update({"summary": "not found", "position": "not found", "ref": ["not_found"]})

        insert_into_table(party)
if __name__ == "__main__":
    main()
