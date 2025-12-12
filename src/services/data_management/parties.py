from src.services.db.db_manager import Database

PARTIES_TABLE = Database(table="candidate_data.parties")

def get_all_parties():
    return PARTIES_TABLE.select("*")

def get_party_by_id(id: int):
    rows = PARTIES_TABLE.select(
        "*",
        "id = %s",
        params=(id,)
    )
    if not rows:
        return None  # or raise error
    return rows[0]
