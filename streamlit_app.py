import streamlit as st
import requests

# Define the URL and endpoint
url = "https://mayanode.mayachain.info/mayachain/liquidity_auction_tier/thor.rune/"

# Define the Streamlit app
def app():
    # Set the page title and a header
    st.set_page_config(page_title="Cacao Deposit Value Extractor")
    st.header("Cacao Deposit Value Extractor")

    # Get the user input
    user_input = st.text_input("Enter the user input string:", value="maya1ry8gr7clqyvrvsk7m53ak09yc7pcewpgx4r2uv")

    # Define the API endpoint with the user input
    endpoint = url + user_input

    # Send a GET request to the API endpoint
    response = requests.get(endpoint)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the cacao deposit value from the data
        cacao_deposit_value = data["cacao_deposit_value"]
        # Display the cacao deposit value to the user
        st.write(f"The cacao deposit value is: {cacao_deposit_value}")
    else:
        # Display an error message if the request was unsuccessful
        st.error(f"Error: {response.status_code} - {response.reason}")

if __name__ == "__main__":
    app()
