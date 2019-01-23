import logging

import gmpy2
from cat.log.log import LIB_ROOT_LOGGER_NAME as LOGGER


def factor(N):
    # type: mpz
    """
    Computes a factorization of N using pure Fermat approach

    Expects N to be odd (i.e. 3, 5, etc.) and throws a ValueError otherwise.
    See: https://en.wikipedia.org/wiki/Fermat%27s_factorization_method

    Args:
        N: the number to factorize

    Returns:
        A factor of N

    Raises:
        ValueError: if N is even
    """

    if N & 1 == 0:
        raise ValueError("Expected N to be odd, was {}".format(N))

    logger = logging.getLogger(LOGGER)

    bits = 2048
    if gmpy2.get_context().precision < bits:
        logger.warning(
            "Precision of gmpy2 is too low, consider >= {} bits".format(bits)
        )

    a = gmpy2.mpz(gmpy2.ceil(gmpy2.sqrt(N)))
    b = a * a - N

    while not gmpy2.is_square(b):
        a, b = a + 1, b + 2 * a + 1

    # NOTE: must convert to integer before subtraction
    result = a - gmpy2.mpz(gmpy2.sqrt(b))

    return result


if __name__ == "__main__":

    pass

    product = 123456789 ** 2

    print(factor(product))

    base = 123456789123456789
    product = 123456789123456789 ** 2

    print(factor(product) == base)
