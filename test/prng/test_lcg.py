from cat.prng.lcg import *
from hypothesis import given, assume, example
from hypothesis.strategies import integers, floats


def test_reconstruct_lower_bits_sanity():
    m = 4294967291
    a = 598176085
    s = 252291025
    L = [[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]]
    xs = [1477951715, 3597964208, 2802631510, 3169049466]
    ys = get_upper_bits(xs, 16)
    zs = reconstruct_lower_bits(L, m, ys)
    assert zs == [49379, 37808, 50006, 56186]


@given(integers(3), integers(2), integers(2), floats(1 / 2, 1))
def test_reconstruct_lower_bits(m, a, s, bits_proportion):
    assume(a < m and s < m)
    nbits = int(m.bit_length() * bits_proportion)
    L = [[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2 % m, 0, -1, 0], [a ** 3 % m, 0, 0, -1]]
    xs = [(a ** (i + 1) * s) % m for i in range(4)]
    ys = get_upper_bits(xs, nbits)
    zs = [(x - y) % m for x, y in zip(xs, ys)]
    recovered_zs = reconstruct_lower_bits(L, m, ys)
    # assert zs.table() == expected_zs
    s_prime = int(recovered_zs[0] + ys[0])
    if s_prime == s:
        # Test pass, the seed is correct
        return
    print("s' - s = ", s_prime - s)
    print(f"m={m}, a={a}, s={s}")
    xs_prime = [(a ** i * s_prime) % m for i in range(4)]
    zs_prime = [(x - y) % m for x, y in zip(xs_prime, get_upper_bits(xs_prime, nbits))]
    print("Actual Expect:", zs)
    print("Actual    Got:", recovered_zs)
    assert zs == recovered_zs
    print("Expect:", zs_prime, "Got:", recovered_zs)
    assert zs_prime == recovered_zs
