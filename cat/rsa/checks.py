from Cryptodome.PublicKey import RSA
from gmpy2 import log2, is_prime
from .. import CheckResult, Severity

# TODO: Type this
def check_public(pk):
    """
    Does basic checks on a RSA public key

    :pk The RSA public key
    """
    return all([check_modulus(pk.n), check_public_exponent(pk.e)])

def check_public_exponent(e: int):
    """
    Checks a RSA public exponent

    :e The RSA public exponent
    """
    # TODO: Public exponent of 3 enables certain attacks
    return [check_prime(e)]

def check_prime(p: int):
    """
    Checks if given number is a prime

    :p the potential prime
    """
    result = CheckResult()
    if not is_prime(p):
        result.severity = Severity.CRITICAL
        result.comment = 'Not a prime'
    return result

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
