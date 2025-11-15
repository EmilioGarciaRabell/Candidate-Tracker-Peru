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
from serpapi import GoogleSearch


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

import wikipedia

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

##Code for updating parties  summary
def get_wiki_page(party):
    try:
        wikipedia.set_lang("es-formal")
        page = wikipedia.page(party)
        if page:
            return page.url
        return None
    except Exception as e:
         print(e)
         return None

def get_wikipedia_page(name: str):
    wiki = wikipediaapi.Wikipedia(
        language='es',
        user_agent='candidate-info-fetcher/1.0 (contact@example.com)'
    )
    page = wiki.page(name)
    if not page.exists():
        return None, None

    return  page.text, page.fullurl
def get_parties_table():
    """Get the contents of the parties table"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None, []

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name FROM candidate_data.parties
            ORDER BY name ASC
        """)
        parties = cur.fetchall()
        conn.close()

        formatted_parties = {p[1].lower(): p[0] for p in parties}
        parties_names = [p[1] for p in parties]

        return formatted_parties, parties_names

    except Exception as e:
        print("Error while accessing parties table:", e)
        return None, []
    
def extract_party_info(text,url,name):
    if not text:
        return None
    schema = {
        "type": "object",
        "properties": {
            "ideology": {"type": "string"},
            "summary": {"type": "string"},
            "ref": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["ideology", "summary", "ref"]
    }

    prompt = f"""
    Eres un analista experto en política peruana.
    Lee la siguiente información sobre el partido politico "{name}".
    Extrae los datos clave en formato JSON según el esquema dado. 
    Si alguna de estas secciones ["ideology", "summary", "ref"], no tiene un resultado dale un valor como el siguiente: "ideology":"not found"","summary": "not found", "ref": ["not_found"]. Para "ref" debe ser  una lista: ["not_found"] 

    Texto de Wikipedia:
    {text[:12000]}  # (limita el texto para evitar desbordes)

    URL: {url}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema
        }
    )

    # fallback in case .parsed isn't set
    result = getattr(response, "parsed", None) or response.text
    return result                                                 

def insert_into_table(name,party_dict):
    """update candidate info table"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        insert_query = sql.SQL("""
            UPDATE candidate_data.parties
            SET position = %s,
                summary = %s,
                ref = %s
            WHERE name = %s;
        """)


        cur.execute(insert_query, (
            party_dict.get("ideology",-1),
            party_dict.get("summary","not_found"),
            party_dict.get("ref",["not_found"]),
            name,

        ))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Error inserting candidate:", e)
        if conn:
            conn.rollback()
            conn.close()
        return None

def update_party_info():
    _,party_names = get_parties_table()
    
    for party in party_names:
        text = ""
        url = ""
        if party == "Alianza para el Progreso":
            text,url = get_wikipedia_page("Alianza_para_el_Progreso_(Perú)")
        else:
            text, url = get_wikipedia_page(party)
        result = extract_party_info(text,url,party)
        if not result:
            result = {"ideology":"not found","summary": "not found", "ref": ["not_found"]}
        insert_into_table(party,result)


def get_party_website(name,num_results):
    params = {
        "engine": "google",
        "q": f"{name} partido politico peru",
        "num": num_results,
        "api_key": os.environ.get("SERAPI")
    }
    search = GoogleSearch(params)
    res = search.get_dict()
    return res.get("organic_results", [])


    
def main():
    print(get_party_website("Fe en el Peru", 1))
    # print(get_wikipedia_page('Alianza_para_el_Progreso_(Perú)'))
    

if __name__ == "__main__":
    main()
