from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import re 
import trafilatura


load_dotenv()

def get_candidate_bio_web(name,num_results):
    params = {
        "engine": "google",
        "q": f"infogob {name}",
        "num": num_results,
        "api_key": os.environ.get("SERAPI")
    }
    search = GoogleSearch(params)
    res = search.get_dict()
    return res.get("organic_results", [])

def verify_credibility(google_search_response):
    invalid_links = ["facebook.com","x.com","youtube.com","en.wikipedia.org","instagram.com","tiktok.com"]
    filtered_results = []
    for r in google_search_response:
        keep = True  
        for domain in invalid_links:
            if domain in r["link"]:
                keep = False 
                break 
        if keep:
            filtered_results.append(r["link"])
    return filtered_results

    ##check that the sources end in .org, or is from one of the reliable news outlets


def extract_main_text(url):
    fetch_u = trafilatura.fetch_url(url)
    result = trafilatura.extract(fetch_u)
    keywords = [
        "nació en", "fecha de nacimiento", "lugar de nacimiento",
        "edad", "origen", "nacionalidad", "biografía", "infancia", "juventud",
        "vida temprana", "familia", "padres", "hermanos", "hijos",
        "estudió en", "graduado de", "título en", "universidad", "escuela",
        "educación", "formación profesional", "licenciado en", "doctor en",
        "trabajó en", "se desempeñó como", "ocupó el cargo de", "fundador de",
        "carrera", "trayectoria", "premio", "reconocido por", "aportaciones",
        "falleció", "murió", "fecha de muerte", "vida personal", "perfil personal", "quien es"
    ]
    if result is not None:
        count = 0
        for i in keywords:
            if i in result.lower():
                count += 1
        
        if count >= 3:
            return result
        

result = get_candidate_bio_web("Emiliano Vargas Florecin",10)
print(result)
# clean_link = verify_credibility(result)
# print(clean_link)
# for i in clean_link:
#     print(extract_main_text(i))
## websites: infobae, elcomercio, newyorktimes, economist, rpp, tvperunoticias

##issues: add name of party

##use search api to get biography or use the news api and search if there are any news about the candidates biography