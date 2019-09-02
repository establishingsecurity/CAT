from cat.speke.Ispeke import ISpeke
from cat.utils.ntheory import gen_safe_prime
from gmpy2 import powmod, mpz
from random import SystemRandom
import cat.speke.constants

class Speke(ISpeke):
    const = cat.speke.constants

# keep track (list of dict-participants attributes) of all participants -> can register via init and then set a password
# via get key
    users = []
    userInstances = []
    transcription = []
    g = 2;
    p = gen_safe_prime(128)
    q = gen_safe_prime(128)
    cryptogen = SystemRandom()

    def initialize(self, userNumber, id):
        user = {self.const.usernumber:userNumber, self.const.id:id}
        self.users.append(user)
        pass


    # user needs to have a password
    def setPassword(self, userNumber, id, password):
        for u in self.users:
            if u["id"] == id:
                user = {self.const.usernumber:userNumber, self.const.id:id, "password": password}
                u.update(user)
        pass

    def initializeUserInstance(self, userInstance, id, role, pid):
        userInstance.update({"status":"initialize", "role": role, "id": id, "pid": pid})
        self.userInstances.append(userInstance)
        pass

    def terminateUserInstance(self, userInstance):
        for uI in self.userInstances:
            if uI["i"] == userInstance["i"]:
                uI.update({"status":"terminate"})
        pass

    def getKey(self, userInstance):
        for uI in self.userInstances:
            if uI["i"] == userInstance["i"] and uI["j"] == userInstance["j"]:
                #correct userInstance found.
                #check if a userInstance is doing a "request" -> pid = id  and status connect
                for puI in self.userInstances:
                    if puI["pid"] == uI["id"] and puI["role"] == "connect" and uI["role"] == "open":
                        #determine private and public key for puid
                        print("i:" + str(uI["i"]) + " j:" + str(uI["j"]) + " role: " + uI["role"] + " getKey() ")

                        #find correct user
                        for u in self.users:
                            if u["id"] == puI["id"]:
                                x = self.cryptogen.randrange(self.p)
                                gx = powmod(self.g, x, self.p)
                                gx = powmod(self.f(u["password"],self.p, self.q), x, self.p)
                                update = {"public": gx, "private": x}
                        puI.update(update)
                        return gx
                    if puI["pid"] == uI["id"] and puI["role"] == "open" and uI["role"] == "connect":
                        print("i:" + str(uI["i"]) + " j:" + str(uI["j"]) + " role: " + uI["role"] + " getKey() ")
                        return puI["public"]
        pass

    def sendKey(self, userInstance, key):
        for uI in self.userInstances:
            if uI["i"] == userInstance["i"] and uI["j"] == userInstance["j"]:
                #correct userInstance found
                for puI in self.userInstances:
                    if puI["pid"] == uI["id"] and puI["role"] == "open" and uI["role"] == "connect":
                        print("i:" + str(uI["i"]) + " j:" + str(uI["j"]) + " role: " + uI["role"] + " sendKey() ")
                        for u in self.users:
                            if u["id"] == puI["id"]:
                                # send key and calc session key
                                x = self.cryptogen.randrange(self.p)
                                gx = powmod(self.g, x, self.p)

                                gx = powmod(self.f(u["password"], self.p, self.q), x, self.p)
                                sessionkey = powmod(key, x, self.p)

                                print("Sessionkey:" + str(sessionkey))
                                update = {"sessionkey": sessionkey, "private": x, "public": gx}
                                puI.update(update)
                    if puI["pid"] == uI["id"] and puI["role"] == "connect" and uI["role"] == "open":
                        print("i:" + str(uI["i"]) + " j:" + str(uI["j"]) + " role: " + uI["role"] + " sendKey() ")
                        sessionkey = powmod(key, puI["private"], self.p)
                        update = {"sessionkey": sessionkey}
                        print("Sessionkey:" + str(sessionkey))
                        puI.update(update)
        pass

    def getChallenge(self, userInstance):
        pass

    def sendChallenge(self, userInstance, challenge):
        pass

    def application(self):
        pass

    def f(self, S, p, q):
        return powmod(S, mpz((p-1)/q), p)