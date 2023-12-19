# %%

from transfer.transfer import get_raw_news_list_by_date, post_transformed_news_list
from result import Ok, Err, is_err, Result
from transform.transform_new import transform_raw_news_into_transformed_news
import pendulum


def transform_job() -> Result[str, str]:
    now_date_str = pendulum.now().strftime("%Y-%m-%d")

    raw_news_list_response = get_raw_news_list_by_date(now_date_str)
    if raw_news_list_response.status_code != 200:
        return Err("response.status_code != 200 :" + raw_news_list_response.text)

    raw_news_list = raw_news_list_response.json()["data"]["raw_news_list"]
    publisher_str = raw_news_list_response.json()["data"]["published_by"]
    transformed_news_list_result = transform_raw_news_into_transformed_news(
        raw_news_list
    )
    if is_err(transformed_news_list_result):
        return Err(
            "Failed to transform_raw_news_into_transformed_news"
            + transformed_news_list_result.err_value
        )
    transform_news_list = transformed_news_list_result.ok_value

    transformed_news_dict = {
        "date": now_date_str,
        "transformed_news_list": transform_news_list,
        "published_by": publisher_str,
    }
    post_transformed_news_list_response = post_transformed_news_list(
        transformed_news_dict
    )
    if post_transformed_news_list_response.status_code != 200:
        return Err(
            "post_transformed_news_list_response.status_code != 200 :"
            + post_transformed_news_list_response.text
        )

    return Ok("ok")


if __name__ == "__main__":
    transform_job()
# %%
