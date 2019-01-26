import re

import requests
from tqdm import tqdm

from cat.prng.lcg import lcg_step_state, reconstruct_lcg_state
from lottery import INCREMENT, MODULUS, MULTIPLIER, SHIFT, STATE_SIZE

# Hollywood Mode
SAMPLES = 300

# This suffices too
# SAMPLES = 10

PORT = 8080


def get_numbers():
    r = requests.get("http://localhost:{}".format(PORT))
    matches = re.findall(r'(?<=<span class="number">)\w+', r.text)
    return [int(n, 16) << SHIFT for n in matches]


if __name__ == "__main__":
    print("Retrieving samples")
    # Get SAMPLES outputs
    highs_mat = [get_numbers() for _ in range(SAMPLES)]

    # Transpose the output matrix for easier usage
    highs_mat = [*zip(*highs_mat)]

    print("Reconstructing states")
    # Reconstruct the original state for each LCG in the samples
    states = [
        int(next(reconstruct_lcg_state(MODULUS, MULTIPLIER, INCREMENT, highs, SHIFT)))
        for highs in tqdm(highs_mat)
    ]

    # Step the LCGs to the next step, effectivly predicting the next value
    states = [
        int(list(lcg_step_state(MODULUS, MULTIPLIER, INCREMENT, state, SAMPLES))[-1])
        for state in states
    ]

    print("Your next lottery numbers are:")
    for n in states:
        print("{:02X}".format(n >> SHIFT), end=" ")
    print()
