import duckdb
import os

import pandas as pd
import streamlit as st

@st.cache_data
def get_article_data():
    db_name = os.environ.get("MD_DB_NAME", "athena_beta")
    motherduck_token = os.environ.get("MOTHERDUCK_KEY")
    db_url = f"md:{db_name}?motherduck_token={motherduck_token}"
    print(db_url)
    conn = duckdb.connect(db_url)

    # Assuming table name is "articles". Replace "articles" with your actual table name
    q = "SELECT title,category,summary,link,site_summary,authors FROM athena_beta.public.summarize_articles"
    df: pd.DataFrame = conn.execute(q).fetch_df()

    return df.set_index("link")


for idx, row in get_article_data().sort_index().iterrows():
    article_title = row['title']
    article_link = idx
    summary = row['summary']

    # Displaying the link with clickable URL
    st.markdown(f"[{article_title}]({article_link})")

    # Displaying the summary
    st.write(f"Summary: {summary}")
