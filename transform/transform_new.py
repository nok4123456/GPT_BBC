# %%
from transform.chain.chain import init_cnn_chain
import logging
from result import Ok, Err, Result


def transform_raw_news_into_transformed_news(raw_news_list: list) -> Result[list, str]:
    try:
        chain = init_cnn_chain()
        transformed_news_list = []
        for row in raw_news_list:
            docs = row["content"]
            logging.info("Chain invoke start")
            res = chain.invoke({"text": docs})
            logging.info("Chain invoke end")
            row["summary"] = res
            transformed_news_list.append(row)
    except Exception as e:
        logging.error(e)
        return Err(e)
    return Ok(transformed_news_list)


# %%
