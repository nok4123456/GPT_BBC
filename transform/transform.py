# %%
from transform.chain.chain import init_cnn_chain
from cloudpathlib import GSPath
import polars as pl
import logging


def main():
    GS_FILE_PATH = GSPath(
        "gs://ken_chan_personal_project/gpt_bbc_project/transformed_news.csv"
    )
    chain = init_cnn_chain()
    original_news_df = pl.read_csv("./data/news.csv")
    transformed_news_list = []
    for row in original_news_df.rows(named=True):
        docs = row["content"]
        logging.info("Chain invoke start")
        res = chain.invoke({"text": docs})
        logging.info("Chain invoke end")
        row["summary"] = res
        transformed_news_list.append(row)
    transformed_news_df = pl.DataFrame(transformed_news_list)
    transformed_news_df.write_csv("./data/transformed_news.csv")
    GS_FILE_PATH.upload_from("./data/transformed_news.csv")
    return


if __name__ == "__main__":
    main()

# %%
