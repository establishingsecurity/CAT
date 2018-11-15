from Cryptodome.PublicKey import RSA
from gmpy2 import mpz, mpfr, invert, powmod, gcd, isqrt, is_square, floor

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


def fermat_factoring(pk):
    """
    This attack tries to factor moduli with primes that are close to each other
    and returns a matching rsa private key

    >>> from gmpy2 import next_prime
    >>> p = int(next_prime(2**511))
    >>> q = int(next_prime(p))
    >>> e = 2**16 + 1
    >>> pk = RSA.construct((p*q, e))
    >>> key = reconstruct_private(pk, p)
    >>> sk = fermat_factoring(pk)
    >>> plain = 256
    >>> cipher = powmod(plain, key.e, key.n)
    >>> plain == int(powmod(cipher, sk.d, sk.n))
    True
    """
    # FIXME: This is not correct, what we want is ceil(sqrt(pk.n))
    a = isqrt(pk.n)
    bsqr = a*a - pk.n
    while not is_square(bsqr):
        a = a + 1
        bsqr = a*a - pk.n

    return reconstruct_private(pk, int(a - isqrt(bsqr)))


def common_divisor(pk, product):
    """
    This attack takes an rsa public key and some integer that is known to have a
    common divisor with the modulus and returns a matching rsa private key

    >>> key = RSA.generate(2048)
    >>> sk = common_divisor(key.publickey(), key.p * 17)
    >>> plain = 256
    >>> cipher = powmod(plain, key.e, key.n)
    >>> plain == int(powmod(cipher, sk.d, sk.n))
    True
    """
    p = int(gcd(mpz(pk.n), mpz(product)))
    return reconstruct_private(pk, p)

def lsb_oracle(public_key, ciphertext, oracle):
    # type: RSAKey, RSACiphertext, Callable[[RSACiphertext], bool] -> RSAPlaintext
    """
    The Least Significant Bit Oracle attack is a simpler variation on
    Bleichenbacher.
    
    It assumes a decryption oracle :math:`LSB(\dot)` that accepts ciphertexts and returns the
    least significant or parity bit of the decrypted plaintext.
    """
    mult = powmod(2, public_key.e, public_key.n)

    t = (ciphertext * mult) % public_key.n
    lower = mpfr(0)
    upper = mpfr(public_key.n)
    for i in range(public_key.n.bit_length()):
        possible_plaintext = (lower + upper)/2
        if not oracle(t):
            upper = possible_plaintext            # plaintext is in the lower half
        else:
            lower = possible_plaintext            # plaintext is in the upper half
        t = (t * mult) % public_key.n
    return mpz(floor(upper))
