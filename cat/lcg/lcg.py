from fpylll import IntegerMatrix, LLL
import numpy as np
from gmpy2 import mpz
from sympy import solveset, S, symbols, Matrix


def matrix_to_fplll(matrix):
    assert len(matrix.shape) == 2
    rv = IntegerMatrix(*matrix.shape)
    for i, row in enumerate(matrix):
        for j, elem in enumerate(row):
            rv[i, j] = int(elem)
    return rv


def fplll_to_matrix(matrix):
    return np.array([list(map(mpz, row)) for row in matrix], dtype=object)


def reconstruct_lower_bits(L, m, ys):
    B = fplll_to_matrix(LLL.reduction(matrix_to_fplll(L)))
    Bys = B.dot(ys)
    assert np.array_equal(Bys, [-326409191424, -1125261508608, -876166381568, -339302678528])
    ks = np.array([round(x) for x in Bys / m])
    assert np.array_equal(ks, [-76, -262, -204, -79])
    Bzs = m * ks - Bys
    assert np.array_equal(Bzs, np.array([-8322692, -19921634, -6945796, 262539]))
    B = Matrix(B)
    Bzs = Matrix(Bzs)
    # print(B, Bzs)
    # zs = lu_solve(B, Bzs)
    # res = residual(B, zs, Bzs)
    zs = B.solve(Bzs)
    assert B @ zs == Bzs
    #assert B @ Matrix([49379, 37808, 50006, 56186]) == np.array([-8322692, -19921634, -6945796, 262539])
    return np.array(list(map(int, zs)))


def get_upper_bits(v, n=None):
    if n is None:
        n = max([e.bit_length() // 2 for e in v])
    return [x - x % 2 ** n for x in v]


def test_reconstruct_lower_bits():
    m = 4294967291
    a = 598176085
    s = 252291025
    L = np.array([[m, 0, 0, 0], [a, -1, 0, 0], [a ** 2, 0, -1, 0], [a ** 3, 0, 0, -1]])
    xs = np.array([1477951715, 3597964208, 2802631510, 3169049466])
    ys = get_upper_bits(xs, 16)
    assert np.array_equal(ys, [1477902336, 3597926400, 2802581504, 3168993280])
    zs = reconstruct_lower_bits(L, m, ys)
    expected_zs = xs - ys
    assert np.array_equal(expected_zs, [49379, 37808, 50006, 56186])
    assert np.array_equal(zs, expected_zs)
    assert np.array_equal(xs, (ys + zs))
