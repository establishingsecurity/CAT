#!/usr/bin/env python

import functools
import operator


def compute_product(xs):
    """Computes a (somewhat) fast product of all list elements."""

    return _compute_product_1(xs)


def _compute_product_0(xs):
    """Uses built-in Python tools to compute the product of the list."""

    return functools.reduce(operator.mul, xs)


def _compute_product_1(xs):
    """
    Uses the idea behind the product tree to compute the product of the list.
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

    Example:
        TODO
    """

    return _build_product_tree_0(xs)


def _build_product_tree_0(xs):

    if not xs:
        return [[0]]

    step = 0
    tree = [xs]

    while len(tree[step]) != 1:
        level = tree[step]

        tree.append(
            [level[i - 1] * level[i] for i in range(1, len(level), 2)]
        )

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
