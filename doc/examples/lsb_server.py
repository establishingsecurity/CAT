import socketserver
from binascii import hexlify, unhexlify

from gmpy2 import mpz, powmod

from Cryptodome.PublicKey import RSA

# Security parameter in bytes in hex
MESSAGE_SIZE = (1024//8) * 2

def int_to_hex(n):
    return hexlify(n.to_bytes(128, 'big'))

def hex_to_int(s):
    return int.from_bytes(unhexlify(s), 'big')

class LSBHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.
    """

    def encrypt(self, plaintext):
        return powmod(plaintext, self.e, self.n)

    def oracle(self, ciphertext):
        return powmod(ciphertext, self.d, self.n) % 2

    def handle(self):
        self.key = RSA.generate(1024)
        self.n = self.key.n
        self.e = self.key.e
        self.d = self.key.d
        self.plaintext = hex_to_int(b'deadbeef')

        # First send out the public key
        self.request.sendall(int_to_hex(self.n))
        self.request.sendall(int_to_hex(self.e))
        # And the ciphertext
        self.request.sendall(int_to_hex(self.plaintext))

        # This is for optimization
        self.n = mpz(self.n)
        self.e = mpz(self.e)
        self.d = mpz(self.d)
        while True:
            # The server accepts ciphertexts in hex
            cipher = mpz(hex_to_int(self.request.recv(MESSAGE_SIZE).strip()))
            # And sends back the parity
            self.request.sendall(int_to_hex(int(self.oracle(cipher))))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), LSBHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
