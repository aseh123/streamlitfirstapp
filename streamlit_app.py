import streamlit as st
import requests

# Define a title for your app
st.title("Current Bitcoin Price")

# Fetch the current price of BTC from the CoinGecko API
response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
data = response.json()
btc_price = data["bitcoin"]["usd"]

# Display the current price of BTC
st.write(f"The current price of Bitcoin is ${btc_price}")
