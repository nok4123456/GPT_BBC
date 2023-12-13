# %%

from scraping.scraping_BBC import main as scraping_BBC
from transfer.transfer import post_raw_news_list
from result import Ok, Err, is_err
import pendulum
import json


def main():
    result = scraping_BBC()
    if is_err(result):
        print(result.err)
        return Err(result.err)
    raw_news_list = result.ok_value
    data_dict = {
        "raw_news_list": raw_news_list,
        "date": pendulum.now().to_date_string(),
        "published_by": "BBC",
    }

    try:
        response = post_raw_news_list(data_dict)
        if response.status_code != 200:
            return Err("response.status_code != 200 :" + response.text)
        return Ok(response.text)
    except Exception as e:
        print("Error in transfering data to server :" + str(e))
        return Err(e)


if __name__ == "__main__":
    res = main()
    print(res)
# %%
