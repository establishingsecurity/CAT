import logging

import gmpy2
from cat.log.log import LIB_ROOT_LOGGER_NAME as LOGGER

PRECISION_BITS = 2048


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

    if gmpy2.get_context().precision < PRECISION_BITS:
        adjust_gmpy2_precision(PRECISION_BITS)

    logger = logging.getLogger(LOGGER)

    a = gmpy2.mpz(gmpy2.ceil(gmpy2.sqrt(N)))
    b = a * a - N

    while not gmpy2.is_square(b):
        a = a + 1
        b = a * a - N

        logger.info("Iteration {} and {}".format(a, b))

    # NOTE: must convert to integer before subtraction
    result = a - gmpy2.mpz(gmpy2.sqrt(b))

    return result


def adjust_gmpy2_precision(precision):
    logger = logging.getLogger(LOGGER)

    context = gmpy2.get_context()

    expected, observed = precision, context.precision

    logger.warning(
        "Expected gmpy2 context to have at least {} bits of precision, was {}".format(
            expected, observed
        )
    )

    context.precision = expected

    logger.warning(
        "Changed gmpy2 context to have {} bits of precision".format(expected)
    )


if __name__ == "__main__":

    pass

    product = 123456789 ** 2

    print(factor(product))

    base = 123456789123456789
    product = 123456789123456789 ** 2

    print(factor(product) == base)
