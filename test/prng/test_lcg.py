from functools import reduce

import pytest
from hypothesis import assume, example, given, settings
from hypothesis.strategies import floats, integers

from cat.prng.lcg import *
from gmpy2 import mpz, next_prime


def blank_lower_bits(v, n=None):
    if n is None:
        n = max([e.bit_length() // 2 for e in v])
    return [x - (x % 2 ** n) for x in v]


def test_reconstruct_lower_bits_sanity():
    m = 4_294_967_291
    a = 598_176_085
    s = 252_291_025
    L = [[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]]
    xs = [1_477_951_715, 3_597_964_208, 2_802_631_510, 3_169_049_466]
    ys = blank_lower_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)
    assert zs == [49379, 37808, 50006, 56186]


def test_reconstruct_lower_bits_few_outputs():
    m = int(next_prime(2 ** 64))
    a = int(next_prime(2 ** 30))
    s = 252_291_025
    shift = 64 - 32
    size = 2

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    # Only two states should not be able to predictable (even information theoretically?)
    assert xs[0] != (ys[0] + zs[0]) % m
    assert all((x != y + z % m) for x, y, z in zip(xs, ys, zs))


def test_reconstruct_lower_bits_few_bits():
    m = int(next_prime(2 ** 512))
    a = int(next_prime(2 ** 128))
    s = 252_291_025
    shift = 512 - 32
    size = 15

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    # Only a few bits should not be able to predictable (even information theoretically?)
    assert xs[0] != (ys[0] + zs[0]) % m
    assert all((x != y + z % m) for x, y, z in zip(xs, ys, zs))


@settings(max_examples=500)
@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_30(s):
    m = int(next_prime(2 ** 32))
    a = int(next_prime(2 ** 30))
    s %= m
    shift = 32 - 16
    size = 20

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_glibc_params(s):
    a = 1_103_515_245
    # b = 12345
    m = 2 ** 32
    s %= m
    shift = 32 - 16
    size = 5

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_java_params(s):
    m = 2 ** 48
    a = 0x5DEECE66D
    # b = 0xbl
    s %= m
    shift = 48 - 16
    size = 5

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_60(s):
    m = int(next_prime(2 ** 64))
    a = int(next_prime(2 ** 32))
    s %= m
    shift = 64 - 16
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_128(s):
    m = int(next_prime(2 ** 128))
    a = int(next_prime(2 ** 64))
    s %= m
    shift = 128 - 64
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
@pytest.mark.slow
def test_reconstruct_lower_bits_prime_512(s):
    m = int(next_prime(2 ** 512))
    a = int(next_prime(2 ** 256))
    s %= m
    shift = 512 - 256 - 128
    size = 15

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = blank_lower_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


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

    recovered_ys = reconstruct_lower_bits(L, m, zs)

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

    recovered_ys = reconstruct_lower_bits(L, m, zs)

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
    zs = reconstruct_lower_bits(L, m, lehmer_style_lcg)
    z_prime = retrieve_state(m, a, b, zs[0])

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

    def _generate(state):
        for i in range(size):
            yield state  # TODO: dump the state after updating?
            state = (a * state + b) % m

    xs = list(_generate(s))
    ys = blank_lower_bits(xs, shift)

    lehmer_style_lcg = [(xp - x) % m for xp, x in zip(xs[1:], xs)]
    # yprimes = [[(y - yp) % m, (y - yp - pow(2, shift)) % m] for (y, yp) in zip(ys[1:], ys)]
    blanked = blank_lower_bits(lehmer_style_lcg, shift)
    yprimes = [
        [(y - yp) % m, (y - yp - pow(2, shift)) % m] for (y, yp) in zip(ys[1:], ys)
    ]
    print("Blanked in guessed? {}".format(tuple(blanked) in product(*yprimes)))

    # print(f'ACTUAL   {blanked[0]:032b}')
    # print(f'PROPOSE1 {yprimes[0][0]:032b}')
    # print(f'PROPOSE2 {yprimes[0][1]:032b}')
    # pyp = list(product(*yprimes))
    # if tuple(blanked) in pyp:
    #    print(pyp)
    #    print(lehmer_style_lcg)
    # recovered_zs = reconstruct_initial_state(m, a, b, ys, shift)

    L = construct_lattice(m, a, size - 1)  # DONTCOPY
    recovered_zs = [
        int(y + z) % m
        for y, z in zip(blanked, reconstruct_lower_bits(L, m, list(blanked)))
    ]

    lehmer_init_states = [(a ** i * (a - 1) * s + b) % m for i in range(10)]
    recovered_state = retrieve_state(m, a, b, recovered_zs[0])
    print("Lehmer real: {}".format(lehmer_init_states))
    print("Recovered: {}".format(recovered_zs))
    print("Intersection: {}".format(set(lehmer_init_states) & set(recovered_zs)))
    print("")
    assert s in recovered_state
    # assert xs[0] == (ys[0] + zs[0]) % m
    # assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))
