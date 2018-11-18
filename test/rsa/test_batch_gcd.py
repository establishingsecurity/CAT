import pytest

import copy
import random


from cat.rsa.batch_gcd import compute_product
from cat.rsa.batch_gcd import _compute_product_0, _compute_product_1
from cat.rsa.batch_gcd import build_product_tree
from cat.rsa.batch_gcd import _build_product_tree_0, _build_product_tree_1
from cat.rsa.batch_gcd import build_remainder_tree
from cat.rsa.batch_gcd import _build_remainder_tree_0
from cat.rsa.batch_gcd import compute_remainders
from cat.rsa.batch_gcd import attack_batch_gcd
from cat.rsa.batch_gcd import _attack_batch_gcd_0, _attack_batch_gcd_1


compute_product_list = [compute_product, _compute_product_0, _compute_product_1]
build_product_tree_list = [
    build_product_tree,
    _build_product_tree_0,
    _build_product_tree_1,
]
build_remainder_tree_list = [
    build_remainder_tree,
    _build_remainder_tree_0,
]
attack_batch_gcd_list = [
    attack_batch_gcd,
    _attack_batch_gcd_0,
    _attack_batch_gcd_1
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


@pytest.mark.parametrize("build_remainder_tree", build_remainder_tree_list)
def test_build_remainder_tree_empty(build_remainder_tree):

    # The default value for an "empty" product tree is [[0]]
    # Also, the product tree is not supposed to contain a zero anywhere, because
    # it is only possible if the initial data contained a zero. So, it is very
    # likely that something went wrong before the trees were built. Throw the
    # error and let the caller keep all the shiny pieces.
    with pytest.raises(ZeroDivisionError) as e:
        build_remainder_tree(0, [[0]])


@pytest.mark.parametrize("build_remainder_tree", build_remainder_tree_list)
def test_build_remainder_tree_negative(build_remainder_tree):

    # If you have negative numbers in your product tree, it means you supplied
    # negative numbers in the input of your product tree. This is most likely
    # not what you want when building the remainder tree. However, it is only
    # possible to detect with additional checks of the product tree, which are
    # not performed. So, enjoy the unexpected results :(

    # If you decide to fix this behaviour by adding more checks, feel free to
    # remove this test.
    assert build_remainder_tree(0, [[-1]]) == [[0]]
    assert build_remainder_tree(1, [[-1]]) == [[0]]

    assert build_remainder_tree(0, [[-42]]) == [[0]]
    # Because this is how modulo division works in Python:
    assert build_remainder_tree(1, [[-42]]) == [[-41]]


@pytest.mark.parametrize("build_remainder_tree", build_remainder_tree_list)
def test_build_remainder_tree_single(build_remainder_tree):

    assert build_remainder_tree(0, [[1]]) == [[0]]
    assert build_remainder_tree(1, [[1]]) == [[0]]

    assert build_remainder_tree(0, [[42]]) == [[0]]
    assert build_remainder_tree(1, [[42]]) == [[1]]


@pytest.mark.parametrize("build_remainder_tree", build_remainder_tree_list)
def test_build_remainder_tree_two_levels(build_remainder_tree):

    assert build_remainder_tree(3, [[2, 3], [6]]) == [[1, 0], [3]]


@pytest.mark.parametrize("build_remainder_tree", build_remainder_tree_list)
def test_build_remainder_tree_three_levels(build_remainder_tree):

    assert build_remainder_tree(3, [[1, 2, 3], [2, 3], [6]]) == [[0, 1, 0], [1, 0], [3]]


def test_compute_remainders_empty():

    assert compute_remainders(0, []) == []


def test_compute_remainders_zero():

    # If you ask for the remainder after dividing by zero, it is your fault
    with pytest.raises(ZeroDivisionError) as e:
        compute_remainders(42, [0])


@pytest.mark.parametrize("n", [-42, -1, 1, 42])
def test_compute_remainders_single(n):

    assert compute_remainders(0, [n]) == [0]


@pytest.mark.parametrize("n", [-42, -1, 0, 1, 42])
@pytest.mark.parametrize("m", [-42, -1, 1, 42])
def test_compute_remainders_as_in_python(n, m):

    assert compute_remainders(n, [m]) == [n % m]


def test_compute_remainders_three():

    assert compute_remainders(3, [2, 3, 4]) == [1, 0, 3]


@pytest.mark.parametrize("attack_batch_gcd", attack_batch_gcd_list)
def test_attack_batch_gcd_empty(attack_batch_gcd):

    assert attack_batch_gcd([]) == []


@pytest.mark.parametrize("attack_batch_gcd", attack_batch_gcd_list)
def test_attack_batch_gcd_zero(attack_batch_gcd):

    with pytest.raises(ZeroDivisionError) as e:
        attack_batch_gcd([0])


@pytest.mark.parametrize("attack_batch_gcd", attack_batch_gcd_list)
@pytest.mark.parametrize("n", [-42, -1, 1, 42])
def test_attack_batch_gcd_single(attack_batch_gcd, n):

    # The negative values do not make any sense here, so if you change the
    # behaviour for negatives, feel free to change this test too
    assert attack_batch_gcd([n]) == [1]


@pytest.mark.parametrize("attack_batch_gcd", attack_batch_gcd_list)
def test_attack_batch_gcd_only_small_primes(attack_batch_gcd):

    assert attack_batch_gcd([2, 3, 5, 7, 997]) == [1, 1, 1, 1, 1]


@pytest.mark.parametrize("attack_batch_gcd", attack_batch_gcd_list)
def test_attack_batch_gcd_small_primes_and_products(attack_batch_gcd):

    assert attack_batch_gcd([2, 3, 6]) == [2, 3, 6]
    assert attack_batch_gcd([7, 997, 7 * 997]) == [7, 997, 7 * 997]
