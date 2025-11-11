from google import genai
import wikipediaapi
import os
from dotenv import load_dotenv
load_dotenv()

# --- Setup ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# --- Wikipedia Helper ---
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

    return page.text, page.fullurl


# --- Gemini Structured Extraction ---
def extract_candidate_info(name: str):
    text, url = get_wikipedia_page(name)
    if not text:
        return {"error": f"No se encontró la página de Wikipedia para '{name}'."}

    schema = {
        "type": "object",
        "properties": {
            "age": {"type": "string"},
            "education": {"type": "string"},
            "summary": {"type": "string"},
            "ref": {"type": "array", "items": {"type": "string"}},
            "controversies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "ref": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            "accomplishments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "ref": {"type": "array", "items": {"type": "string"}}
                    }
                }
            }
        },
        "required": ["age","education", "summary", "ref"]
    }

    prompt = f"""
    Eres un analista experto en política peruana.
    Lee la siguiente información de Wikipedia (en español) sobre el candidato "{name}".
    Extrae los datos clave en formato JSON según el esquema dado.

    Si alguna sección no tiene información disponible, deja el campo vacío o una lista vacía.
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

# --- Example ---
if __name__ == "__main__":
    print(get_wikipedia_page("Rafael López Aliaga"))
