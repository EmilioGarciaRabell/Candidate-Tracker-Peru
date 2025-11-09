import wptools
import re
import html
from datetime import datetime

# Silence wptools logs
wptools.debug = 0

def clean_text(text):
    if not text:
        return None
    text = html.unescape(text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text if text else None

def calculate_age(birth_date_str):
    try:
        match = re.search(r"(\d{4})-(\d{2})-(\d{2})", birth_date_str)
        if not match:
            return None
        year, month, day = map(int, match.groups())
        today = datetime.now()
        return today.year - year - ((today.month, today.day) < (month, day))
    except Exception:
        return None

def get_claim_label(claim):
    if isinstance(claim, list) and len(claim) > 0:
        c = claim[0]
        return c.get('label') or c.get('value')
    elif isinstance(claim, dict):
        return claim.get('label') or claim.get('value')
    return None

def extract_section_snippets(text, keywords):
    """Find short relevant sections from text given keyword list."""
    snippets = []
    if not text:
        return snippets
    paragraphs = re.split(r"(?=<p>)", text)
    for p in paragraphs:
        plain = clean_text(p)
        if plain and any(k.lower() in plain.lower() for k in keywords):
            snippets.append({
                "summary": plain,
                "dates": "",
                "source": ""
            })
    return snippets

def get_candidate_info_es(name):
    page = wptools.page(name, lang="es", silent=True)
    page.get_query()
    page.get_parse()
    page.get_wikidata()

    data = page.data
    wikidata = data.get("wikidata", {})
    claims = wikidata.get("claims", {})

    # --- Base structure ---
    candidate = {
        "name": name,
        "party": None,
        "age": None,
        "education": None,
        "summary": None,
        "ref": [data.get("url")],
        "controversies": [],
        "accomplishments": []
    }

    # --- Wikidata structured fields ---
    party_claim = claims.get("P102")  # political party
    edu_claim = claims.get("P69")     # educated at
    birth_claim = claims.get("P569")  # date of birth

    if party_claim:
        candidate["party"] = get_claim_label(party_claim)
    if edu_claim:
        candidate["education"] = get_claim_label(edu_claim)
    if birth_claim:
        birth_value = get_claim_label(birth_claim)
        candidate["age"] = calculate_age(birth_value)

    # --- Summary ---
    candidate["summary"] = clean_text(
        data.get("exrest")
        or data.get("extract")
        or data.get("description")
    )

    # --- Extract controversies & accomplishments ---
    text = data.get("extract", "")
    controversies = extract_section_snippets(
        text, ["corrupción", "escándalo", "acusación", "controversia", "delito", "blanqueo"]
    )
    accomplishments = extract_section_snippets(
        text, ["fue elegida", "fue elegido", "premio", "logró", "reconocido", "reconocida", "fundó", "dirigió"]
    )

    # Assign sources
    for c in controversies + accomplishments:
        c["source"] = data.get("url")

    candidate["controversies"] = controversies
    candidate["accomplishments"] = accomplishments

    return candidate

# Example usage
if __name__ == "__main__":
    info = get_candidate_info_es("Keiko Fujimori")
    from pprint import pprint
    pprint(info)
