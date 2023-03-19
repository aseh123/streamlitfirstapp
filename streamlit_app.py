import streamlit as st
import bech32



def main():
    st.title("Bech32 Converter")
    string = st.text_input("Enter a string to convert:")
    hrp = "thor" # Human-readable part for rune addresses
    data = bytes(string.encode())
    witprog = bech32.convertbits(data, 8, 5)
    out = bech32.encode(hrp, witprog)
    if st.button("Convert"):
        try:
            result = out
            st.success(f"Bech32 format: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
    
if __name__ == "__main__":
    main()
