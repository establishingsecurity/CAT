from .checks import check_public
from Cryptodome.PublicKey import RSA
from .. import CheckResult, Severity

def test_check_public():
    """
    Does basic checks on a RSA public key

    :pk The RSA public key
    """
    result = check_public(RSA.generate(1024))
    assert result.comment == ''
    assert result.severity == Severity.OK

# def test_check_modulus():
#     """
#     Checks a RSA modulus

#     :n The RSA modulus
#     """
#     return all([check_composite(n), check_size(n)])

# def test_check_composite():
#     """
#     Checks if the modulus has good RSA sizes

#     :n The RSA modulus
#     """
#     # TODO: Research exact size
#     return log2(n) >= 1024

# def test_check_composite():
#     """
#     Checks if a number is probably composite in a RSA sense

#     :n The composite number
#     """
#     return n % 2 == 1
