import streamlit as st
import requests

# Define the Streamlit app
def app():
    # Create a user input field for the MayaChain address
    user_input = st.text_input("Enter MayaChain address")

    # Create a submit button
    if st.button("Submit"):
        # Define the URL to retrieve the data
        url = f"https://mayanode.mayachain.info/mayachain/liquidity_auction_tier/thor.rune/{user_input}"
        
        # Send a GET request to the URL and retrieve the response data
        response = requests.get(url)
        data = response.json()

        # Extract the value of "cacao_deposit_value"
        cacao_deposit_value = data["liquidity_provider"]["cacao_deposit_value"]

        # Display the value of "cacao_deposit_value"
        st.write(f"The cacao deposit value is: {cacao_deposit_value}")
