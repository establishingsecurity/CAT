from fpylll import LLL, IntegerMatrix

from sympy import Matrix


def matrix_to_fplll(matrix):
    assert len(matrix.shape) == 2
    rv = IntegerMatrix(*matrix.shape)
    for i, elem in enumerate(matrix):
        rv[i // matrix.shape[0], i % matrix.shape[1]] = int(elem)  # TODO CHECK
    return rv


def fplll_to_matrix(matrix):
    return Matrix([[*row] for row in matrix])


def reconstruct_lower_bits(L, m, ys):
    """
    Reconstructs the lower bits of a system of linear congurential equations in lattice form with
    L * xs = 0 mod m for solution xs.
    It works by computing a smaller basis B from the basis L and solving equations in the smaller basis

    :param L: The system of linear equation in matrix form (evaluating to 0)
    :param m: The modulus used for all the equations
    :param ys: Partial solutions for the variables (xs = ys + zs)
    :return: The remaining operands of the solutions zs
    """
    # Reducing the lattice basis L to a smaller basis B
    B = fplll_to_matrix(LLL.reduction(matrix_to_fplll(L)))

    Bys = Matrix(B @ ys)

    # TODO: There might be a better solution to find the individual ks
    # NB: B * (ys + zs) = m * ks for some ks
    ks = Matrix([round(x) for x in Bys / m])

    # We know solve the system of linear equations B zs = m * ks - B ys for zs
    Bzs = Matrix(m * ks - Bys)
    zs = B.solve(Bzs)
    assert B @ zs == Bzs
    return Matrix(zs)


def get_upper_bits(v, n=None):
    if n is None:
        n = max([e.bit_length() // 2 for e in v])
    return [x - x % 2 ** n for x in v]


