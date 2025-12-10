import os
import re
import unicodedata
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

BASE_URL = "https://es.wikipedia.org/wiki/Elecciones_generales_de_Per%C3%BA_de_2026"

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


def clean_text(text):
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def clean_summary(summary):
    if not summary:
        return summary
    summary = re.sub(r"\[\s*\d+\s*\]", "", summary)  # Remove references like [1], [ 2 ]
    summary = re.sub(r"\s{2,}", " ", summary).strip()
    return summary


def get_candidates():
    # request setup
    html = fetch_page(BASE_URL)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"class": "wikitable"})
    if not table:
        raise Exception("No se encontró la tabla de candidatos.")

    candidates = []
    # get all the tr tags
    for row in table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if not cols:
            continue

        candidato_cell = cols[1] if len(cols) >= 4 else cols[0]
        link_tag = candidato_cell.find("a", href=True)
        wiki_link = (
            f"https://es.wikipedia.org{link_tag['href']}"
            if link_tag and link_tag["href"].startswith("/wiki/")
            else None
        )
        candidato = clean_text(candidato_cell.get_text())
        # if there is a canditate return the candidate with the assigned link
        if candidato:
            candidates.append({"candidato": candidato, "wiki_link": wiki_link})

    return candidates


def get_candidate_info(wiki_link):
    """Retunr the candidate name, age, summary, political party, education, and reference link from wikipedia"""
    if not wiki_link:
        return {
            "name": "not_found",
            "age": -1,
            "summary": "not_found",
            "partido_politico": "not_found",
            "educacion": "not_found",
            "ref": "No link found",
        }

    try:
        html = fetch_page(wiki_link, headers={"User-Agent": HEADERS["User-Agent"]})
    except requests.RequestException:
        return {
            "name": "not_found",
            "age": -1,
            "summary": "not_found",
            "partido_politico": "not_found",
            "educacion": "not_found",
            "ref": "Request failed",
        }

    soup = BeautifulSoup(html, "html.parser")

    # Name
    name_tag = soup.find("caption") or soup.find("th", {"class": "infobox-above"})
    if name_tag:
        name = clean_text(name_tag.get_text(" ", strip=True))
    else:
        heading = soup.find("h1", {"id": "firstHeading"})
        name = clean_text(heading.get_text(strip=True)) if heading else "not_found"

    # Age
    age = -1
    birth_row = soup.find("th", string=lambda t: t and "Nacimiento" in t)
    if birth_row:
        birth_td = birth_row.find_next("td")
        if birth_td:
            match = re.search(r"\((\d+)\s*años", birth_td.get_text(" ", strip=True))
            if match:
                age = int(match.group(1))

    # Summary
    first_p = soup.select_one("p")
    summary = clean_summary(clean_text(first_p.get_text(" ", strip=True))) if first_p else "not_found"

    # Party
    partido = "not_found"
    partido_cell = soup.find("th", string=lambda t: t and ("Partido político" in t or "Partido" in t))
    if partido_cell:
        td = partido_cell.find_next("td")
        if td:
            for sup in td.find_all("sup"):
                sup.decompose()
            partido = clean_text(td.get_text(" ", strip=True)) or "not_found"

    # Education
    educacion = "not_found"
    edu_labels = ["Educación", "Formación", "Alma máter", "Universidad", "Estudios"]
    for label in edu_labels:
        edu_cell = soup.find("th", string=lambda t: t and label in t)
        if edu_cell:
            td = edu_cell.find_next("td")
            if td:
                for sup in td.find_all("sup"):
                    sup.decompose()
                educacion = clean_text(td.get_text(" ", strip=True)) or "not_found"
            break
    
     # Image
    image_path = None
    img_tag = soup.select_one(".infobox img")
    if img_tag and img_tag.get("src"):
        img_url = img_tag["src"]
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        os.makedirs("etl/candidates/data/images", exist_ok=True)
        safe_name = unicodedata.normalize('NFKD', name or 'unknown')
        safe_name = safe_name.encode('ascii', 'ignore').decode('ascii') 
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', safe_name)
        filename = f"{safe_name}.jpg"
        local_path = os.path.join("etl/candidates/images", filename)

        try:
            img_data = requests.get(img_url, headers=HEADERS, timeout=8).content
            with open(local_path, "wb") as f:
                f.write(img_data)
            image_path = local_path
        except Exception:
            image_path = None

    return {
        "name": name,
        "age": age,
        "summary": summary,
        "partido_politico": partido,
        "educacion": educacion,
        "ref": wiki_link or "not_found",
    }


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


def clean_data(data, parties_names):

    name = data.get("name", "")
    summary = data.get("summary", "")

    if not name or name.lower().startswith(("archivo", "venceremos")):
        return
    if any(name.lower().startswith(p.lower()) for p in parties_names):
        return
    # if len(name.split()) < 2 and not summary:
    #     return
    if any(x in summary.lower() for x in ["haz clic", "creativecommons", "logo", "publicdomain"]):
        return
    
    return data


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
            candidate_dict.get("name", "not_found"),
            candidate_dict.get("age", -1),
            candidate_dict.get("partido_politico", "not_found"),
            candidate_dict.get("educacion", "not_found"),
            candidate_dict.get("summary", "not_found"),
            candidate_dict.get("ref", "not_found")
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

    for row in raw_candidates:
        # get the information about the candidate from wikipedia
        candidate_info = get_candidate_info(row["wiki_link"])
        # clean the party field
        clean_partido = re.sub(r"\s*\(.*?\)\s*$", "", candidate_info.get("partido_politico", "")).lower()
        # assign the party id to the candidate 
        candidate_info["partido_politico"] = parties.get(clean_partido, None)
        
        candidate_info = clean_data(candidate_info, parties_names)

        candidates.append(candidate_info)
        # Insert candidate into table
        print(candidate_info)
        #if candidate_info: insert_into_table(candidate_info)

if __name__ == "__main__":
    main()

