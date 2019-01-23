from __future__ import division

from itertools import product

import gmpy2
from flint import fmpz_mat


def lcg_step_state(m, a, b, state, n):
    for _ in range(n):
        state = (a * state + b) % m
        yield state


def lehmer_step_state(m, a, state, n):
    for _ in range(n):
        state = (a * state) % m
        yield state


def blank_lower_bits(v, n=None):
    if n is None:
        n = v.bit_length() // 2
    return v - (v % 2 ** n)


def construct_lattice(m, a, size):
    L = [[m] + (size - 1) * [0]] + [
        ([pow(a, i, m)] + [0] * (i - 1) + [-1] + [0] * (size - i - 1))
        for i in range(1, size)
    ]
    assert len(L) == size and all([len(l) == size for l in L])
    return L


def reconstruct_lehmer_lower(L, m, ys):
    """
    Reconstructs the lower bits :math:`zs` of a system of linear congurential equations in lattice form with
    :math:`L \\cdot xs = 0 \\mod m` for solution :math:`xs`, where :math:`xs = ys + zs`.
    It works by computing a smaller basis :math:`B` from the basis :math:`L` and solving equations in the smaller basis.

    :param L: The system of linear equation in matrix form (evaluating to 0)
    :param m: The modulus used for all the equations
    :param ys: Partial solutions for the variables (xs = ys + zs)
    :return: The remaining operands of the solutions zs
    """
    L = fmpz_mat([row for row in L])
    ys = fmpz_mat([[y] for y in ys])
    B = L.lll()
    # Reducing the lattice basis L to a smaller basis B

    Bys = B * ys

    # TODO: There might be a better solution to find the individual ks
    # NB: B * (ys + zs) = m * ks for some ks
    ks = fmpz_mat([[int(round(int(x) / m))] for x in Bys])

    # We now solve the system of linear equations B zs = m * ks - B ys for zs
    Bzs = m * ks - Bys
    zs = B.solve(Bzs)
    assert all(z.denom() == 1 for z in zs)
    return [z.numer() % m for z in zs]


def retrieve_states(m, a, b, z):
    # return ((z - b) * int(gmpy2.invert(a - 1, m))) % m
    # (a - 1) * s + b = z (mod m)
    a = a - 1
    z = (z - b) % m
    # a * s = z (mod m)
    d = gmpy2.gcd(a, m)
    if z % d != 0:
        raise Exception("Cannot retrieve state")
    # (a*s)//d = z//d (mod m//d)
    a_inv = gmpy2.invert(a // d, m // d)
    return [(((z // d) * a_inv) + m // d * k) % m for k in range(0, d)]


def reconstruct_lcg_state(m, a, b, highs, shift):
    """
    :param m: The modulus used for all the equations
    :param a: The multiplier used for all the equations
    :param b: The increment used for all the equations
    :param highs: Partial solutions for the variables (xs = ys + zs)
    :param shift: Number of bits that
    :return: The remaining operands of the solutions zs
    """
    size = len(highs) - 1
    L = construct_lattice(m, a, size)

    # Compute the differences of consecutive truncated outputs
    # NB: We have two versions of every difference, because of missing carry
    delta_high_options = [
        ((y - yp) % m, (y - yp - pow(2, shift)) % m)
        for (y, yp) in zip(highs[1:], highs)
    ]
    assert size == len(delta_high_options)

    # Try every combination of delta values with or without carry
    for delta_highs in product(*delta_high_options):
        delta_highs = list(delta_highs)
        # Recover possible lower bits of (a - 1) * s + b (lehmerized states)
        delta_lows = [int(z) % m for z in reconstruct_lehmer_lower(L, m, delta_highs)]
        delta_states = [(y + z) % m for y, z in zip(delta_highs, delta_lows)]
        states = retrieve_states(m, a, b, delta_states[0])
        # TODO: Check if this state is correct by testing if it predicts the highs
        for state in states:
            if viable_lcg_state(m, a, b, state, highs, shift):
                yield state


def viable_lcg_state(m, a, b, state, highs, shift):
    """
    This predicate is true if the state is consistent with the following high outputs

    :param m: The modulus used for all the equations
    :param a: The multiplier used for all the equations
    :param b: The increment used for all the equations
    :param state:
    :param highs:
    :param shift:
    :return:
    """

    def compare(t):
        x, y = t
        return blank_lower_bits(x, shift) == y

    states = [state] + list(lcg_step_state(m, a, b, state, len(highs) - 1))
    return all(map(compare, [(x, y) for x, y in zip(states, highs)]))
