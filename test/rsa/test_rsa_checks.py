from Cryptodome.PublicKey import RSA

from cat.rsa.checks import check_composite, check_modulus_size, check_public_key
from cat.utils.result import Severity


def test_check_public():
    """
    Does basic checks on a RSA public key

    :pk The RSA public key
    """
    key = RSA.generate(1024)
    result = check_public_key(key.n, key.e)
    assert all([lambda r: r.severity == Severity.OK for r in result])


def test_check_composite():
    """
    Checks if the check_composite function works correctly
    """
    # even
    result = check_composite(2)
    assert result.severity == Severity.CRITICAL

    # odd
    result = check_composite(3)
    assert result.severity == Severity.OK


def test_check_modulus_size():
    """
    Checks a RSA modulus

    :n The RSA modulus
    """
    result = check_modulus_size(pow(2, 1023))
    assert result.severity == Severity.OK

    result = check_modulus_size(pow(2, 1022))
    assert result.severity == Severity.SUSPICIOUS
