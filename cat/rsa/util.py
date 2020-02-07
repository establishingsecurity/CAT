from typing import TYPE_CHECKING, Tuple, Union

from Cryptodome.PublicKey import RSA
from Cryptodome.PublicKey.RSA import RsaKey
from gmpy2 import invert

if TYPE_CHECKING:

    class RSAKeyLike:
        n: int
        e: int


def reconstruct_private(pk, p):
    # type: (RSAKeyLike, int) -> RsaKey
    """
    Reconstructs the private key from a public key and a factor of the modulus
    """
    q = pk.n // p
    assert p * q == pk.n
    phi = (p - 1) * (q - 1)
    d = int(invert(pk.e, (p - 1) * (q - 1)))
    assert pk.e * d % phi == 1
    return RSA.construct((pk.n, pk.e, d, p, q), consistency_check=True)


def reconstruct_privates(pks, factors):
    """
    Reconstructs private keys from public keys if a factor of the modulus is in
    the factors list
    """

    def filtering(k):
        factor = list(filter(lambda p: (k.n % p == 0), factors))
        if len(factor) > 0:
            return reconstruct_private(k, factor[0])
        else:
            return k

    return list(map(lambda k: filtering(k), pks))
