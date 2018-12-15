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
@example(s = 252_291_025)
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

@settings(max_iterations=10000)
@example(s = 252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_60(s):
    m = int(next_prime(2 ** 64))
    a = int(next_prime(2 ** 60))
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m

@settings(max_iterations=10000)
@example(s = 252_291_025)
@given(integers(2))
def test_reconstruct_lower_bits_prime_128(s):
    m = int(next_prime(2 ** 128))
    a = int(next_prime(2 ** 120))
    size = 10

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    L = construct_lattice(m, a, size)

    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)

    assert xs[0] == (ys[0] + zs[0]) % m

@settings(max_iterations=10000)
@given(integers(2), integers(2), floats(1 / 2, 1))
def test_reconstruct_lower_bits(m, s, bits_proportion):
    assume(s < m)
    m = int(next_prime(m))
    a = 2
    size = 25
    nbits = int(m.bit_length() * bits_proportion)

    L = [[m] + (size - 1) * [0]] + [
        ([pow(a, i, m)] + [0] * (i - 1) + [-1] + [0] * (size - i - 1))
        for i in range(1, size)
    ]
    assert len(L) == size and all([len(l) == size for l in L])

    xs = [(a ** i * s) % m for i in range(1, size + 1)]
    assert len(xs) == size

    ys = get_upper_bits(xs, nbits)
    # ys can't be 0
    assume(all(y != 0 for y in ys))
    zs = [(x - y) % m for x, y in zip(xs, ys)]
    recovered_zs = reconstruct_lower_bits(L, m, ys)

    if xs[0] != (ys[0] + recovered_zs[0]) % m:
        print()
        print(f"m = {m}, a = {a}, s={a}")
        print(
            f"x_0 = {xs[0]}, y_0 = {ys[0]} + rz_0={recovered_zs[0]} = {ys[0] + recovered_zs[0]},"
        )
        print(zs)
        print(recovered_zs)
    assert xs[0] == (ys[0] + recovered_zs[0]) % m
