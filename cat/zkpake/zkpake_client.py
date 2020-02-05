from random import SystemRandom

from Cryptodome.Hash import SHA256
from gmpy2 import powmod, mpz, gmpy2
import hmac
import hashlib
from math import ceil

class ZkPakeClient():
    hash_len = 32
    cryptogen = SystemRandom()

    def receive(self, message):
        if "N" in message:
            N = message["N"]
            g = message["g"]
            p = message["p"]
            r = gmpy2.mpz_from_old_binary(SHA256.new(self.password.encode()).hexdigest().encode())
            v = self.cryptogen.randrange(p)
            t = powmod(g,v,p)
            R = powmod(g, r, p)
            g_bytes = g.to_bytes(256, 'big')
            r_bytes = gmpy2.to_binary(R)
            t_bytes = gmpy2.to_binary(t)
            n_bytes = gmpy2.to_binary(N)

            grtn_bytes = g_bytes + r_bytes + t_bytes + n_bytes

            c = gmpy2.mpz_from_old_binary(SHA256.new(grtn_bytes).hexdigest().encode())
            self.hc = gmpy2.mpz_from_old_binary(SHA256.new(gmpy2.to_binary(c)).hexdigest().encode())
            self.u = v - (self.hc * r % p)
            self.sk = self.hkdf(256, gmpy2.to_binary(c), b"")

        #if "hsk" in message:


    def send(self):
        result = {"u": self.u, "hc": self.hc}
        return result


    def hmac_sha256(self, key, data):
        return hmac.new(key, data, hashlib.sha256).digest()

    def hkdf(self, length: int, ikm, salt: bytes = b"", info: bytes = b"") -> bytes:
        if len(salt) == 0:
            salt = bytes([0] * self.hash_len)
        prk = self.hmac_sha256(salt, ikm)
        t = b""
        okm = b""
        for i in range(ceil(length / self.hash_len)):
            t = self.hmac_sha256(prk, t + info + bytes([1 + i]))
            okm += t
        return okm[:length]

    def __init__(self, password):
        self.password = password




