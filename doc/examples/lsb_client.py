import sys
import socket
from collections import namedtuple
from binascii import hexlify, unhexlify

from cat.rsa import RSADriver

# Security parameter in bits
SECURITY_PARAMETER = 1024
# Security parameter in bytes in hex
MESSAGE_SIZE = (SECURITY_PARAMETER//8) * 2
INT_SIZE = (SECURITY_PARAMETER//8)

def int_to_hex(n):
    return hexlify(n.to_bytes(INT_SIZE, 'big'))

def hex_to_int(s):
    return int.from_bytes(unhexlify(s), 'big')

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # Get the parameters
    n = hex_to_int(sock.recv(MESSAGE_SIZE).strip())
    e = hex_to_int(sock.recv(MESSAGE_SIZE).strip())
    t = hex_to_int(sock.recv(MESSAGE_SIZE).strip())

    def oracle(c):
        sock.sendall(int_to_hex(c))
        return hex_to_int(sock.recv(MESSAGE_SIZE).strip())

    r = RSADriver()
    KeyTuple = namedtuple('KeyTuple', 'n e')
    r.keys = [KeyTuple(e=e, n=n)]
    r.add_lsb_oracle(oracle)
    print(r.run_lsb_oracle(t))

