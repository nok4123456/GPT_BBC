# %%

from dotenv import load_dotenv
from chain import init_chain
import polars as pl


def main():
    load_dotenv()
    chain = init_chain()
    original_news_df = pl.read_csv("./news.csv")
    transformed_news_list = []
    for row in original_news_df.rows(named=True):
        docs = row["content"]
        print("Chain invoke start")
        print(len(docs))
        res = chain.invoke({"text": docs})
        print("Chain invoke end")
        row["summary"] = res
        transformed_news_list.append(row)
    transformed_news_df = pl.DataFrame(transformed_news_list)
    transformed_news_df.write_csv("./transformed_news.csv")
    return


if __name__ == "__main__":
    main()

# %%
