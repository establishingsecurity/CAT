from cat.speke.Ispeke import ISpeke
from gmpy2 import powmod
from random import SystemRandom

import cat.speke.constants


class SpekeUKS():

    const = cat.speke.constants


    def uks(self, speke):
        if not issubclass(speke.__class__, ISpeke):
            print("wrong class type")
            return

        self.speke = speke
        self.setupAlice(speke)

        speke.initialize(2, self.id)
        userInstance1 = {"i": 2, "j": 1}
        speke.initializeUserInstance(userInstance1, self.id, "open", "A")
        userInstance2 = {"i": 2, "j": 2}
        speke.initializeUserInstance(userInstance2, self.id, "connect", "A")


        cryptogen = SystemRandom()
        c = cryptogen.randrange(speke.p)

        key = speke.getKey(userInstance1)
        key = powmod(key, c, speke.p)
        speke.sendKey(userInstance2, key)

        key = speke.getKey(userInstance2)
        key = powmod(key, c, speke.p)
        speke.sendKey(userInstance1, key)

    def setupAlice(self, speke):
        speke.initialize(1, "A")
        speke.setPassword(1, "A", 1234)
        userInstance = {"i": 1, "j": 1}
        speke.initializeUserInstance(userInstance, "A", "open", "B")

        userInstance = {"i": 1, "j": 2}
        speke.initializeUserInstance(userInstance, "A", "connect", "B")

    def __init__(self, id):
        self.id = id

