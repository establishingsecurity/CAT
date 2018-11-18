import pytest

import copy
import random


from cat.rsa.batch_gcd import compute_product
from cat.rsa.batch_gcd import _compute_product_0, _compute_product_1

compute_product_list = [compute_product, _compute_product_0, _compute_product_1]

@pytest.mark.parametrize("compute_product", compute_product_list)
def test_compute_product_empty(compute_product):

    assert compute_product([]) == 0, "Empty list must have product 0"

@pytest.mark.parametrize("compute_product", compute_product_list)
@pytest.mark.parametrize("n", [-42, -1, 0, 1, 42])
def test_compute_product_single(compute_product, n):

    assert compute_product([n]) == n, "Single element must be unchanged"


@pytest.mark.parametrize("compute_product", compute_product_list)
@pytest.mark.parametrize("n", list(range(2, 10)))
def test_compute_product_small_nonzero_list(compute_product, n):

    random.seed(n)

    xs = [random.randint(1, 10) for i in range(n)]
    ys = copy.copy(xs)

    result = 1
    for y in ys:
        result *= y

    assert compute_product(xs) == result, "Simple non-zero list product failed"

@pytest.mark.parametrize("compute_product", compute_product_list)
@pytest.mark.parametrize("n", list(range(2, 10)))
def test_compute_product_small_list(compute_product, n):

    random.seed(n)

    xs = [random.randint(-42, +42) for i in range(n)]
    ys = copy.copy(xs)

    result = 1
    for y in ys:
        result *= y

    assert compute_product(xs) == result, "Simple non-zero list product failed"
