# %%
from bs4 import BeautifulSoup
import requests
import polars as pl
import logging
from result import Ok, Err, Result


def main() -> Result[list, Exception]:
    try:
        ROOT_WEBSITE = "https://www.bbc.com"
        NEWS_WEBSITE = "https://www.bbc.com/news"
        logging.info("Scraping start")
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
            try:
                image_element = image_container_element.find("img")
                row["img_url"] = image_element["src"]
            except AttributeError:
                image_element = None
                row["img_url"] = "None"

            text_elements_list = article_element.find_all(
                "div", {"data-component": "text-block"}
            )
            new_content = ""
            for text_element in text_elements_list:
                text = text_element.text
                new_content += text
            row["content"] = new_content
            row["url"] = link
            row.pop("link")
            row.pop("image")
            news.append(row)
    except Exception as e:
        logging.error(e)
        return Err(e)

    logging.info("Scraping end")
    return Ok(news)


if __name__ == "__main__":
    main()

# %%
