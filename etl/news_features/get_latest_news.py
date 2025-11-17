import time
from dotenv import load_dotenv
import psycopg2
load_dotenv()
import os
import requests
import json
from psycopg2 import sql
from datetime import datetime
from unidecode import unidecode
from datetime import time
from src.services.data_management import news


NEWS_API = os.environ.get("CARLA_API")
api_url = f"https://newsdata.io/api/1/latest?country=PE&apikey={NEWS_API}"


def get_all_news():
    try:
        response = requests.get(api_url)
        results = []
        if response.status_code == 200:
            page_count = 1
            data = response.json()
            results.extend(data["results"])
            nextPage = data["nextPage"]

            while nextPage is not None:
                page_count +=1  
                if page_count >= 75:
                    break
                new_url = api_url + f"&page={nextPage}"
                response = requests.get(new_url)
                if response.status_code == 200:
                    data = response.json()
                    results.extend(data.get("results", []))
                    nextPage = data.get("nextPage")
                else:
                    print("error while loading")
                    break
                time.sleep(1)
        return results
    except Exception as e:
        print("Error:", e) 

def get_all(item):
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        select_query = ""
        if item == "candidate":
            select_query = sql.SQL("""
                SELECT id,name from candidate_data.candidate_info
            """)

        elif item == "parties":
            select_query = sql.SQL("""
                SELECT id,name from candidate_data.parties
            """)
        else:
            return None
        cur.execute(
            select_query
        )
        list_of_tuples = cur.fetchall()
        
        conn.commit()
        cur.close()
        conn.close()
        return list_of_tuples

    except Exception as e:
        print("Error getting select statements:", e)
        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return None

def database_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None
    conn = psycopg2.connect(database_url)

    return conn



def call_api_store_initial_news():
    news = get_all_news()
    ##start database connection
    conn = database_connection()
    cur = conn.cursor()
    
    current_time = datetime.now()
    ##for each news form the structure of the table
    ##get article_id, title, link, keywords, fetch_data
    
    try:
        for n in news:
            sql_query = sql.SQL("""
                INSERT INTO candidate_data.all_news(id,title,link,keywords,fetch_data)
                VALUES(%s, %s, %s,%s, %s)
                RETURNING id;                   
                """)
            cur.execute(sql_query,(n["article_id"], n["title"], n["link"],n["keywords"],current_time))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Error getting select statements:", e)
        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return None


def get_news_from_db(slot):
    query = """
        select  * from candidate_data.all_news
        where fetch_data::time BETWEEN (%s) and (%s)
        and fetch_data::date = CURRENT_DATE -1
    """
    interval1 = ''
    interval2 = ''
    if slot == 'morning':
        interval1 = '7:00'
        interval2 = '8:00'
    elif slot == 'evening':
        interval1 = '13:00'
        interval2 = '14:00'
    
    conn = database_connection()
    cur = conn.cursor()

    try:
        news = cur.fetchall(query,(interval1,interval2))
        conn.commit()
        cur.close()
        conn.close()

        return news
    except Exception as e:
        print("Error getting select statements:", e)
        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return None  


def retrieve_results(batch_time):
    conn = database_connection()
    cur = conn.cursor()
    query = """
        select  * from candidate_data.all_news
        where fetch_data::time BETWEEN (%s) and (%s)
        and fetch_data::date = CURRENT_DATE - 4
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
    
    print(interval1)
    print(interval2)

    try:
        with conn.cursor() as cur:
                cur.execute(query,(interval1,interval2,))
                colnames = [c[0] for c in cur.description]
                return [dict(zip(colnames, r)) for r in cur.fetchall()]
    finally:
            cur.close()
            conn.close()
    
def remove_accents(list):
    result = []
    for i in list:
        result.append(unidecode(i).lower())
    return result   

# print(remove_accents(['espectáculos']))

def get_candidate_news(batch_time):
    conn = database_connection()
    cur = conn.cursor()
    news = retrieve_results(batch_time)
    candidates = get_all("candidate")   
    result = []
    for candidate in candidates:
        candidate_news = {      
            "id": candidate[0],
            "news": []
        }
        for n in news:
            if n is not None and n["keywords"] is not None:
                clean_keywords = remove_accents(n["keywords"])
                if unidecode(candidate[1].lower()) in clean_keywords or unidecode(candidate[1].lower()) in unidecode(n["title"].lower()):
                    candidate_news["news"].append({"title": n["title"],"link": n["link"],"keywords":n["keywords"]})
        result.append(candidate_news)

    query = """
    TRUNCATE TABLE candidate_data.all_news
    """
    try:
        if batch_time == "afternoon":
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
    finally:
            cur.close()
            conn.close()


def get_day_period(t: time) -> str:
    """Return 'morning' if before 12 PM, otherwise 'evening'."""
    return "morning" if t.hour < 12 else "evening"

def main():
    batch_time = get_day_period(datetime.now().time())
    get_candidate_news(batch_time)
    news.store_candidates_news(batch_time)
    

if __name__ == "__main__":
    main()