# app.py

import streamlit as st
import requests

API_KEY = "a3f417b116fa4104b3c547e8ee9d32e1"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Headlines App",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Advanced News Headlines App")
st.write("Fetch latest news headlines by country, topic, keywords, and article count.")

# Sidebar filters
st.sidebar.header("🔍 Filter News")

country = st.sidebar.selectbox(
    "Select Location / Country",
    {
        "India": "in",
        "United States": "us",
        "United Kingdom": "gb",
        "Australia": "au",
        "Canada": "ca",
        "Germany": "de",
        "France": "fr",
        "Japan": "jp"
    }
)

category = st.sidebar.selectbox(
    "Select Topic",
    [
        "general",
        "business",
        "technology",
        "sports",
        "entertainment",
        "health",
        "science"
    ]
)

page_size = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

keyword = st.sidebar.text_input("Search Keyword")

fetch_button = st.sidebar.button("Fetch News")


def fetch_news(country_code, category, page_size, keyword):
    params = {
        "apiKey": API_KEY,
        "country": country_code,
        "category": category,
        "pageSize": page_size
    }

    if keyword:
        params["q"] = keyword

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None


if fetch_button:
    news_data = fetch_news(country, category, page_size, keyword)

    if news_data and news_data.get("status") == "ok":
        articles = news_data.get("articles", [])

        st.subheader(f"Showing {len(articles)} News Articles")

        if len(articles) == 0:
            st.warning("No articles found. Try changing filters.")
        else:
            for article in articles:
                with st.container():
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        if article.get("urlToImage"):
                            st.image(article["urlToImage"], use_container_width=True)
                        else:
                            st.info("No Image")

                    with col2:
                        st.markdown(f"### {article.get('title', 'No Title')}")
                        st.write(article.get("description", "No description available."))

                        st.write(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                        st.write(f"**Published At:** {article.get('publishedAt', 'Unknown')}")

                        if article.get("url"):
                            st.link_button("Read Full Article", article["url"])

                    st.divider()

    else:
        st.error("Failed to fetch news.")
else:
    st.info("Use the sidebar filters and click **Fetch News**.")