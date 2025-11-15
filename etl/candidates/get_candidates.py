import os
import re
import unicodedata
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from serpapi import GoogleSearch
import wikipediaapi
from google import genai
import os
load_dotenv()

# --- Setup ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


BASE_URL = "https://elcomercio.pe/elecciones/elecciones-2026-jne-candidatos-presidenciales-estos-son-los-mas-de-60-aspirantes-que-se-proyectan-hacia-el-sillon-presidencial-en-las-proximas-elecciones-del-12-de-abril-elecciones-primarias-noticia/"

load_dotenv()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}


def fetch_page(url, headers=HEADERS):
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    return res.text

def get_wikipedia_page(name: str):
    wiki = wikipediaapi.Wikipedia(
        language='es',
        user_agent='candidate-info-fetcher/1.0 (contact@example.com)'
    )
    page = wiki.page(name)
    if not page.exists():
        return None, None
    
    # Collect reference links if available
    references = []
    for link_title in page.references.keys() if hasattr(page, "references") else []:
        link = page.references[link_title]
        if link and link.startswith("http"):
            references.append(link)

    return page.text, page.fullurl




def get_candidates():
    # request setup
    html = fetch_page(BASE_URL)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"aria-label": "Organizaciones políticas y candidatos"})
    if not table:
        raise Exception("No se encontró la tabla de candidatos.")

    candidates = []
    # get all the tr tags
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td"])

        partido = cols[0]
        candidato = cols[1].find("button")
        vicepresidentes = cols[1].find("ul")


        if candidato and partido and vicepresidentes:
            lista_vice = []
            for item in vicepresidentes.find_all("li"):
                lista_vice.append(item.text)        
            candidates.append({"name": candidato.text, "partido": partido.text.lower()})

    return candidates


def extract_candidate_info(name: str):
    text, url = get_wikipedia_page(name)
    if not text:
        return None

    schema = {
        "type": "object",
        "properties": {
            "age": {"type": "string"},
            "educacion": {"type": "string"},
            "summary": {"type": "string"},
            "ref": {"type": "array", "items": {"type": "string"}}
            # ,
            # "controversies": {
            #     "type": "array",
            #     "items": {
            #         "type": "object",
            #         "properties": {
            #             "summary": {"type": "string"},
            #             "ref": {"type": "array", "items": {"type": "string"}}
            #         }
            #     }
            # },
            # "accomplishments": {
            #     "type": "array",
            #     "items": {
            #         "type": "object",
            #         "properties": {
            #             "summary": {"type": "string"},
            #             "ref": {"type": "array", "items": {"type": "string"}}
            #         }
            #     }
            # }
        },
        "required": ["age","educacion", "summary", "ref"]
    }

    prompt = f"""
    Eres un analista experto en política peruana.
    Lee la siguiente información de Wikipedia (en español) sobre el candidato "{name}".
    Extrae los datos clave en formato JSON según el esquema dado. Para la edad, solo da el numero de cuantos anos tiene

    Si alguna de estas secciones ["age","educacion", "summary", "ref"], no tiene un resultado dale un valor como el siguiente: "age":-1,"summary": "not found", "ref": ["not_found"],"educacion":"not_found". Para "age" debe ser un numero : -1 y "ref" una lista: ["not_found"]
    Si encuentras hechos relevantes (controversias o logros), incluye una breve descripción
    y una lista con los enlaces de referencia correspondientes. 

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
            SELECT id, lower(name) FROM candidate_data.parties
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



def insert_into_table(candidate_dict):
    """Insert candidate into table"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        insert_query = sql.SQL("""
            INSERT INTO candidate_data.candidate_info 
            (name, age, party_id, education, summary, ref)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """)

        cur.execute(insert_query, (
            candidate_dict.get("name","not_found"),
            candidate_dict.get("age",-1),
            candidate_dict.get("partido",-1),
            candidate_dict.get("educacion","not_found"),
            candidate_dict.get("summary","not_found"),
            candidate_dict.get("ref",["not_found"])
        ))
        candidate_id = cur.fetchone()[0]

        conn.commit()
        conn.close()
        print(f"Inserted candidate with id {candidate_id}")
        return candidate_id

    except Exception as e:
        print("Error inserting candidate:", e)
        if conn:
            conn.rollback()
            conn.close()
        return None

def main():
    # get the raw candidates data from the wikipedia table
    raw_candidates = get_candidates()
    # get the parties information from the DB
    parties, parties_names = get_parties_table()
    # candidates container
    candidates = []

    for candidate in raw_candidates:
        
        # get the information about the candidate from wikipedia

        # clean the party field
        partido = candidate["partido"].lower()
        # assign the party id to the candidate 
        candidate["partido"] = parties.get(partido, None)

        new_candidate = candidate.copy()
        
        candidate_info = extract_candidate_info(candidate["name"])
        if isinstance(candidate_info, dict):
            new_candidate.update(candidate_info)
        else:
            new_candidate.update({"age":-1,"summary": "not found", "ref": ["not_found"],"educacion":"not_found"})

        candidates.append(new_candidate)
        # # Insert candidate into table
        if new_candidate: 
            insert_into_table(new_candidate)
        
if __name__ == "__main__":
    main()

