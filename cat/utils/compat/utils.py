import sys
from binascii import hexlify

def hex_str(byte_str):
    return hexlify(byte_str).decode('utf-8')
