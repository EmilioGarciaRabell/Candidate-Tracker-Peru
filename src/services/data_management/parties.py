from src.services.db.db_manager import Database 


PARTIES_TABLE = Database(table="candidate_data.parties")
def get_all_parties():
    return PARTIES_TABLE.select('*')

def get_party_by_id(id):
    return PARTIES_TABLE.select('*', f"id = {id}")[0]
    
