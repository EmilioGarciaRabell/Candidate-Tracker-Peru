from src.services.db.db_manager import Database 

SENTIMENT_TABLE = Database(table="candidate_data.sentiment_analysis")

def get_candidate_sentiment(id: int) -> dict | None:
    rows = SENTIMENT_TABLE.select(
        "*",
        "candidate_id = %s",
        params=(id,)
    )

    if not rows:
        return None  # or if you prefer: return {} or raise custom error

    return rows[0]
