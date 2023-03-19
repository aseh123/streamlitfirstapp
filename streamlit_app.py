import streamlit as st

# Define a title for your app
st.title("Welcome to my Streamlit App")

# Add a slider widget for the user to select a value
user_input = st.slider("Select a value", 0, 100, 50)

# Add a 
st.write(f"You selected: {user_input}")
