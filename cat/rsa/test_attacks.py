from binascii import hexlify

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from gmpy2 import powmod


from .attacks import LSBOracle

def test_lsb_oracle():
    key = RSA.generate(1024)
    class TestLSBOracle(LSBOracle):
        def query(self, m: int):
            return powmod(m, key.d, self.pk.n) % 2

    target = powmod(255, key.e, key.n)
    o = TestLSBOracle(key.publickey(), target)
    assert o.run() == 255

