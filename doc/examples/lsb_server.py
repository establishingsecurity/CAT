import socketserver
from binascii import hexlify, unhexlify

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
        return plaintext**self.key.e % self.key.n

    def oracle(self, ciphertext):
        return (ciphertext**self.key.d % self.key.n) % 2

    def handle(self):
        self.key = RSA.generate(1024)
        self.plaintext = hex_to_int(b'deadbeef')

        # First send out the public key
        self.request.sendall(int_to_hex(self.key.n))
        self.request.sendall(int_to_hex(self.key.e))
        # And the ciphertext
        self.request.sendall(int_to_hex(self.key.e))
        while True:
            # The server accepts ciphertexts in hex
            cipher = self.request.recv(MESSAGE_SIZE).strip()
            # And sends back the parity
            self.request.sendall(int_to_hex(self.oracle(hex_to_int(cipher))))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), LSBHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
