import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Define a title for your app
st.title("Live Bitcoin Price Chart")

# Set up the Plotly figure
fig = go.Figure()

# Fetch the historical price data for the past month from the CoinGecko API
end_date = datetime.now()
start_date = end_date - timedelta(days=30)
end_date_str = end_date.strftime("%d-%m-%Y")
start_date_str = start_date.strftime("%d-%m-%Y")
response = requests.get(f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={end_date.timestamp()}")
data = response.json()
prices = data["prices"]
x_values = [datetime.fromtimestamp(price[0]/1000.0) for price in prices]
y_values = [price[1] for price in prices]
fig.add_trace(go.Scatter(x=x_values, y=y_values, name="BTC Price"))

# Define the layout for the Plotly figure
fig.update_layout(
    title="Bitcoin Price (USD) - Past Month",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_dark"
)

# Display the live line chart of BTC price
st.plotly_chart(fig, use_container_width=True)

