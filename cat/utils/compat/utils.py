import sys
from binascii import hexlify

if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
    def hex_str(byte_str):
        return str(hexlify(byte_str), 'utf-8')
else:
    def hex_str(byte_str):
        return hexlify(byte_str)
