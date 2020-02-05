from random import SystemRandom

from cat.utils.ntheory import gen_safe_prime
from gmpy2 import powmod, mpz, gmpy2
from Cryptodome.Hash import SHA256

class ZkPakeServer():
    g = 2
    cryptogen = SystemRandom()

    def send(self):
        self.p = gen_safe_prime(128)
        n = self.cryptogen.randrange(self.p)
        self.N = powmod(self.g, n, self.p)
        result = {"N": self.N, "g":self.g, "p":self.p}
        return result;

    def receive(self, message):
        u = message["u"]
        hc = message["hc"]
        r = gmpy2.mpz_from_old_binary(SHA256.new(self.password.encode()).hexdigest().encode())
        R = powmod(self.g, r, self.p)
        t = powmod(self.g, u, self.p) * powmod(self.g, r*hc, self.p)
        g_bytes = self.g.to_bytes(256, 'big')
        r_bytes = gmpy2.to_binary(R)
        t_bytes = gmpy2.to_binary(t)
        n_bytes = gmpy2.to_binary(self.N)

        grtn_bytes = g_bytes + r_bytes + t_bytes + n_bytes

        c = gmpy2.mpz_from_old_binary(SHA256.new(grtn_bytes).hexdigest().encode())

    def __init__(self, password):
        self.password = password