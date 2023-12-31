import streamlit as st
import polars as pl


def load_data():
    transformed_news_path = "https://storage.googleapis.com/ken_chan_personal_project/gpt_bbc_project/transformed_news.csv"
    return pl.read_csv(transformed_news_path)


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="News Summary Demo", layout="wide")
    load_css("./style.css")
    st.write(
        "# <span style = 'text-align:center'>News Summary Demo</span>",
        unsafe_allow_html=True,
    )
    st.write(
        "This application is a demo for BBC news summary. It will scrape the most read news from BBC and use LLM to generate the summary."
    )
    st.write("It will refresh every 30 minutes.")
    news_df = load_data()
    for row in news_df.rows(named=True):
        title_with_link = f"<a style='text-decoration: none' href='{row['link']}' target='_blank'>{row['title']}</a>"
        st.write(f"## {title_with_link}", unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"<p class='content'>{row['summary']}</p>", unsafe_allow_html=True)
        img_markdown = (
            f'<img class="picture" src="{row["image"]}" alt="{row["title"]}">'
        )
        with col2:
            st.markdown(img_markdown, unsafe_allow_html=True)
        st.write("---")
    return


if __name__ == "__main__":
    main()
