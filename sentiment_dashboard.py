
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Investment Sentiment Engine", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sample_df.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    sample_df = load_data()
except FileNotFoundError:
    st.error("🚨 sample_df.csv not found. Please place it in the same folder as this script.")
    st.stop()

st.title("📊 Investment Sentiment Engine Dashboard")

# Sidebar filters
stocks = sample_df['Stock_symbol'].unique()
selected_stock = st.sidebar.selectbox("Select a stock", sorted(stocks))

filtered_df = sample_df[sample_df['Stock_symbol'] == selected_stock].copy()

# Display a data table
st.subheader("Headline Sentiment and Price Movement")
st.dataframe(
    filtered_df[['date', 'Article_title', 'sentiment', 'return_1d', 'signal']].sort_values(by='date', ascending=False),
    height=400
)

# Time series chart
st.subheader("Price & Sentiment Over Time")
line_chart = alt.Chart(filtered_df).mark_line().encode(
    x='date:T',
    y='close:Q',
    tooltip=['date', 'close', 'sentiment', 'signal']
).properties(width=800, height=400)

# Sentiment dots
color_sentiment = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x='date:T',
    y='close:Q',
    color='sentiment:N',
    tooltip=['Article_title', 'return_1d', 'signal']
)

st.altair_chart(line_chart + color_sentiment)
