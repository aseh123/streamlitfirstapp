import streamlit as st
import plotly.express as px
import pandas as pd
import requests

# Get BTC price data from Coindesk API
response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2022-03-01&end=2023-03-01')
btc_data = response.json()['bpi']
df = pd.DataFrame.from_dict(btc_data, orient='index', columns=['BTC Price'])

# Create line chart using Plotly Express
fig = px.line(df, x=df.index, y='BTC Price', title='BTC Price Chart')

# Display chart in Streamlit
st.plotly_chart(fig)
