from fpylll import IntegerMatrix, LLL
from sympy import Matrix


def matrix_to_fplll(matrix):
    assert len(matrix.shape) == 2
    print(matrix.shape)
    rv = IntegerMatrix(*matrix.shape)
    for i, elem in enumerate(matrix):
        rv[i // matrix.shape[0], i % matrix.shape[1]] = int(elem)  # TODO CHECK
    return rv


def fplll_to_matrix(matrix):
    return Matrix([[*row] for row in matrix])


def reconstruct_lower_bits(L, m, ys):
    B = fplll_to_matrix(LLL.reduction(matrix_to_fplll(L)))
    Bys = Matrix(B @ ys)
    ks = Matrix([round(x) for x in Bys / m])
    Bzs = m * ks - Bys
    B = Matrix(B)
    Bzs = Matrix(Bzs)
    zs = B.solve(Bzs)
    assert B @ zs == Bzs
    return Matrix(zs)


def get_upper_bits(v, n=None):
    if n is None:
        n = max([e.bit_length() // 2 for e in v])
    return [x - x % 2 ** n for x in v]


def test_reconstruct_lower_bits():
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
