import os
from google import genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TODAY_STR = datetime.today().strftime("%d/%m/%Y")

def get_sentiment_summary(candidate, sentiment, posts_info):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # We'll only ask Gemini to produce title, summary, and content.
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["title", "summary", "content"]
    }

    prompt = f"""
    Eres un analista político experto en opinión pública y tendencias electorales.
    Analiza los datos de sentimiento en redes sociales sobre el candidato "{candidate}"
    durante las elecciones peruanas de 2026. 

    ### Objetivo:
    Genera un análisis textual con el siguiente formato:
    {{
      "title": título corto del hallazgo principal (máx. 10 palabras) agrega la fecha exacta aqui, hoy es {TODAY_STR},
      "summary": resumen conciso del sentimiento general (2-3 oraciones),
      "content": análisis detallado y objetivo (máx. 200 palabras)
    }}

    ### Instrucciones:
    - Usa solo el idioma español.
    - No inventes cifras, usa únicamente la información proporcionada.
    - Mantén un tono analítico, neutral y claro.
    - Evita adjetivos valorativos o juicios personales.

    ### Datos:
    Candidato: {candidate}

    Sentimiento general (usado solo como contexto):
    {sentiment}

    Publicaciones analizadas:
    {posts_info}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema
        }
    )

    text_result = getattr(response, "parsed", None) or response.text

    # Combine Gemini’s structured output with your sentiment numbers
    return {
        "negative": sentiment["negative"],
        "positive": sentiment["positive"],
        "neutral": sentiment["neutral"],
        "title": text_result.get("title", "") if isinstance(text_result, dict) else "",
        "summary": text_result.get("summary", "") if isinstance(text_result, dict) else "",
        "content": text_result.get("content", "") if isinstance(text_result, dict) else ""
    }
