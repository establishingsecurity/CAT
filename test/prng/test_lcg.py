from sympy import Matrix

from cat.prng.lcg import *
from hypothesis import given, assume, example
from hypothesis.strategies import integers, floats


def test_reconstruct_lower_bits_sanity():
    m = 4294967291
    a = 598176085
    s = 252291025
    L = Matrix([[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]])
    xs = Matrix([1477951715, 3597964208, 2802631510, 3169049466])
    ys = Matrix(get_upper_bits(xs, 16))
    assert ys == Matrix([1477902336, 3597926400, 2802581504, 3168993280])
    zs = reconstruct_lower_bits(L, m, ys)
    expected_zs = Matrix(xs - ys)
    assert expected_zs == Matrix([49379, 37808, 50006, 56186])
    assert zs == expected_zs
    assert xs == (ys + zs)

def test_reconstruct_lower_bits_sanity_flint():
    m = 4294967291
    a = 598176085
    s = 252291025
    L = [[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]]
    xs = [1477951715, 3597964208, 2802631510, 3169049466]
    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits_flint(L, m, ys)
    assert zs.table() == [[49379], [37808], [50006], [56186]]

@example(m=406, a=2, s=1, bits_proportion=0.5)
@given(integers(0), integers(2), integers(), floats(1 / 2, 1))
def test_reconstruct_lower_bits(m, a, s, bits_proportion):
    assume(a < m and s < m)
    nbits = int(m.bit_length() * bits_proportion)
    assume(nbits > 2)
    L = Matrix([[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]])
    xs = Matrix([(a ** (i + 1) * s) % m for i in range(4)])
    ys = Matrix(get_upper_bits(xs, nbits))
    zs = reconstruct_lower_bits(L, m, ys)
    expected_zs = Matrix(xs - ys)
    print(zs, expected_zs)
    assert xs == (ys + zs)
    assert zs == expected_zs
