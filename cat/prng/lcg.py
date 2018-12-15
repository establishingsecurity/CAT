from flint import fmpz_mat


def construct_lattice(m, a, size):
    L = [[m] + (size - 1) * [0]] + [
        ([pow(a, i, m)] + [0] * (i - 1) + [-1] + [0] * (size - i - 1))
        for i in range(1, size)
    ]
    assert len(L) == size and all([len(l) == size for l in L])
    return L

def reconstruct_lower_bits(L, m, ys):
    """
    Reconstructs the lower bits :math:`zs` of a system of linear congurential equations in lattice form with
    :math:`L \cdot xs = 0 \mod m` for solution :math:`xs`, where :math:`xs = ys + zs`.
    It works by computing a smaller basis :math:`B` from the basis :math:`L` and solving equations in the smaller basis.

    :param L: The system of linear equation in matrix form (evaluating to 0)
    :param m: The modulus used for all the equations
    :param ys: Partial solutions for the variables (xs = ys + zs)
    :return: The remaining operands of the solutions zs
    """
    L = fmpz_mat([[*row] for row in L])
    ys = fmpz_mat([[y] for y in ys])
    B = L.lll()
    # Reducing the lattice basis L to a smaller basis B

    Bys = B * ys

    # TODO: There might be a better solution to find the individual ks
    # NB: B * (ys + zs) = m * ks for some ks
    ks = fmpz_mat([[round(int(x) / m)] for x in Bys])

    # We know solve the system of linear equations B zs = m * ks - B ys for zs
    Bzs = m * ks - Bys
    zs = B.solve(Bzs)
    assert all(z.denom() == 1 for z in zs)
    return [z.numer() % m for z in zs]


def get_upper_bits(v, n=None):
    if n is None:
        n = max([e.bit_length() // 2 for e in v])
    return [x - (x % 2 ** n) for x in v]
