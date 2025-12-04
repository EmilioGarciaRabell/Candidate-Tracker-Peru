import requests
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

from google import genai
import os
import trafilatura
from psycopg2.extras import Json


load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
SERPER_API_KEY = os.environ.get("SERPER")

# Instrucciones para Experiencia Laboral
WORKEXP_INSTRUCTIONS = (
    "Genera un objeto JSON donde la clave principal sea EXACTAMENTE 'Experiencia Laboral'. "
    "El valor de esta clave debe ser una lista de objetos, donde cada uno represente un puesto con: "
    "'title' (título/cargo), 'institution' (empresa), 'place' (lugar) y 'time' (fecha/años). "
    "No inventes información."
)

# Instrucciones para Educación
EDUCATION_INSTRUCTIONS = (
    "Genera un objeto JSON donde la clave principal sea EXACTAMENTE 'Educacion'. "
    "El valor de esta clave debe ser una lista de objetos, donde cada uno represente un estudio con: "
    "'title' (grado/título), 'institution' (universidad/centro), 'place' (lugar) y 'time' (fecha/años). "
    "No inventes información."
)

# Instrucciones para Biografía y Polémicas (Texto plano)
TEXT_CATEGORY_INSTRUCTIONS = (
    "Genera un resumen en texto coherente, detallado."
)

def extract_candidate_category_info(text, candidate, category, category_instructions):
    if not text:
        return {
            "content": "not_found",
            "ref": [{"quote": "not_found", "link": "not_found"}]
        }

    # 1. Esquema de Referencias (Común para todos)
    ref_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "quote": {"type": "string"},
                "link": {"type": "string"},
                "category": {"type": "string"}
            },
            "required": ["quote", "link"]
        }
    }

    # 2. Lógica para definir el esquema de 'content' basado en la categoría
    if category == "Experiencia Laboral":
        content_schema = {
            "type": "object",
            "properties": {
                "Experiencia Laboral": { 
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "institution": {"type": "string"},
                            "place": {"type": "string"},
                            "time": {"type": "string"}
                        },
                        "required": ["title", "institution", "time"]
                    }
                }
            },
            "required": ["Experiencia Laboral"]
        }

    elif category == "Educacion":
        content_schema = {
            "type": "object",
            "properties": {
                "Educacion": { 
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            # Nota: Usamos 'title' para mantener consistencia, 
                            # o puedes cambiarlo a 'degree' si prefieres, 
                            # pero el prompt de arriba pide 'title'.
                            "title": {"type": "string"}, 
                            "institution": {"type": "string"},
                            "place": {"type": "string"},
                            "time": {"type": "string"}
                        },
                        "required": ["title", "institution", "time"]
                    }
                }
            },
            "required": ["Educacion"]
        }

    else:
        # Caso para "Polemicas" y "Biografia" (Texto plano)
        content_schema = {"type": "string"}

    # 3. Esquema Final
    final_schema = {
        "type": "object",
        "properties": {
            "content": content_schema,
            "ref": ref_schema
        },
        "required": ["content", "ref"]
    }

    prompt = f"""
    Eres un analista experto.
    Tarea: Extraer información del candidato **{candidate}** para la categoría **{category}** esta tendra que ser utilizada en el ref.
    E
    
    Instrucciones específicas: {category_instructions}
    
    Texto fuente:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-pro", 
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": final_schema
        },
    )

    result = response.parsed

    if result:
        return result

    return {
        "content": "not_found",
        "ref": [{"quote": "not_found", "link": "not_found"}]
    }


def verify_credibility(google_search_response):
    invalid_domains = ["facebook.com", "x.com", "youtube.com", "instagram.com", "tiktok.com"]
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

        results = data.get("organic", None)
        if results and len(results) == 0 and i <len(categories[category])-1:
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
        query = sql.SQL(f"SELECT id, name FROM candidate_data.candidate_info ORDER BY id asc")
        cur.execute(query)

        candidates = cur.fetchall()
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

def process_candidate_category(candidate_id, candidate_name, category, category_instructions=None):
    print(f"\n--- Processing {candidate_name} | Category: {category} ---")

    #Search links
    results = get_category_links(candidate_name, category)
    if not results:
        print("No search results.")
        return

    # remove domains 
    credible_links = verify_credibility(results)

    # get text
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
        
        insert_content(final, candidate_id, category)
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
    limited_sources,
    candidate_name,
    category,
    category_instructions
)
    # Safety fallback
    if not extracted:
        extracted = {
            "content": "not_found",
            "ref": [{"quote": "not_found", "link": "not_found"}]
        }
    # insert results into DB
    insert_content(extracted, candidate_id, category)
    return extracted.get("ref")



def insert_content(content, candidate_id, category):
    # 'content' es el resultado completo del extractor
    new_content = content.get("content")
    
    column_map = {
        "Polemicas": "polemicas",
        "Biografia": "summary",
        "Experiencia Laboral": "work_experience_2",
        "Educacion": "education_1",
    }

    column_name = column_map.get(category)
    if not column_name:
        return {"status": "error", "message": f"Categoría desconocida: {category}"}

    # --- Adaptación del Contenido usando psycopg2.extras.Json ---
    
    if isinstance(new_content, dict):
        # Para Experiencia Laboral y Educación, que son objetos Python (JSON estructurado),
        # envolvemos el contenido con Json() para un manejo seguro.
        data_to_insert = Json(new_content)
    else:
        # Para Polémicas y Biografía (texto), se inserta como una cadena normal.
        data_to_insert = new_content
        
    # -----------------------------------------------------------

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        # El SQL se simplifica, ya que psycopg2.extras.Json se encarga de la serialización
        # y la indicación del tipo.
        sql = f"""
            UPDATE candidate_data.candidate_info
            SET {column_name} = %s
            WHERE id = %s
        """

        cur.execute(sql, (
            data_to_insert, # Aquí se inserta el Json(obj) o el string
            candidate_id
        ))

        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": f"Contenido de {category} insertado para el candidato {candidate_id}"}


    except Exception as e:
        # En caso de error, siempre es bueno hacer rollback si la conexión sigue abierta
        if conn:
            conn.rollback()
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
    categories = ["Experiencia Laboral", "Educacion", "Polemicas", "Biografia" ]

    additional_instructions = {
        "Experiencia Laboral": WORKEXP_INSTRUCTIONS,
        "Educacion": EDUCATION_INSTRUCTIONS
    }

    for candidate_id, candidate_name in candidates:
        all_refs = []

        if candidate_name == "Pendiente":
            continue

        for category in categories:
            category_instructions = additional_instructions.get(category, "")

            used_refs = process_candidate_category(
                candidate_id,
                candidate_name,
                category,
                category_instructions
            )

            if used_refs:
                all_refs.extend(used_refs)

        update_refs(candidate_id, all_refs)



if __name__ == "__main__":
    main()

