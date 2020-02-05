from gmpy2 import powmod, gmpy2
from Cryptodome.Hash import SHA256
import datetime

class OfflineDictionaryAttack():

    def crack_password(self, N, u, hc, p, g):
        pw = ""
        counter = 0;
        for password in self.file:
            counter = counter + 1

            r = gmpy2.mpz_from_old_binary(SHA256.new(password.encode()).hexdigest().encode())
            v = u + (hc * r % p)
            t = powmod(g, v, p)
            R = powmod(g, r, p)
            g_bytes = g.to_bytes(256, 'big')
            r_bytes = gmpy2.to_binary(R)
            t_bytes = gmpy2.to_binary(t)
            n_bytes = gmpy2.to_binary(N)
            grtn_bytes = g_bytes + r_bytes + t_bytes + n_bytes
            c = gmpy2.mpz_from_old_binary(SHA256.new(grtn_bytes).hexdigest().encode())
            mhc = gmpy2.mpz_from_old_binary(SHA256.new(gmpy2.to_binary(c)).hexdigest().encode())
            if mhc == hc:
                pw = password
                break

        return pw

    def __init__(self, filename):
        self.file = open(filename, "r")
