
# ✈️ US Airline Sentiment Analysis Web App

This is an interactive Streamlit web application for visualizing **sentiment analysis on tweets about US Airlines**. It allows users to explore tweet data using charts, maps, word clouds, and more.

## 🔍 Features

- 📊 **Sentiment Distribution**: View bar/pie charts of tweet sentiments (positive/neutral/negative)
- 🗺️ **Tweet Locations**: Visualize tweet geolocations based on the hour of the day
- 🏢 **Airline-wise Sentiment Analysis**: Breakdown tweets by individual airlines
- ☁️ **Word Cloud**: Generate word clouds for each sentiment
- 🔄 **Random Tweet**: Display a random tweet by sentiment

## 🖥️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Data Visualization**: Plotly, Matplotlib
- **NLP & Preprocessing**: WordCloud
- **Data**: `Tweets.csv` (dataset of airline-related tweets)

## 📁 Dataset

The app uses the [US Airline Tweets Dataset](https://www.kaggle.com/crowdflower/twitter-airline-sentiment), with the following key columns:

- `airline_sentiment`
- `tweet_created`
- `tweet_coord`
- `airline`
- `text`

## 🚀 Live Demo

🔗 [Click here to open the app](https://twitter-us-airline-sentiment-dashboard.streamlit.app)  

## 🧠 How to Run Locally

1. **Clone the repo**  

   ```bash
   git clone https://github.com/G5277/airline-sentiment-streamlit.git
   cd airline-sentiment-streamlit
   ```

2. **Install dependencies**  

   ```bash
   pip install -r requirements.txt
   ```

3. **Place `Tweets.csv`** in the root directory (or update path in code)

4. **Run the Streamlit app**  

   ```bash
   streamlit run app.py
   ```

## 📦 Dependencies

```text
streamlit
pandas
numpy
matplotlib
plotly
wordcloud
```

Create a `requirements.txt` by running:

```bash
pip freeze > requirements.txt
```

## 🙋‍♀️ Author

**Gazal Arora**  
[GitHub Profile](https://github.com/G5277)

---

🛠️ Built with love and Streamlit
