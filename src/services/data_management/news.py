import json
from flask import jsonify
from pydantic import Json
from src.services.db.db_manager import Database 
from unidecode import unidecode

NEWS_TABLE = Database(table="candidate_data.all_news")
CANDIDATE_TABLE = Database(table="candidate_data.candidate_info")
BATCH_TABLE = Database(table="candidate_data.news_batch")
##Functionality to get all news
def retrieve_results(batch_time):
    conn = NEWS_TABLE._get_conn()
    query = """
        select  * from candidate_data.all_news
        where fetch_data::time BETWEEN (%s) and (%s)
        and fetch_data::date = CURRENT_DATE - 7
    """
    interval1 = ''
    interval2 = ''
    if batch_time == 'morning':
        interval1 = '7:00'
        interval2 = '8:00'
    elif batch_time == 'evening':
        interval1 = '19:00'
        interval2 = '20:00' 
    else:
         interval1 = 'batch_not_found'
         interval2 = 'batch_not_found'
    try:
        with conn.cursor() as cur:
                cur.execute(query,(interval1,interval2))
                colnames = [c[0] for c in cur.description]
                return [dict(zip(colnames, r)) for r in cur.fetchall()]
    finally:
            NEWS_TABLE._release_conn(conn)


def remove_accents(list):
    result = []
    for i in list:
        result.append(unidecode(i).lower())
    return result   

def store_candidates_news(batch_time):
    news = retrieve_results(batch_time)
    candidates = CANDIDATE_TABLE.select(["id","name"])
    result = []
    for candidate in candidates:
        candidate_news = {      
            "id": candidate["id"],
            "news": []
        }
        for n in news:
            if n is not None and n["keywords"] is not None:
                clean_keywords = remove_accents(n["keywords"])
                if unidecode(candidate["name"].lower()) in clean_keywords or unidecode(candidate["name"].lower()) in unidecode(n["title"].lower()):
                    candidate_news["news"].append({"title": n["title"],"link": n["link"],"keywords":n["keywords"]})
        result.append(candidate_news)
    
    conn = BATCH_TABLE._get_conn()
    query = """
        INSERT INTO candidate_data.news_batch(batch,news_json)
        VALUES (%s,%s)
        """
    try:
        with conn.cursor() as cur:
                cur.execute(query,(batch_time, json.dumps({"news": result})))
                conn.commit()
    finally:
            BATCH_TABLE._release_conn(conn)
    return result

def get_news(batch_time):
    return BATCH_TABLE.select("news_json",f"batch = {batch_time}")


     
