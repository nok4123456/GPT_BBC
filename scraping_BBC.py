# %%
from bs4 import BeautifulSoup
import requests
import polars as pl


def main():
    ROOT_WEBSITE = "https://www.bbc.com"
    NEWS_WEBSITE = "https://www.bbc.com/news"
    response = requests.get(NEWS_WEBSITE)
    content = response.text
    content_element: BeautifulSoup = BeautifulSoup(content, "lxml")
    most_read_element = content_element.find("div", class_="nw-c-most-read")
    most_read_links_elements_list = most_read_element.find_all("a")
    df_schema = {
        "title": pl.Utf8,
        "link": pl.Utf8,
        "content": pl.Utf8,
        "image": pl.Utf8,
    }
    all_news_df = pl.DataFrame(schema=df_schema)

    for most_read_links_elements in most_read_links_elements_list:
        title = most_read_links_elements.text
        link = ROOT_WEBSITE + most_read_links_elements["href"]
        new_df = pl.DataFrame(
            {"title": [title], "link": [link], "content": "None", "image": "None"}
        )
        all_news_df = all_news_df.extend(new_df)

    news = []
    for row in all_news_df.rows(named=True):
        link = row["link"]
        target_news_url = link
        response = requests.get(target_news_url)

        content = response.text
        content_element: BeautifulSoup = BeautifulSoup(content, "lxml")
        article_element = content_element.find("article")

        image_container_element = article_element.find(
            "div", {"data-component": "image-block"}
        )
        image_element = image_container_element.find("img")
        row["image"] = image_element["src"]

        text_elements_list = article_element.find_all(
            "div", {"data-component": "text-block"}
        )
        new_content = ""
        for text_element in text_elements_list:
            text = text_element.text
            new_content += text
        row["content"] = new_content
        news.append(row)

    all_news_df = pl.DataFrame(news, schema=df_schema)
    all_news_df.write_csv("news.csv")

    return


if __name__ == "__main__":
    main()
