from src.services.db.db_manager import Database 


CANDIDATES_TABLE = Database(table="candidate_data.candidate_info")
PARTIES_TABLE = Database(table="candidate_data.parties")

def get_candidates() -> list[dict]:
    """ get all candidates """
    return CANDIDATES_TABLE.get_candidates_with_parties()


def get_candidate(id: int) -> dict:
    rows = CANDIDATES_TABLE.select(
        'id, name, age, party_id, education, summary, work_experience, polemicas, ref',
        "id = %s",
        params=(id,),
    )
    if not rows:
        raise KeyError(f"Candidate {id} not found")

    candidate = rows[0]
    party_rows = PARTIES_TABLE.select("name", "id = %s", params=(candidate.get("party_id"),))
    if party_rows:
        candidate["party_id"] = party_rows[0].get("name")

    return candidate


