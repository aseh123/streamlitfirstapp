import streamlit as st
from typing import Tuple

# Define Bech32 character set and separator
BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32_SEPARATOR = "1"

# Bech32 encoding algorithm
def bech32_encode(hrp: str, data: bytes) -> str:
    # Create checksum
    values = [ord(x) >> 5 for x in data] + [0] * 6
    for i in range(len(data)):
        values[i] = (values[i] ^ ord(data[i])) & 31
    checksum = bech32_polymod([ord(x) for x in hrp + BECH32_SEPARATOR] + values + [0]*6) ^ 1
    # Convert data and checksum to Bech32 string
    return hrp + BECH32_SEPARATOR + ''.join([BECH32_CHARSET[d] for d in values + [checksum]])

def bech32_decode(bech: str) -> Tuple[str, bytes]:
    if not all(x in BECH32_CHARSET for x in bech):
        raise ValueError("Invalid characters in Bech32 string")
    bech = bech.lower()
    pos = bech.rfind(BECH32_SEPARATOR)
    if pos == -1:
        raise ValueError("Bech32 string missing separator")
    if pos < 1 or pos + 7 > len(bech):
        raise ValueError("Invalid Bech32 string length")
    hrp = bech[:pos]
    data = bytes([BECH32_CHARSET.find(x) for x in bech[pos+1:]])
    if not bech32_verify_checksum(hrp, data):
        raise ValueError("Invalid Bech32 checksum")
    return hrp, data[:-6]

def bech32_verify_checksum(hrp: str, data: bytes) -> bool:
    values = [ord(x) & 31 for x in hrp] + [0] + [x for x in data]
    return bech32_polymod(values) == 1

def bech32_polymod(values: list) -> int:
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = (chk >> 25) & 1
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            chk ^= generator[i] if ((b >> i) & 1) else 0
    return chk

# User input prompt
input_bech32 = st.text_input("Enter a Bech32 string:", value="", max_chars=None, key=None, type='default')

if input_bech32 != "":
    try:
        hrp, data = bech32_decode(input_bech32)
       
