from Cryptodome.PublicKey import RSA

import gmpy2

from . import RSAKey
from .. import CheckResult, Severity


def check_public(pk):
    # type: RSAKey
    """
    Checks the RSA public key for anything "easy and suspicious"

    :param pk: the RSA public key
    :return: a list of check results
    """
    return [check_composite(pk.n), check_modulus_size(pk.n), check_prime(pk.e)]


def check_public_rsa_exponent(pk):
    # type: RSAKey
    """
    Checks if the public RSA exponent is non-standard

    The well-known, widely-used standard default is 65537. If you pick something
    higher, you end up doing unnecessary work. If you pick something lower, you
    run a small risk of having a weak cipher if your padding (or something else)
    is weak too.

    See:
        1. https://crypto.stackexchange.com/a/3113/23435
        2. https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf
    """

    results = []

    if pk.e != 65537:
        results.append(
            CheckResult(
                Severity.OK,
                "This is a deliberate deviation from the well-known, common default.",
            )
        )

    if pk.e > 65537:
        results.append(
            CheckResult(
                Severity.OK, "Larger than default: will slow down RSA performance."
            )
        )

    # Based on https://crypto.stackexchange.com/a/3113/23435
    if pk.e < 65537:
        results.append(
            CheckResult(
                Severity.OK,
                "Smaller than default: (unlikely) could be weak if padding is weak.",
            )
        )

    # From "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, where
    # section 4.2 mentions "Hastard's Broadcast attack"
    # The if block below uses an arbitrary choice of a small constant
    if pk.e < 512:
        result.append(
            CheckResult(
                Severity.OK,
                """
                If the same message is encrypted roughly {} times for different
                values of N, then the message could be recovered.
                """.format(
                    e
                ),
            )
        )

    # From "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, where
    # section 4.5 mentions "Partial Key Exposure Attack"
    # This will be a very noisy check though, very often true.
    if pk.e < gmpy2.sqrt(n):
        result.append(
            CheckResult(
                Severity.OK,
                """
                If you could recover some bits of the private key, then maybe
                you could recover the whole private key.
                """,
            )
        )

    return results


def check_private_rsa_exponent(pk):
    # type: RSAKey

    # From "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, where
    # section 3 mentions "Cryptanalysis of short RSA secret exponents" by Wiener
    if pk.d < 0.3 * pow(pk.n, 1 / 4):
        return CheckResult(
            Severity.SUSPICIOUS,
            "Very small private exponent: could be vulnerable to Wiener 1990",
        )


def check_prime(p):
    # type: int
    """
    Checks if given number is a prime

    :p the potential prime
    """
    if not gmpy2.is_prime(p):
        return CheckResult(Severity.SUSPICIOUS, "Not a prime")

    return CheckResult()


def check_modulus_size(n):
    # type: int
    """
    Checks if the modulus has good RSA sizes

    :n The RSA modulus
    """
    # TODO: Research exact size

    if gmpy2.log2(n) < 1023:
        return CheckResult(Severity.SUSPICIOUS, "Modulus too small")

    return CheckResult()


def check_composite(n):
    # type: int
    """
    Checks if a number is probably composite in a RSA sense

    :n The composite number
    """
    if n % 2 == 0:
        return CheckResult(Severity.CRITICAL, "Modulus is even")

    return CheckResult()
