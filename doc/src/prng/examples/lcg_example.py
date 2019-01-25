import re

import requests
from cat.prng.lcg import reconstruct_lcg_state, lcg_step_state

from lottery import STATE_SIZE, MODULUS, MULTIPLIER, INCREMENT, SHIFT

SAMPLES = 10

PORT = 8080


def get_number():
    r = requests.get("http://localhost:{}".format(PORT))
    m = re.search(r"(?<=<body>)\w+", r.text)
    return int(m.group(0)) << SHIFT


if __name__ == "__main__":
    highs = [get_number() for _ in range(SAMPLES)]
    state = int(next((reconstruct_lcg_state(MODULUS, MULTIPLIER, INCREMENT, highs, SHIFT))))
    print("Original state:\n{}".format(state))
    states = [int(x) for x in lcg_step_state(MODULUS, MULTIPLIER, INCREMENT, state, SAMPLES+5)]
    print("Your next lottery numbers are:")
    for l in map(lambda x: x >> SHIFT, states[SAMPLES-1:]):
        print("\t", l)

