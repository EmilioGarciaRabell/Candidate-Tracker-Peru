from src.services.db.db_manager import Database 


SM_TABLE = Database(table="candidate_data.social_media")

def get_social_media(id: int) -> dict | None:
    rows = SM_TABLE.select("*", "candidate_id = %s", params=(id,))
    return rows[0] if rows else None
