import pytest

import copy
import random


from cat.rsa.batch_gcd import compute_product
from cat.rsa.batch_gcd import _compute_product_0, _compute_product_1
from cat.rsa.batch_gcd import build_product_tree
from cat.rsa.batch_gcd import _build_product_tree_0, _build_product_tree_1

compute_product_list = [
    compute_product, _compute_product_0, _compute_product_1
]
build_product_tree_list = [
    build_product_tree, _build_product_tree_0, _build_product_tree_1
]


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


@pytest.mark.parametrize("build_product_tree", build_product_tree_list)
def test_build_product_tree_empty(build_product_tree):

    assert build_product_tree([]) == [[0]], "Must be empty product tree"


@pytest.mark.parametrize("build_product_tree", build_product_tree_list)
@pytest.mark.parametrize("n", [-42, -1, 0, 1, 42])
def test_build_product_tree_single(build_product_tree, n):

    assert build_product_tree([n]) == [[n]], "Single element must become the root"


@pytest.mark.parametrize("build_product_tree", build_product_tree_list)
def test_build_product_tree_two_elements(build_product_tree):

    assert build_product_tree([-1, 1]) == [[-1, 1], [-1]]
    assert build_product_tree([-1, 0]) == [[-1, 0], [0]]
    assert build_product_tree([0, -1]) == [[0, -1], [0]]

    assert build_product_tree([3, -2]) == [[3, -2], [-6]]
    assert build_product_tree([-2, 3]) == [[-2, 3], [-6]]


@pytest.mark.parametrize("build_product_tree", build_product_tree_list)
def test_build_product_tree_three_elements(build_product_tree):

    tree0 = build_product_tree([1, 2, 3])
    tree1 = [[1, 2, 3], [2, 3], [6]]
    tree2 = [[1, 2, 3], [1, 6], [6]]

    assert tree0 == tree1 or tree0 == tree2

    tree0 = build_product_tree([1, -2, 3])
    tree1 = [[1, -2, 3], [-2, 3], [-6]]
    tree2 = [[1, -2, 3], [1, -6], [-6]]

    assert tree0 == tree1 or tree0 == tree2
