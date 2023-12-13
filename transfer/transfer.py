import requests

BACKEND_NETLOC = "localhost:8000"
PATH_PREFIX = "/api/v1"


def post_raw_news_list(raw_news_list):
    url = f"http://{BACKEND_NETLOC}{PATH_PREFIX}/raw_news_list"
    response = requests.post(url, json=raw_news_list)
    return response
