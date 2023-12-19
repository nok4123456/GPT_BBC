# %%
import logging
import time

from result import Err, Ok, Result

from transform.chain.chain import init_cnn_chain, init_tw_chain


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
            if res_tw.startswith("ASSISTANT:"):
                row["summary_tw"] = res_tw[10:]
            else:
                row["summary_tw"] = res_tw
            transformed_news_list.append(row)
    except Exception as e:
        logging.error(e)
        return Err(e)
    return Ok(transformed_news_list)


# %%
