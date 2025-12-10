
from unidecode import unidecode
import csv 
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
        ##check if all nickname in tokens
        ##check all keyword tokens in full name tokens

# Example usage
# candidates = ["Rosario del Pilar Fernández Bazán"]
# nick_names = ["Rosario Fernandez"]
# keywords = ["flamengo celebraciones", "río", "flamengo"]


# if tokenize_name(candidates,nick_names, keywords):
#     print("Candidate mentioned!") 
          

def database_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL not found in environment")
        return None
    conn = psycopg2.connect(database_url)

    return conn

def read_csv():
    conn = database_connection()
    cur = conn.cursor()

    try:
        with open('/Users/carlalopez/Candidate-Tracker-Peru/etl/news_features/data.csv', newline='') as csvfile:
            r = csv.reader(csvfile, delimiter=',')
            header = next(r)
            print(header)
            # print(header[0],header[1])
            for row in r:
                id_val = int(row[0])
                nick_val = row[8].split("|")
                nick_val = [x.strip('"') for x in nick_val]
                print(nick_val)

                sql_query = """
                    UPDATE candidate_data.candidate_infO
                    SET nicknames = (%s)
                    WHERE id = (%s)
                """
                cur.execute(sql_query, (nick_val,id_val))

                conn.commit()

    except Exception as e:
            print("Error getting select statements:", e)
            if conn:
                conn.rollback()
            if cur:
                cur.close()
            if conn:
                conn.close()
            return None




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
    
