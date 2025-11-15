from google import genai
from psycopg2 import sql
import psycopg2
import wikipediaapi
import os
from dotenv import load_dotenv
load_dotenv()
import wikipedia
# print(wikipedia.languages())

def get_wiki_page(candidate):
    try:
        wikipedia.set_lang("es-formal")
        page = wikipedia.page(candidate)
        if page.title.lower() in candidate and len(page.title.split()) > 1:
            return page.content,page.url
        return None, None
    except Exception as e:
         print(e)
         return None,None


def get_candidates_table():
    """Get the contents of the parties table"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None, []

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        cur.execute("""
            SELECT id, lower(name) FROM candidate_data.candidate_info where age = -1
            ORDER BY name ASC
        """)
        candidates = cur.fetchall()
        conn.close()

        c = [p[1] for p in candidates]
        return c

    except Exception as e:
        print("Error while accessing parties table:", e)
        return None, []

def get_wikipedia_page(name: str):
    wiki = wikipediaapi.Wikipedia(
        language='es',
        user_agent='candidate-info-fetcher/1.0 (contact@example.com)'
    )
    page = wiki.page(name)
    if not page.exists():
        return None, None
    return page.text, page.fullurl


# --- Setup ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


def extract_candidate_info(name: str):
    text, url = get_wiki_page(name)
    if not text:
        text, url = get_wikipedia_page(name)
    if not text:
        return None
    schema = {
        "type": "object",
        "properties": {
            "age": {"type": "string"},
            "educacion":{"type": "string"},
            "summary": {"type": "string"},
            "ref": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["age","educacion", "summary", "ref"]
    }

    prompt = f"""
    Eres un analista experto en política peruana. Traduce todo el contenido a espanol. El resultado que das debe estar en espanol
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

            
def insert_into_table(name,candidate_dict):
    """update candidate info table"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        insert_query = sql.SQL("""
            UPDATE candidate_data.candidate_info
            SET age = %s,
                education = %s,
                summary = %s,
                ref = %s
            WHERE lower(name) = %s;
        """)


        cur.execute(insert_query, (
            candidate_dict.get("age",-1),
            candidate_dict.get("educacion","not_found"),
            candidate_dict.get("summary","not_found"),
            candidate_dict.get("ref",["not_found"]),
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

def get_wiki_for_all_candidates():
    candidates = get_candidates_table()
    for i in candidates:
        response = extract_candidate_info(i)
        if response:
            insert_into_table(i.lower(),response)



# --- Example ---
if __name__ == "__main__":
    print(get_wikipedia_page("Francisco_Diez_Canseco_Távara"))
    response = extract_candidate_info("Francisco_Diez_Canseco_Távara")
    print(response)
    insert_into_table("francisco diez canseco",response)

##to do get biographies of candidates missing