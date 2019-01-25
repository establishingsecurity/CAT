import re

import requests
from cat.prng.lcg import reconstruct_lcg_state, lcg_step_state
from gmpy2 import mpz, mpz_random, next_prime, random_state

# Define rng parameters
STATE_SIZE = 8192
MODULUS = 2**STATE_SIZE - 1
MULTIPLIER = int(next_prime(2 ** (STATE_SIZE // 2)))
INCREMENT = int(next_prime(2 ** (STATE_SIZE // 4)))
SHIFT = STATE_SIZE // 2

SAMPLES = 10

PORT = 8080


def get_number():
    r = requests.get("http://localhost:{}".format(PORT))
    m = re.search(r"(?<=<body>)\w+", r.text)
    return int(m.group(0)) << SHIFT


if __name__ == "__main__":
    highs = [get_number() for _ in range(SAMPLES)]
    state = int(next((reconstruct_lcg_state(MODULUS, MULTIPLIER, INCREMENT, highs, SHIFT))))
    print("Original state: {}".format(state))
    states = [int(x) for x in lcg_step_state(MODULUS, MULTIPLIER, INCREMENT, state, 2 * SAMPLES)]
    from pprint import pprint
    print("Next states:")
    pprint((states[SAMPLES-1:]))
    print("Next outputs:")
    pprint(list(map(lambda x: x >> SHIFT, states[SAMPLES-1:])))

