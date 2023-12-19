import requests

BACKEND_NETLOC = "localhost:8000"
PATH_PREFIX = "/api/v1"


def post_raw_news_list(raw_news_list) -> requests.Response:
    url = f"http://{BACKEND_NETLOC}{PATH_PREFIX}/raw_news_list"
    response = requests.post(url, json=raw_news_list)
    return response


def get_raw_news_list_by_date(date: str) -> requests.Response:
    url = f"http://{BACKEND_NETLOC}{PATH_PREFIX}/raw_news_list"
    response = requests.get(url, params={"date": date})
    return response


def post_transformed_news_list(transformed_news_list) -> requests.Response:
    url = f"http://{BACKEND_NETLOC}{PATH_PREFIX}/transformed_news_list"
    response = requests.post(url, json=transformed_news_list)
    return response
