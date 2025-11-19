import requests
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
load_dotenv()
from google import genai
import os
import trafilatura
import unicodedata
from psycopg2.extras import Json


# --- Setup ---
SERPER_API_KEY = os.environ.get("SERPER")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

    

def extract_candidate_category_info(text, candidate, category):
    if not text:
        return {
            "content": "not_found",
            "ref": [{"quote": "not_found", "link": "not_found"}]
        }

    schema = {
        "type": "object",
        "properties": {
            "content": {"type": "string"},
            "ref": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "quote": {"type": "string"},
                        "link": {"type": "string"}
                    },
                    "required": ["quote", "link"]
                }
            }
        },
        "required": ["content", "ref"]
    }

    

    prompt = f"""
    Eres un analista experto en política peruana.

    Tarea:
    - Resume información sobre el candidato **{candidate}**, específicamente sobre la categoría **{category}**.
    - Usa únicamente el contenido proporcionado.
    - NO inventes información.
    - Utiliza informacion de cada uno de los links creando un texto corto que muestre el contenido de una manera informativa.
    - Devuelve el resultado en JSON EXACTAMENTE con este formato:

    {{
      "content": "<Párrafo explicativo>",
      "ref": [
        {{"quote": "<fragmento de texto usado>", "link": "<URL de donde salió>"}}
      ]
    }}

    Reglas:
    - "content" debe ser un parrafo coherente, escrito en español.
    - Cada entrada en "ref" debe contener:
        - "quote": frase textual extraída del artículo
        - "link": URL desde la cual proviene esa frase
    - Si falta información, devuelve:
        "content": "not_found"
        "ref": [ {{"quote": "not_found", "link": "not_found"}} ]
    - Asegurate de porfavor insertar cada referencia a cada dato al que te refieras
    - Es de suma importancia que si agregas algo como referencia que en verdad lo hayas usado en el parrafo inicial
    - Intenta no solo incluir texto de un solo link si no que intenta recaudar informacion variada porfavor.
    - Enfocate en contenido que sea explicitamente relacionado con la categoria de {category} no incluyas informacion irrelevante
    - No utilices wikipedia como la fuente principal, si alguno de las fuentes tiene un resultado contradictorio con otra mencionalo.
    - Mi vida depende en que sigas el formato de manera correcta.
    Diccionario de texto disponible con links y texto asociado:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema
        }
    )

    # If Gemini returns parsed structured output, prefer that
    result = getattr(response, "parsed", None)
    if result:
        return result

    # fallback in case Gemini returns text
    return {
        "content": "not_found",
        "ref": [{"quote": "not_found", "link": "not_found"}]
    }




def verify_credibility(google_search_response):
    invalid_domains = ["facebook.com", "x.com", "youtube.com", "instagram.com", "tiktok.com", "jne.gob.pe"]
    filtered_results = []
    for r in google_search_response:
        url = r.get("link", "")
        keep = True
        for domain in invalid_domains:
            if domain in url:
                keep = False
                break
        if keep:
            filtered_results.append(r)

    return filtered_results


def get_category_links(candidate, category):
    categories = {
        "Polemicas":[f"Antecedentes de {candidate} candidato Peru", f"Polemicas de {candidate} candidato Peru"],
        "Biografia":[f"Biografia de {candidate} candidato Peru", f"Vida de {candidate} candidato Peru", f"Historia de {candidate} candidato Peru", f"Logros de {candidate} candidato Peru", f"Quien es {candidate} candidato Peru"],
        "Experiencia Laboral":[f"Experiencia Laboral de {candidate} candidato Peru"],
        "Educacion":[f"Educacion de {candidate} candidato Peru"]

        }
    
    queries = categories[category]
    i = 0
    for query in queries:
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
                "q": query,
                "num": 5
        }

        r = requests.post("https://google.serper.dev/search", json=payload, headers=headers)
        data = r.json()

        results = data.get("organic", [])
        if len(results) == 0 and i <len(categories[category])-1:
            i+=1
            continue
        return results
       

def fetch_text_from_url(url):
    """
    Fetch article text + return it paired with its origin link.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            if text:
                return {
                    url:text
                }
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    
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

def process_candidate_category(candidate_id, candidate_name, category):
    print(f"\n--- Processing {candidate_name} | Category: {category} ---")

    # 1. Search links
    results = get_category_links(candidate_name, category)
    if not results:
        print("No search results.")
        return

    # 2. Filter junk domains
    credible_links = verify_credibility(results)

    # 3. Extract text WITH linked source
    extracted_sources = {}

    for item in credible_links:
        result = fetch_text_from_url(item["link"])
        if result:  # result is {"text": ..., "link": ...}
            extracted_sources.update(result)

    if not extracted_sources:
        print("No usable article text found.")
        final = {
            "content": "not_found",
            "ref": [{"quote": "not_found", "link": "not_found"}]
        }
        #insert_candidate_category(candidate_id, category, final)
        return


    max_total_chars = 200_000
    num_docs = len(extracted_sources)

    max_per_doc = max_total_chars // num_docs
    limited_sources = {}

    for link, text in extracted_sources.items():
        cleaned = text.strip()
        limited_sources[link] = cleaned[:max_per_doc]  # hard truncate
        
    # Call Gemini extraction
    extracted = extract_candidate_category_info(
        extracted_sources,
        candidate_name,
        category
    )

    # Safety fallback
    if not extracted:
        extracted = {
            "content": "not_found",
            "ref": [{"quote": "not_found", "link": "not_found"}]
        }

    # 7. Insert into DB (your line commented out)
    # insert_candidate_category(candidate_id, category, extracted)
    insert_content(extracted, candidate_id, category)
    return extracted.get("ref")




def insert_content(content, candidate_id, category):

    new_content = content.get("content")
    

    if category == "Polemicas":
        column_name = "polemicas"
    elif category == "Biografia":
        column_name = "summary"
    elif category == "Experiencia Laboral":
        column_name = "work_experience"
    elif category == "Educacion":
        column_name = "education"

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        sql = f"""
            UPDATE candidate_data.candidate_info
            SET {column_name} = %s
            WHERE id = %s
        """

        cur.execute(sql, (
            new_content,
            
            candidate_id
        ))

        conn.commit()
        cur.close()
        conn.close()


    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_refs(candidate_id, refs):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        sql = """
            UPDATE candidate_data.candidate_info
            SET ref = %s
            WHERE id = %s
        """

        cur.execute(sql, (
            Json(refs),   # <-- makes dict/list safe for jsonb
            candidate_id
        ))

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def main():
    candidates = get_candidates_id()
    categories = ["Polemicas", "Biografia", "Experiencia Laboral", "Educacion"]
    
    for candidate_id, candidate_name in candidates:
        all_refs = []

        if candidate_name == "Pendiente":
            continue

        for category in categories:
            used_refs = process_candidate_category(candidate_id, candidate_name, category)

            if used_refs:               # ensure not None
                all_refs.extend(used_refs)   # <-- append lists correctly

        update_refs(candidate_id, all_refs)


if __name__ == "__main__":
    main()

