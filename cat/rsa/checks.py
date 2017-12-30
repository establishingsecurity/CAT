from Cryptodome.PublicKey import RSA
from gmpy2 import log2

# TODO: Type this
def check_public(pk):
    """
    Does basic checks on a RSA public key

    :pk The RSA public key
    """
    return check_modulus(pk.n)

def check_modulus(n: int):
    """
    Checks a RSA modulus

    :n The RSA modulus
    """
    return all([check_composite(n), check_size(n)])

def check_size(n: int):
    """
    Checks if the modulus has good RSA sizes

    :n The RSA modulus
    """
    # TODO: Research exact size
    return log2(n) >= 1023

def check_composite(n: int):
    """
    Checks if a number is probably composite in a RSA sense

    :n The composite number
    """
    return n % 2 == 1
