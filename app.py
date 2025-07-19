import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

# custom css
background_color = """
<style>

[data-testid="stAppViewContainer"] {
    background-color: #120128; /* Background color set to blue */


</style>
"""
st.markdown(background_color, unsafe_allow_html=True)
st.set_page_config(
    page_title="US Airline Sentiment 📊",
    page_icon="✈️",  # You can use emoji or upload a favicon
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("Sentiment Analysis on Tweets about US Airlines")
    st.sidebar.title("Sentiment Analysis on Tweets")
    st.subheader("A data-driven web app that visualzizes various sentiment and exploratory analysis on tweets about US Airlines.")
    st.sidebar.markdown("A data-driven web app that visulizes various sentiment and exploratory analysis on tweets about US Airlines.")
    st.sidebar.subheader("By [Gazal](https://github.com/G5277)")

    @st.cache_data(persist = True)
    def load_data():
        data = pd.read_csv("Tweets.csv")
        data["tweets_created"] = pd.to_datetime(data["tweet_created"])
        return data
    
    data = load_data()

    st.markdown("---")

    # Show random tweet
    st.sidebar.subheader("Show Random Tweet")
    random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
    if not st.sidebar.checkbox("Hide", True, key = '0'):
        st.subheader(f"Random {random_tweet.capitalize()} Tweet")
        st.header(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0,0])
        st.markdown("---")



    # Number of tweets by sentiment
    st.sidebar.subheader("Number of Tweets by Sentiment")
    select = st.sidebar.selectbox("Visualization Type", ["Bar Plot", "Pie Chart"])
    sentiment_count = data["airline_sentiment"].value_counts()
    sentiment_count = pd.DataFrame({"Sentiment":sentiment_count.index, "Tweets":sentiment_count.values})
    if not st.sidebar.checkbox("Hide", False, key = '1'):
        st.subheader("Number of Tweets by Sentiment")
        if select == "Bar Plot":
            fig = px.bar(sentiment_count, x = "Sentiment", y = "Tweets", color = "Tweets")
            st.plotly_chart(fig)
        if select == "Pie Chart":
            fig = px.pie(sentiment_count, values = "Tweets", names = "Sentiment")
            st.plotly_chart(fig)


    # Tweet locations based on time of day
    st.sidebar.subheader("Tweet locations based on time of day")
    hour = st.sidebar.slider("Hour to look at", 0, 23)

    # Parse tweet_coord into latitude and longitude
    data['latitude'] = data['tweet_coord'].apply(lambda x: float(x.split(',')[0][1:]) if isinstance(x, str) else None)
    data['longitude'] = data['tweet_coord'].apply(lambda x: float(x.split(',')[1][:-1]) if isinstance(x, str) else None)

    # Drop rows with missing coordinates
    data = data.dropna(subset=['latitude', 'longitude'])

    # Convert `tweets_created` to datetime if needed
    data['tweets_created'] = pd.to_datetime(data['tweets_created'], errors='coerce')
    selected_data = data[data["tweets_created"].dt.hour == hour]

    if not st.sidebar.checkbox("Hide", False, key = "2"):
        st.subheader("Tweet locations based on time of the day")
        st.markdown(f"{len(selected_data)} tweets between {hour}:00 and {(hour + 1) % 24}:00")

        # Ensure selected_data has latitude and longitude columns
        st.map(selected_data[['latitude', 'longitude']])

    st.markdown("---")
    
    # Number of tweets for each airline
    st.sidebar.subheader("Tweet of tweets for each Airline")
    each_airline = st.sidebar.selectbox("Visualization Type", ["Bar Plot", "Pie Chart"], key = "3")
    airline_sentiment_count = data.groupby("airline")["airline_sentiment"].count().sort_values(ascending = False)
    airline_sentiment_count = pd.DataFrame({"Airline":airline_sentiment_count.index, "Tweets":airline_sentiment_count.values.flatten()})
    if not st.sidebar.checkbox("Hide", False, key = "4"):
        if each_airline == "Bar Plot":
            st.subheader("Number of Tweets for Each Airline")
            fig = px.bar(airline_sentiment_count, x = "Airline", y = "Tweets", color = "Tweets")
            st.plotly_chart(fig)
        if each_airline == "Pie Chart":
            st.subheader("Number of Tweets for Each Airline")
            fig = px.pie(airline_sentiment_count, values = "Tweets", names = "Airline")
            st.plotly_chart(fig)

    st.markdown("---")

    # Breakdown airline tweets by sentiment
    st.sidebar.subheader("Breakdown Airline Tweets by Sentiment")
    choice = st.sidebar.multiselect("Pick Airline(s)", tuple(pd.unique(data["airline"])))
    if not st.sidebar.checkbox("Hide", True, key = "5"):
        if len(choice) > 0:
            st.header("Breakdown Airline Tweets by Sentiment")
            chosen_data = data[data["airline"].isin(choice)]
            fig = px.histogram(chosen_data, x = "airline", y = "airline_sentiment", histfunc="count", 
                               color = "airline_sentiment", facet_col="airline_sentiment",
                               labels = {"airline_sentiment" : "sentiment"})
            st.plotly_chart(fig)
            st.markdown("---")



    # World Cloud
    st.sidebar.subheader("Word Cloud")
    word_sentiment = st.sidebar.radio("Which Sentiment to Display>", tuple(pd.unique(data["airline_sentiment"])))
    if not st.sidebar.checkbox("Hide", False, key = "6"):
        st.subheader(f"Word Cloud for {word_sentiment.capitalize()} Sentiment")
        df = data[data["airline_sentiment"] == word_sentiment]
        words = " ".join(df["text"])
        processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith("@") and word != "RT"])
        wordcloud =  WordCloud(stopwords = STOPWORDS, background_color = "white", width = 800, height = 640).generate(processed_words)
        # plt.imshow(wordcloud)
        # plt.xticks([])
        # plt.yticks([])
        # st.pyplot()

        fig,ax = plt.subplots()
        ax.imshow(wordcloud, interpolation = "bilinear")
        ax.axis("off")
        plt.xticks([])
        plt.yticks([])

        st.pyplot(fig)

    st.markdown("---")

    st.markdown(
        """
        <div style="text-align: center; font-size: 16px;">
            This app was created with love by 
            <a href="https://github.com/G5277" target="_blank" style="text-decoration: none; color: #ff4b4b;">
                Gazal &#10084
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()