# %%
import logging
import time

from result import Err, Ok, Result, is_err

from transform.chain.chain import init_cnn_chain, init_tw_chain


def transformed_news_cleaning(transformed_news) -> Result[str, str]:
    # Remove the "ASSISTANT:" or "輸出:ASSISTANT:"
    if transformed_news.startswith("ASSISTANT:"):
        transformed_news = transformed_news[10:]
    if transformed_news.startswith("輸出:ASSISTANT:"):
        transformed_news = transformed_news[16:]
    return Ok(transformed_news)


def transform_raw_news_into_transformed_news(raw_news_list: list) -> Result[list, str]:
    try:
        cnn_chain = init_cnn_chain()
        tw_chain = init_tw_chain()
        try:
            tw_chain.invoke({"text": "test"})
        except Exception as e:
            time.sleep(100)
        transformed_news_list = []
        for row in raw_news_list:
            print(row)
            docs = row["content"]
            logging.info("Chain invoke start")
            print("Chain invoke start")
            res_cnn = cnn_chain.invoke({"text": docs})
            res_tw = tw_chain.invoke({"text": docs})
            logging.info("Chain invoke end")
            print("Chain invoke end")
            # Remove the "ASSISTANT:"
            row["summary"] = res_cnn
            cleaning_result = transformed_news_cleaning(res_tw)
            if is_err(cleaning_result):
                return Err(cleaning_result.err_value)
            res_tw = cleaning_result.ok_value
            row["summary_tw"] = res_tw
            transformed_news_list.append(row)
    except Exception as e:
        logging.error(e)
        return Err(e)
    return Ok(transformed_news_list)


# %%
