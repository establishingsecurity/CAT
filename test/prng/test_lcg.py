from hypothesis import assume, example, given, settings
from hypothesis.strategies import floats, integers

from cat.prng.lcg import *
from gmpy2 import mpz, next_prime


def test_reconstruct_lower_bits_sanity():
    m = 4_294_967_291
    a = 598_176_085
    s = 252_291_025
    L = [[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]]
    xs = [1_477_951_715, 3_597_964_208, 2_802_631_510, 3_169_049_466]
    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)
    assert zs == [49379, 37808, 50006, 56186]


@settings(max_iterations=10000)
@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_30(s):
    m = int(next_prime(2 ** 32))
    a = int(next_prime(2 ** 30))
    size = 20

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_glibc_params(s):
    a = 1_103_515_245
    # b = 12345
    m = 2 ** 32
    shift = 16
    size = 5

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_java_params(s):
    a = 0x5DEECE66D
    # b = 0xbl
    m = 2 ** 48
    shift = 16
    size = 5

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, shift)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@settings(max_iterations=10000)
@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_60(s):
    m = int(next_prime(2 ** 64))
    a = int(next_prime(2 ** 32))
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@settings(max_iterations=10000)
@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_128(s):
    m = int(next_prime(2 ** 128))
    a = int(next_prime(2 ** 64))
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))


@settings(max_iterations=10000)
@example(s=252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_512(s):
    m = int(next_prime(2 ** 512))
    a = int(next_prime(2 ** 256))
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, 128)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m
    assert all((x == y + z % m) for x, y, z in zip(xs, ys, zs))
