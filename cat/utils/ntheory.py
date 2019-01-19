"""
A collection of number theoretical utility functions.
"""

from gmpy2 import is_prime, mpz, next_prime


def gen_safe_prime(k):
    # (int) -> mpz
    """
    Generate a safe prime of bit length at least :code:`k`.
    
    >>> p = gen_safe_prime(256)
    >>> p.bit_length() >= 256
    True
    >>> from gmpy2 import is_prime, mpq, mpz 
    >>> q = mpz(mpq(p-1,2))
    >>> is_prime(q)
    True

    :param k: The minimum bit length of the generated safe prime.
    :returns: A safe prime as a :class:`gmpy2.mpz` multiprecision integer.
    """
    q = mpz(2 ** k + 1)
    safe_prime = lambda q: mpz(2 * q + 1)

    while not is_prime(safe_prime(q)):
        q = next_prime(q)

    return safe_prime(q)
