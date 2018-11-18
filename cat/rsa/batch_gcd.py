#!/usr/bin/env python

import functools
import math
import operator


def compute_product(xs):
    """Computes a (somewhat) fast product of all list elements."""

    return _compute_product_1(xs)


def _compute_product_0(xs):
    """Uses built-in Python tools to compute the product of the list."""

    if not xs:
        return 0

    return functools.reduce(operator.mul, xs)


def _compute_product_1(xs):
    """
    Uses the idea behind the product tree to compute the product of the list.

    TODO:
        - Link to build_product_tree and its implementation for details
    """

    if not xs:
        return 0

    while len(xs) != 1:

        x = xs[-1] if len(xs) % 2 else None

        xs = [xs[i - 1] * xs[i] for i in range(1, len(xs), 2)]

        if x is not None:
            xs.append(x)

    return xs[0]


def build_product_tree(xs):
    """
    Builds a product tree where the root is the product of all the leaves.

    This tree is a Python list where each element is itself a list of numbers.
    The inner lists each correspond to a level in the product tree. The first
    list holds the leaves and the last list is a one-element list that holds the
    root of the tree.

    TODO:
        - Provide an example
        - Describe the inputs
        - Think about returned value for the empty list input. It is currently
        [[0]] because the default value for product of empty list is 0. This
        value will also affect build_remainder_tree below.
    """

    return _build_product_tree_0(xs)


def _build_product_tree_0(xs):

    if not xs:
        return [[0]]

    step = 0
    tree = [xs]

    while len(tree[step]) != 1:
        level = tree[step]

        # range(1, ...) guarantees that both level[i - 1] and level[i] exist
        # range(0, ...) does *not* guarantee that level[i + 1] exists
        tree.append([level[i - 1] * level[i] for i in range(1, len(level), 2)])

        # if the last element of this level did not participate in building the
        # next level, just carry it over into the next level unchanged
        if len(level) % 2:
            tree[-1].append(level[-1])

        step += 1

    return tree


def _build_product_tree_1(xs):

    if not xs:
        return [[0]]

    tree = [xs]

    while len(tree[-1]) != 1:
        tree.append([
            functools.reduce(operator.mul, tree[-1][2 * i : 2 * i + 2])
            for i in range((len(tree[-1]) + 1) // 2)
        ])

    return tree


def build_remainder_tree(n, product_tree):
    """
    Builds a remainder tree that has the same shape as the product tree.

    For every element :code:`p` of the product tree, the remainder tree contains
    the value of :code:`n % p` at the same position.

    The remainder tree relies on the following property:

    .. math::
            n \mod x = (n \mod xy) \mod x

    Args:
        n (Int): the divident
        product_tree (List[List[Int]]): the tree of divisors
    """

    return _build_remainder_tree_0(n, product_tree)


def _build_remainder_tree_0(n, product_tree):

    # Compute the root of the remainder tree separately:
    tree = [[n % product_tree[-1][0]]]

    for step, product_level in enumerate(reversed(product_tree[:-1]), 0):

        # Take the previous level of the remainder tree
        level = tree[step]

        tree.append(
            [level[i // 2] % product_level[i] for i in range(len(product_level))]
        )

    # Since the product tree has its root as the last element of the list, make
    # remainder tree have its root as the last element too by reversing it:
    return list(reversed(tree))


def compute_remainders(n, xs):
    """
    Computes remainders n % xs[i] for each i in range(0, len(xs)).

    Uses a product tree and a remainder tree to speed up computations.

    TODO:
        - Describe inputs
        - Cross-reference product tree/remainder tree
    """

    if not xs:
        return []

    return build_remainder_tree(n, build_product_tree(xs))[0]


def attack_batch_gcd(ns):
    """
    Checks for each RSA modulus if it shares primes with another RSA modulus.

    Args:
        ns List[Int]: a list where each element is an RSA modulus

    Returns:
        List[Int]: a list where each position is either one (i.e. the modulus
            from that position in the input list does not share any primes with
            any other modulus from the input list) or greater than one. If the
            value is not one, than it is likely the prime itself or the product
            of two (?) primes.
    """

    return _attack_batch_gcd_0(ns)


def _attack_batch_gcd_0(ns):

    rs = compute_remainders(compute_product(ns), [n ** 2 for n in ns])

    return [math.gcd(r // n, n) for r, n in zip(rs, ns)]


def _attack_batch_gcd_1(ns):
    """
    This is a speed-up from https://facthacks.cr.yp.to/batchgcd.html

    They claim that "the nodes of the product tree used inside the remainder
    tree in the second step are simply the squares of the nodes in the product
    tree used in the first step"
    """

    tree = build_product_tree(ns)

    rs = tree.pop()

    while tree:
        ns = tree.pop()

        rs = [rs[i // 2] % ns[i] ** 2 for i in range(len(ns))]

    return [math.gcd(r // n, n) for r, n in zip(rs, ns)]


if __name__ == '__main__':

    import timeit

    # NOTE: ~20 seconds
    print(
        timeit.timeit(
            '_compute_product_0(list(range(1, 10000)))',
            setup='from __main__ import _compute_product_0',
            number=1000
        )
    )

    # NOTE: ~5 seconds
    print(
        timeit.timeit(
            '_compute_product_1(list(range(1, 10000)))',
            setup='from __main__ import _compute_product_1',
            number=1000
        )
    )

    # NOTE: ~5 seconds
    print(
        timeit.timeit(
            '_build_product_tree_0(list(range(1, 10000)))',
            setup='from __main__ import _build_product_tree_0',
            number=1000
        )
    )

    # NOTE: ~9 seconds
    print(
        timeit.timeit(
            '_build_product_tree_1(list(range(1, 10000)))',
            setup='from __main__ import _build_product_tree_1',
            number=1000
        )
    )
