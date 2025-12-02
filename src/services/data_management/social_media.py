from src.services.db.db_manager import Database 


SM_TABLE = Database(table="candidate_data.social_media")

def get_social_media(id) -> dict:
    """ get social media from candidate id """
    sm = SM_TABLE.select('*', f"candidate_id = {id}")[0]
    return sm