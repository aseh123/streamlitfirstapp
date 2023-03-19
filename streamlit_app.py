import streamlit as st
import bech32


def bech32_converter(string: str) -> str:
    """Converts a given string to bech32 format."""
    hrp = "thor" # Human-readable part for rune addresses
    data = bytes(string.encode())
    witprog = bech32.convertbits(data, 8, 5)
    return bech32.encode(hrp, witprog)

def main():
    st.title("Bech32 Converter")

    string = st.text_input("Enter a string to convert:")
    
    if st.button("Convert"):
        try:
            result = bech32_converter(string)
            st.success(f"Bech32 format: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
    
if __name__ == "__main__":
    main()
