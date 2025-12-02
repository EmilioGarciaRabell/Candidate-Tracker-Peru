from src.services.db.db_manager import Database 


SENTIMENT_TABLE = Database(table="candidate_data.sentiment_analysis")

def get_candidate_sentiment(id) -> dict:
    """ get candidate from id """
    sentiment = SENTIMENT_TABLE.select('*', f"candidate_id = {id}")[0]
    return sentiment