# %%

from transfer.transfer import get_raw_news_list_by_date
from result import Ok, Err, is_err, Result
from transform.transform_new import transform_raw_news_into_transformed_news
import pendulum


def transform_job() -> Result[str, str]:
    now_date_str = pendulum.now().strftime("%Y-%m-%d")
    raw_news_list_response = get_raw_news_list_by_date(now_date_str)
    if raw_news_list_response.status_code != 200:
        return Err("response.status_code != 200 :" + raw_news_list_response.text)
    raw_news_list = raw_news_list_response.json()["data"]["raw_news_list"]
    transformed_news_list_result = transform_raw_news_into_transformed_news(
        raw_news_list
    )
    return Ok("ok")


if __name__ == "__main__":
    transform_job()
# %%
