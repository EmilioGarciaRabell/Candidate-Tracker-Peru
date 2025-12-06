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
from psycopg2.extras import Json



NEWS_API = os.environ.get("CARLA_API")
api_url = f"https://newsdata.io/api/1/archive?country=PE&apikey={NEWS_API}"

def database_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None
    conn = psycopg2.connect(database_url)

    return conn

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
                SELECT * from candidate_data.candidate_info
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


def retrieve_results():
    conn = database_connection()
    query = """
        select  * from candidate_data.all_news
    """
    try:
        with conn.cursor() as cur:
                cur.execute(query)
                colnames = [c[0] for c in cur.description]
                return [dict(zip(colnames, r)) for r in cur.fetchall()]
    except Exception as e:
        print("Error getting select statements:", e)
        if conn:
            conn.rollback()
        if cur:
            cur.close()
        if conn:
            conn.close()
        return None  


def remove_accents(list):
    result = []
    for i in list:
        result.append(unidecode(i).lower())
    return result  


def tokenize_name(names,nicknames, keywords):    
    for n in names:
        n_tokens = unidecode(n.lower()).split()

        for k in keywords:
            k_token = unidecode(k.lower()).split()

            for nick in nicknames:
                if not nick.strip():  # skip empty nicknames
                    continue
                nick_token = unidecode(nick.lower()).split()

                ##check if all nicknames are in keywords
                count = 0
                for token in nick_token:
                    if token in k_token:
                        count +=1
                if count == len(nick_token):
                    return True
                
            all_keyword_tokens = 0
            for k_tok in k_token:
                if k_tok in n_tokens:
                    all_keyword_tokens +=1
            if all_keyword_tokens == len(k_token):
                return True
            
    return False


##script that will run every 7 days (sunday)
def store_candidates_news():
    conn = database_connection()
    news = retrieve_results()
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
                if tokenize_name(candidate[1],candidate[9],clean_keywords):
                    candidate_news["news"].append({"title": n["title"],"link": n["link"],"keywords":n["keywords"]})
        result.append(candidate_news)
    
    current_time = datetime.now().date()
    query = """
        INSERT INTO candidate_data.news_batch(news_json,date_time)
        VALUES (%s,%s)
        """
    query2 = """
        INSERT INTO candidate_data.past_news
        SELECT * FROM candidate_data.all_news
        """
    
    query3 = """
        truncate table candidate_data.all_news
        """
    try:
        with conn.cursor() as cur:
                cur.execute(query,( Json(result) , current_time))
                cur.execute(query2)
                cur.execute(query3)
                conn.commit()
    finally:
            cur.close()
            conn.close()
    return result


def news_daily_script():
    print("Running news daily script...")
    call_api_store_initial_news()
    print("news daily script done")

def news_weekly_srcipt():
    print("Running weekly script...")
    store_candidates_news()
    print("Weekly script done")


if __name__ == "__main__":
    news_weekly_srcipt()


