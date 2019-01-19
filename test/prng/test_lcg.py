from functools import reduce

import pytest
from hypothesis import assume, example, given, settings
from hypothesis.strategies import floats, integers

from cat.prng.lcg import *
from gmpy2 import mpz, next_prime


def glibc_params():
    return (
        2 ** 32,  # m
        1_103_515_245,  # a
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


@pytest.fixture(
    scope="module", params=[32, 64, 128, 256, glibc_params, java_params, prime_params]
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


def test_reconstruct_lehmer_lower_sanity():
    m = 4_294_967_291
    a = 598_176_085
    s = 252_291_025
    L = [[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]]
    xs = [1_477_951_715, 3_597_964_208, 2_802_631_510, 3_169_049_466]
    ys = [blank_lower_bits(x, 16) for x in xs]
    zs = reconstruct_lehmer_lower(L, m, ys)
    assert zs == [49379, 37808, 50006, 56186]


@settings(max_examples=500)
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
    candidate_states = reconstruct_lcg_state(m, a, b, higher, shift)

    assert states[0] in candidate_states


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
    s = 252_291_025
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


@given(integers(2))
@pytest.mark.xfail(reason="Reconstructing upper bits is experimental")
def test_reconstruct_upper_bits_prime_64(s):
    m = int(next_prime(2 ** 64))
    a = 2
    size = 10
    xs = [(a ** i * s) % m for i in range(1, size + 1)]

    ys = blank_lower_bits(xs, 32)
    zs = [x - y for x, y in zip(xs, ys)]
    L = construct_lattice(m, a, size)

    recovered_ys = reconstruct_lehmer_lower(L, m, zs)

    assert xs[0] == (recovered_ys[0] + zs[0]) % m


@given(integers(2))
@pytest.mark.xfail(reason="Reconstructing upper bits is experimental")
def test_reconstruct_upper_bits_prime_512(s):
    m = int(next_prime(2 ** 512))
    a = int(next_prime(2 ** 256))
    size = 10
    xs = [(a ** i * s) % m for i in range(1, size + 1)]

    ys = blank_lower_bits(xs, 384)
    zs = [x - y for x, y in zip(xs, ys)]
    L = construct_lattice(m, a, size)

    recovered_ys = reconstruct_lehmer_lower(L, m, zs)

    assert xs[0] == (recovered_ys[0] + zs[0]) % m


@given(integers(2))
@pytest.mark.xfail()
def test_reconstruct_lower_bits_prime_30_with_constant(s):
    """
    TODO: fixme
    """
    m = int(next_prime(2 ** 32))
    a = int(next_prime(2 ** 30))
    b = int(next_prime(2 ** 10))
    s %= m
    shift = 32 - 16
    size = 20

    def _generate(state):
        for i in range(size):
            state = (a * state + b) % m
            yield state

    xs = list(_generate(s))
    L = construct_lattice(m, a, size - 1)

    ys = blank_lower_bits(xs, shift)
    lehmer_style_lcg = [xp - x for xp, x in zip(ys[1:], ys)]
    zs = reconstruct_lehmer_lower(L, m, lehmer_style_lcg)
    z_prime = retrieve_states(m, a, b, zs[0])

    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))
    assert xs[0] == (ys[0] + z_prime) % m


@example(s=252_291_025)
@given(integers(2))
def test_predict_lcg_glibc_params(s):
    a = 1_103_515_245
    b = 12345
    m = 2 ** 32
    s %= m
    shift = 32 - 16
    size = 5

    def _generate_lcg_states(state):
        for i in range(size):
            state = (a * state + b) % m
            yield state

    states = list(_generate_lcg_states(s))
    higher = blank_lower_bits(states, shift)

    recovered_state = reconstruct_lcg_state(m, a, b, higher, shift)
    assert states[0] in recovered_state


@example(s=252_291_025)
@given(integers(2))
def test_viable_lcg_state_glibc_params(s):
    a = 1_103_515_245
    b = 12345
    m = 2 ** 32
    s %= m
    shift = 32 - 16
    size = 5

    def _generate_lcg_states(state):
        for i in range(size):
            state = (a * state + b) % m
            yield state

    states = list(_generate_lcg_states(s))
    higher = blank_lower_bits(states, shift)

    assert viable_lcg_state(m, a, b, states[0], higher[-1], shift)
