from cat.speke.ISpeke import ISpeke
from gmpy2 import powmod
from random import SystemRandom

import cat.speke.constants


class SpekeUKS():
    const = cat.speke.constants

    def uks(self, speke):
        if not isinstance(speke, ISpeke):
            print("wrong class type")
            return

        # Setup Mallory impersonating "Bob"
        speke.initialize_user(2, self.id)
        user_instance1 = {"i": 2, "j": 1}
        speke.initialize_user_instance(user_instance1, self.id, self.const.open, "A")
        user_instance2 = {"i": 2, "j": 2}
        speke.initialize_user_instance(user_instance2, self.id, self.const.connect, "A")


        cryptogen = SystemRandom()
        c = cryptogen.randrange(speke.p)

        # A wants to establish connection to B
        key = speke.get_key(user_instance1)

        # Establish new connection back to A
        key = powmod(key, c, speke.p)
        speke.send_key(user_instance2, key)
        key = speke.get_key(user_instance2)

        key = powmod(key, c, speke.p)
        speke.send_key(user_instance1, key)
        challenge = speke.get_challenge(user_instance1)

        speke.send_challenge(user_instance2, challenge)
        challenge = speke.get_challenge(user_instance2)

        speke.send_challenge(user_instance1, challenge)




    def __init__(self, id):
        self.id = id

