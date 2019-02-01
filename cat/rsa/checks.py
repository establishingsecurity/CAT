import gmpy2
from cat.utils.result import Result
from cat.utils.result import ResultEntry as RE
from cat.utils.result import Severity


class RSAResult(Result):
    """
    Results for checks on RSA components.
    """

    OK = RE(Severity.OK, """The RSA component is as one would expect.""")
    SMALL_MODULUS = RE(Severity.SUSPICIOUS, """Modulus is smaller than 1023.""")
    EVEN_MODULUS = RE(Severity.CRITICAL, """Modulus is even and therefore composite.""")


class RSAPublicKeyResult(RSAResult):
    """
    Results for checks on RSA public keys. The value of the members denote their severity.
    """

    NON_DEFAULT = RE(
        Severity.OK,
        "The public key is a deliberate deviation from the well-known, common default.",
    )
    LARGER_THAN_DEFAULT = RE(
        Severity.OK, "Larger than default: will slow down RSA performance."
    )
    SMALLER_THAN_DEFAULT = RE(
        Severity.OK,
        "Smaller than default: (unlikely) could be weak if padding is weak.",
    )
    BROADCAST_ATTACK = RE(
        Severity.OK,
        (
            "If the same message is encrypted roughly b times for different "
            "values of N, where b is the Bound given to :func:`check_public_rsa_exponent`, "
            "then the message could be recovered. "
            'See "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, section 4.2.'
        ),
    )
    PARTIAL_KEY_EXPOSURE = RE(
        Severity.OK,
        (
            "If you could recover some bits of the private key, then maybe you could recover"
            "the whole private key. "
            'See "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, section 4.5.'
        ),
    )
    NON_PRIME = RE(Severity.SUSPICIOUS, "The public key's exponent is non-prime.")


class RSAPrivateKeyResult(RSAResult):
    """
    Results for checks on RSA private keys. The value of the members denote their severity.
    """

    SMALL_PRIVATE_EXPONENT = RE(
        Severity.SUSPICIOUS,
        "Very small private exponent: could be vulnerable to Wiener 1990",
    )


def check_public_key(N, e):
    # type: (int, int) -> Tuple[RSAResult, RSAResult, RSAPublicKeyResult]
    """
    Checks the RSA public key for anything "easy and suspicious"

    :param e: The RSA public exponent.
    :param N: The RSA modulus.
    :return: a list of check results
    """
    results = [check_composite(N), check_modulus_size(N), check_prime(e)]
    results.extend(check_public_rsa_exponent(N, e))

    return results


def check_modulus(n):
    # type: (int) -> RSAResult
    """
    Checks the RSA modulus for anything "easy and suspicious".
    """
    return [check_composite(n), check_modulus_size(n)]


def check_public_rsa_exponent(N, e, BOUND=64):
    # type: (RSAKey, int) -> List[RSAPublicKeyResult]
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
    results.extend(_check_public_exponent(e, BOUND))
    results.extend(_check_pub_exp_modulus(e, N))
    return results


def _check_public_exponent(e, BOUND=64):
    results = []

    if e != 65537:
        results.append(RSAPublicKeyResult.NON_DEFAULT)

    if e > 65537:
        results.append(RSAPublicKeyResult.LARGER_THAN_DEFAULT)

    # Based on https://crypto.stackexchange.com/a/3113/23435
    if e < 65537:
        results.append(RSAPublicKeyResult.SMALLER_THAN_DEFAULT)

    # From "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, where
    # section 4.2 mentions "Hastard's Broadcast attack"
    # The if block below uses an arbitrary choice of a small constant
    if e < BOUND:
        results.append(RSAPublicKeyResult.BROADCAST_ATTACK)

    return results


def _check_pub_exp_modulus(e, n):
    results = []

    # From "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, where
    # section 4.5 mentions "Partial Key Exposure Attack"
    # This will be a very noisy check though, very often true.
    if e < gmpy2.sqrt(n):
        results.append(RSAPublicKeyResult.PARTIAL_KEY_EXPOSURE)

    return results


def check_private_key(N, d):
    return [check_composite(N), check_modulus_size(N), check_private_rsa_exponent(N, d)]


def check_private_rsa_exponent(N, d):
    # type: (int, int) -> RSAPrivateKeyResult

    # From "Twenty Years of Attacks on the RSA Cryptosystem" by Dan Boneh, where
    # section 3 mentions "Cryptanalysis of short RSA secret exponents" by Wiener
    if d < 0.3 * pow(N, 1 / 4):
        return RSAPrivateKeyResult.SMALL_PRIVATE_EXPONENT
    return RSAPrivateKeyResult.OK


def check_prime(p):
    # type: (int) -> RSAPublicKeyResult
    """
    Checks if given number is a prime

    :p the potential prime
    """
    if not gmpy2.is_prime(p):
        return RSAPublicKeyResult.NON_PRIME
    return RSAPublicKeyResult.OK


def check_modulus_size(n):
    # type: (int) -> RSAResult
    """
    Checks if the modulus has good RSA sizes

    :n The RSA modulus
    """
    # TODO: Research exact size

    if gmpy2.log2(n) < 1023:
        return RSAResult.SMALL_MODULUS
    return RSAResult.OK


def check_composite(n):
    # type: (int) -> RSAResult
    """
    Checks if a number is probably composite in a RSA sense

    :n The composite number
    """
    if n % 2 == 0:
        return RSAResult.EVEN_MODULUS
    return RSAResult.OK
