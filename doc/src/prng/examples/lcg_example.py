import re
import time

import requests

from cat.prng.lcg import lcg_step_state, reconstruct_lcg_state
from lottery import INCREMENT, MODULUS, MULTIPLIER, SHIFT, STATE_SIZE

SAMPLES = 15

PORT = 8080


def get_numbers():
    r = requests.get("http://localhost:{}".format(PORT))
    matches = re.findall(r'(?<=<span class="number">)\w+', r.text)
    return [int(n, 16) << SHIFT for n in matches]


if __name__ == "__main__":
    print("Retrieving samples")
    # Prepare a list for every number
    highs_mat = [[] for _ in range(9)]

    # Try to use only the minimum number of samples
    for i in range(1, SAMPLES):
        highs_mat = [h + [n] for h, n in zip(highs_mat, get_numbers())]

        try:
            print("Trying to reconstruct states with {:02} samples".format(i), end=": ")
            # Reconstruct the original state for each LCG in the samples
            states = [
                int(
                    next(
                        reconstruct_lcg_state(
                            MODULUS, MULTIPLIER, INCREMENT, highs, SHIFT
                        )
                    )
                )
                for highs in highs_mat
            ]
            print("Success")
            break
        except Exception:
            time.sleep(0.5)
            print("Failed")

    # Step the LCGs to the next step, effectivly predicting the next value
    states = [
        int(list(lcg_step_state(MODULUS, MULTIPLIER, INCREMENT, state, i))[-1])
        for state in states
    ]

    print("Your next lottery numbers are:")
    for n in states:
        print("{:02X}".format(n >> SHIFT), end=" ")
    print()
    print()
