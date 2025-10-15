import time
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json


NEWS_API = os.environ.get("CARLA_API")
api_url = f"https://newsdata.io/api/1/latest?country=pe&apikey={NEWS_API}"


def get_news_srcs():
    response = requests.get(api_url)
    results = []
    print(response)
    if response.status_code == 200:
        data = response.json()
        results.extend(data.get("results", []))
        nextPage = data.get("nextPage")
        print(nextPage)
    else:
        print("not found")


def get_all_news():
    response = requests.get(api_url)
    results = []
    if response.status_code == 200:
        page_count = 1
        data = response.json()
        results.append(data["results"])
        nextPage = data["nextPage"]

        while nextPage is not None:
            page_count +=1
            
            if page_count >= 20:
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

    print(len(results))

get_all_news()

