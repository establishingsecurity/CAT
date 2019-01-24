import pytest

from cat.factorize.fermat import factor


@pytest.mark.parametrize(
    "data",
    [
        [9, [3, 3]],
        [15, [3, 5]],
        [21, [3, 7]],
        [25, [5, 5]],
        [27, [3, 9]],
        [33, [3, 11]],
        [35, [5, 7]],
    ],
)
def test_factor_small_composite(data):

    product, factors = data

    assert factor(product) in factors


@pytest.mark.parametrize("prime", [3, 5, 7, 11, 13, 17, 19, 23])
def test_factor_small_prime(prime):

    assert factor(prime) == 1
