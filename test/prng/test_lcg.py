from functools import reduce

import pytest
from hypothesis import assume, example, given, settings
from hypothesis.strategies import floats, integers

from cat.prng.lcg import *
from gmpy2 import mpz, next_prime


def glibc_params():
    return (
        2 ** 32,  # m
        1103515245,  # a
        12345,  # b
        16,  # shift
        10,  # number of samples
    )


def java_params():
    return (
        2 ** 48,  # m
        0x5DEECE66D,  # a
        0xB,  # b
        48 - 16,  # shift
        10,  # number of samples
    )


def prime_params():
    return (
        int(next_prime(2 ** 128)),  # m
        int(next_prime(2 ** 64)),  # a
        int(next_prime(2 ** 32)),  # b
        64,  # shift
        10,  # number of samples
    )


def non_prime_params():
    return (
        (2 ** 32) - 1,  # m
        1103515216,  # a
        4312,  # b
        16,  # shift
        10,  # number of samples
    )


def few_bit_params():
    return (
        2 ** 32,  # m
        1103515245,  # a
        12345,  # b
        28,  # shift, only 4 bits of output
        25,  # number of samples
    )


@pytest.fixture(
    params=[
        32,
        64,
        128,
        256,
        glibc_params,
        java_params,
        prime_params,
        non_prime_params,
        pytest.param(few_bit_params, marks=pytest.mark.xfail(reason="too hard?")),
    ]
)
def rng_params(request):
    if isinstance(request.param, int):
        n = request.param
        m = int(next_prime(2 ** n))
        a = int(next_prime(2 ** (n // 2)))
        # Chosen by fair dice roll
        b = (2 ** (n // 4)) + 4
        shift = n // 2
        sample_size = 5 if n < 128 else 20

        yield (m, a, b, shift, sample_size)
    else:
        yield request.param()


@settings(max_examples=500)
@example(s=252291025)
# TODO: Breaking examples, find out why?
@example(s=25537)
@example(s=20460)
@example(s=3588)
@given(integers(2))
def test_reconstruct_lehmer_lower(rng_params, s):
    m, a, b, shift, size = rng_params
    s %= m

    def _generate_lehmer_states(state):
        for i in range(size):
            state = (a * state) % m
            yield state

    states = list(_generate_lehmer_states(s))
    higher = [blank_lower_bits(state, shift) for state in states]
    L = construct_lattice(m, a, size)
    lower = reconstruct_lehmer_lower(L, m, higher)

    diff = states[0] - ((higher[0] + lower[0]) % m)
    assert diff == 0
    assert states[0] == (higher[0] + lower[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(states, higher, lower))


@settings(max_examples=500)
@example(s=252291025)
@given(integers(2))
def test_reconstruct_lcg_lower(rng_params, s):
    m, a, b, shift, size = rng_params
    s %= m

    def _generate_lcg_states(state):
        for i in range(size):
            state = (a * state + b) % m
            yield state

    states = list(_generate_lcg_states(s))
    higher = [blank_lower_bits(state, shift) for state in states]
    candidate_state = next(reconstruct_lcg_state(m, a, b, higher, shift))

    assert states[0] == candidate_state


@given(integers(2))
def test_reconstruct_lehmer_lower_few_outputs(rng_params, s):
    m, a, b, shift, size = rng_params
    s %= m
    size = 1

    def _generate_lehmer_states(state):
        for i in range(size):
            state = (a * state) % m
            yield state

    states = list(_generate_lehmer_states(s))
    higher = [blank_lower_bits(state, shift) for state in states]
    L = construct_lattice(m, a, size)
    lower = reconstruct_lehmer_lower(L, m, higher)

    # TODO: Maybe throw an exception for to few states?
    assert states[0] != (higher[0] + lower[0]) % m
    assert all((x != y + z % m) for x, y, z in zip(states, higher, lower))


def test_reconstruct_lehmer_lower_few_bits():
    m = int(next_prime(2 ** 256))
    a = int(next_prime(2 ** 128))
    s = 252291025
    shift = 256 - 16
    size = 15

    def _generate_lehmer_states(state):
        for i in range(size):
            state = (a * state) % m
            yield state

    states = list(_generate_lehmer_states(s))
    higher = [blank_lower_bits(state, shift) for state in states]
    L = construct_lattice(m, a, size)
    lower = reconstruct_lehmer_lower(L, m, higher)

    # Only a few bits should not be able to predictable
    assert states[0] != (higher[0] + lower[0]) % m
    assert all((x != y + z % m) for x, y, z in zip(states, higher, lower))


@example(s=252291025)
@given(integers(2))
def test_viable_lcg_state(rng_params, s):
    m, a, b, shift, size = rng_params
    s %= m

    def _generate_lcg_states(state):
        for i in range(size):
            state = (a * state + b) % m
            yield state

    states = list(_generate_lcg_states(s))
    higher = [blank_lower_bits(state, shift) for state in states]

    assert viable_lcg_state(m, a, b, states[0], higher, shift) == True
