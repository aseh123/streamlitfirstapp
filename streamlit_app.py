import streamlit as st
import bech32

st.title("Bech32 Converter")

string = st.text_input("Enter a string to convert:")

if st.button("Convert"):
    try:
        hrp = "bc" # Human-readable part for Bitcoin addresses
        data = bytes(string.encode())
        witprog = bech32.convertbits(data, 8, 5)
        result = bech32.encode(hrp, witprog)
        st.success(f"Bech32 format: {result}")
    except Exception as e:
        st.error(f"Error: {e}")
