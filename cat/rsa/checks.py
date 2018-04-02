from Cryptodome.PublicKey import RSA
from gmpy2 import log2, is_prime
from .. import CheckResult, Severity

# TODO: Type this
def check_public(pk):
    """
    Does basic checks on a RSA public key

    :pk The RSA public key
    """
    return [check_composite(pk.n), check_modulus_size(pk.n), check_prime(pk.e)]

def check_prime(p):
    # type: int
    """
    Checks if given number is a prime

    :p the potential prime
    """
    if not is_prime(p):
        return CheckResult(Severity.SUSPICIOUS, 'Not a prime')
    
    return CheckResult()

def check_modulus_size(n):
    # type: int
    """
    Checks if the modulus has good RSA sizes

    :n The RSA modulus
    """
    # TODO: Research exact size

    if log2(n) < 1023:
        return CheckResult(Severity.SUSPICIOUS, 'Modulus too small')
    
    return CheckResult()

def check_composite(n):
    # type: int
    """
    Checks if a number is probably composite in a RSA sense

    :n The composite number
    """
    if n % 2 == 0:
        return CheckResult(Severity.CRITICAL, 'Modulus is even')
    
    return CheckResult()
