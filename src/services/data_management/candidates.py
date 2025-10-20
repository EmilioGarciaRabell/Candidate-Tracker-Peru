from src.services.db.db_manager import Database 


CANDIDATES_TABLE = Database(table="candidate_data.candidate_info")
PARTIES_TABLE = Database(table="candidate_data.parties")

def get_candidates() -> list[dict]:
    """ get all candidates """
    return CANDIDATES_TABLE.get_candidates_with_parties()


def get_candidate(id) -> dict:
    """ get candidate from id """
    candidate = CANDIDATES_TABLE.select('*', f"id = {id}")[0]
    candidate["party_id"] = PARTIES_TABLE.select("name", f"id = {candidate.get('party_id')}")[0].get("name")
    return candidate

##ERROR psycopg2.errors.UndefinedColumn: column "none" does not exist
##LINE 1: SELECT name FROM candidate_data.parties WHERE id = None
##HINT:  Perhaps you meant to reference the column "parties.name".