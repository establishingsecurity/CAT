from cat.prng.lcg import construct_lattice, reconstruct_lower_bits
from gmpy2 import mpz, mpz_random, next_prime, random_state

# Define rng parameters
bits = 128
m = int(next_prime(2 ** bits))
a = int(next_prime(2 ** (bits // 2)))
s = int(mpz_random(random_state(), m))
shift = bits // 2
size = 10


def attack(m, a, ys):
    # Constructing lattice for the modular relations
    L = construct_lattice(m, a, len(ys))
    # Reconstructing the missing state
    zs = reconstruct_lower_bits(L, m, ys)
    # Returning the full reconstructed state
    return [y + z for y, z in zip(ys, zs)]


def lehmer_random(s):
    return a * s % m


if __name__ == "__main__":

    # Use Lehmer Style to generate size "random" states and
    # blank the lower shift (=256) bits of the state, to generate the output
    xs = []
    ys = []
    for i in range(size):
        s = lehmer_random(s)
        xs.append(s)
        ys.append(s - (s % 2 ** shift))
        print("Next State:\t{}\n|- Output:\t{}".format(hex(xs[-1]), hex(ys[-1])))

    print("\nStarting attack...\n")
    reconstructed = attack(m, a, ys)

    for (i, (x, y, r)) in enumerate(zip(xs, ys, reconstructed)):
        print(
            "Reconstruction of state {}:\n  {:032x}\n= {:032x}\n+ {:032x}".format(
                i, int(x), int(y), int(r - y)
            )
        )

    assert reconstructed[0] == xs[0]
    assert reconstructed == xs
    print("Everything reconstructed")
