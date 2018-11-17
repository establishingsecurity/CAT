from gmpy2 import invert
from Cryptodome.PublicKey import RSA


def reconstruct_private(pk, p):
    """
    Reconstructs the private key from a public key and a factor of the modulus
    """
    q = pk.n // p
    assert p*q == pk.n
    phi = (p-1)*(q-1)
    d = int(invert(pk.e, (p-1)*(q-1)))
    assert pk.e * d % phi == 1
    return RSA.construct((pk.n, pk.e, d, p, q), consistency_check=True)


