from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json


NEWS_API = os.environ.get("CARLA_API")
api_url = f"https://newsdata.io/api/1/latest?country=pe&apikey={NEWS_API}"

##Note: There is a next page keyword that contains the parameter that needs to be added to the URL
## We need send a request to the API until nextPage is null or define a number (10 )

def get_news_srcs():
    response = requests.get(api_url)
    if response.status_code == 200:
        dic = response.json()
    else:
        print("not found")

def get_all_news():
    next_page = ""
    all_news = []
    i = 0
    while next_page is not None:
        if next_page == "":
            new_url = api_url
        else:
            new_url = api_url + "&page=" + next_page
        response = requests.get(new_url)

        if response.status_code == 200:
            response = response.json()
            all_news.append(response)
            next_page = response["nextPage"]
        else:
            print("url not found")
        i+=1
    
    for i in all_news:
        print(i["nextPage"])


get_all_news()

