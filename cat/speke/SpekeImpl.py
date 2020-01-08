from abc import ABC

from cat.speke.ISpeke import ISpeke
from cat.utils.ntheory import gen_safe_prime
from gmpy2 import powmod, mpz, gmpy2
from random import SystemRandom
import cat.speke.constants
from Cryptodome.Hash import SHA256


def f(s, p, q):
    return powmod(s, mpz((p - 1) / q), p)


class Speke(ISpeke, ABC):
    const = cat.speke.constants

    # via get key
    users = []
    userInstances = []
    transcription = []
    g = 2;
    p = gen_safe_prime(128)
    q = gen_safe_prime(128)
    cryptogen = SystemRandom()

    def initialize(self, user_number, m_id):
        user = {self.const.usernumber: user_number, self.const.id: m_id}
        self.users.append(user)
        pass

    # user needs to have a password
    def set_password(self, user_number, m_id, password):
        for u in self.users:
            if u["id"] == m_id:
                user = {self.const.usernumber: user_number, self.const.id: m_id, "password": password}
                u.update(user)
        pass

    def initialize_user_instance(self, user_instance, m_id, role, pid):
        user_instance.update({"status": "initialize", "role": role, "id": m_id, "pid": pid})
        self.userInstances.append(user_instance)
        self.transcription.append("[initialize    ]" +
                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                  " id:" + user_instance["id"] +
                                  " pid:" + user_instance["pid"] +
                                  " role:" + user_instance["role"])
        pass

    def update_status(self, user_instance, status):
        for uI in self.userInstances:
            if uI["i"] == user_instance["i"] and uI["j"] == user_instance["j"]:
                uI.update({"status": status})
                self.transcription.append("[" + status + "     ]" +
                                          " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                          " id:" + user_instance["id"] +
                                          " pid:" + user_instance["pid"] +
                                          " role:" + user_instance["role"])
        pass

    def terminate_user_instance(self, user_instance):
        self.update_status(user_instance, "terminate")
        pass

    def connection_established(self, user_instance):
        self.update_status(user_instance, "connected")
        pass

    def get_key(self, user_instance):
        for uI in self.userInstances:
            if uI["i"] == user_instance["i"] and uI["j"] == user_instance["j"]:
                # correct userInstance found.
                # check if a userInstance is doing a "request" -> pid = id  and status connect
                for puI in self.userInstances:
                    if puI["pid"] == uI["id"] and puI["role"] == "connect" and uI["role"] == "open":
                        # determine private and public key for puid

                        # find correct user
                        for u in self.users:
                            if u["id"] == puI["id"]:
                                x = self.cryptogen.randrange(self.p)
                                gx = powmod(f(u["password"], self.p, self.q), x, self.p)
                                update = {"public": gx, "private": x}
                        puI.update(update)
                        self.transcription.append("[get_key       ]" +
                                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                                  " id:" + user_instance["id"] +
                                                  " pid:" + user_instance["pid"] +
                                                  " role:" + user_instance["role"] +
                                                  " pubKey:" + str(puI["public"]))
                        return gx
                    if puI["pid"] == uI["id"] and puI["role"] == "open" and uI["role"] == "connect":
                        self.transcription.append("[get_key       ]" +
                                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                                  " id:" + user_instance["id"] +
                                                  " pid:" + user_instance["pid"] +
                                                  " role:" + user_instance["role"] +
                                                  " pubKey:" + str(puI["public"]))
                        return puI["public"]
        pass

    def send_key(self, user_instance, key):
        self.transcription.append("[send_key      ]" +
                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                  " id:" + user_instance["id"] +
                                  " pid:" + user_instance["pid"] +
                                  " role:" + user_instance["role"] +
                                  " pubKey:" + str(key))
        for uI in self.userInstances:
            if uI["i"] == user_instance["i"] and uI["j"] == user_instance["j"]:
                # correct userInstance found
                for puI in self.userInstances:
                    if puI["pid"] == uI["id"] and puI["role"] == "open" and uI["role"] == "connect":
                        for u in self.users:
                            if u["id"] == puI["id"]:
                                # send key and calc session key
                                x = self.cryptogen.randrange(self.p)
                                gx = powmod(f(u["password"], self.p, self.q), x, self.p)
                                sessionkey = powmod(key, x, self.p)

                                update = {"sessionkey": sessionkey, "private": x, "public": gx}
                                puI.update(update)
                    if puI["pid"] == uI["id"] and puI["role"] == "connect" and uI["role"] == "open":
                        sessionkey = powmod(key, puI["private"], self.p)
                        update = {"sessionkey": sessionkey}
                        puI.update(update)
        pass

    def get_challenge(self, user_instance):
        for uI in self.userInstances:
            if uI["i"] == user_instance["i"] and uI["j"] == user_instance["j"]:
                # correct user userinstance found
                for puI in self.userInstances:
                    if puI["pid"] == uI["id"] and puI["role"] == "connect" and uI["role"] == "open":
                        # get hash of hash of session key
                        mhash = SHA256.new(SHA256.new(gmpy2.to_binary(puI["sessionkey"])).digest()).hexdigest()
                        self.transcription.append("[get_challenge ]" +
                                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                                  " id:" + user_instance["id"] +
                                                  " pid:" + user_instance["pid"] +
                                                  " role:" + user_instance["role"] +
                                                  " challenge:" + mhash)
                        return mhash
                    if puI["pid"] == uI["id"] and puI["role"] == "open" and uI["role"] == "connect":
                        mhash = SHA256.new(gmpy2.to_binary(puI["sessionkey"])).hexdigest()
                        self.transcription.append("[get_challenge ]" +
                                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                                  " id:" + user_instance["id"] +
                                                  " pid:" + user_instance["pid"] +
                                                  " role:" + user_instance["role"] +
                                                  " challenge:" + mhash)
                        return mhash

        pass

    def send_challenge(self, user_instance, challenge):
        self.transcription.append("[send_challenge]" +
                                  " i/j:" + str(user_instance["i"]) + "/" + str(user_instance["j"]) +
                                  " id:" + user_instance["id"] +
                                  " pid:" + user_instance["pid"] +
                                  " role:" + user_instance["role"] +
                                  " challenge:" + challenge)
        for uI in self.userInstances:
            if uI["i"] == user_instance["i"] and uI["j"] == user_instance["j"]:
                # correct userInstance found
                for puI in self.userInstances:
                    if puI["pid"] == uI["id"] and puI["role"] == "open" and uI["role"] == "connect":
                        mhash = SHA256.new(SHA256.new(gmpy2.to_binary(puI["sessionkey"])).digest()).hexdigest()
                        if mhash == challenge:
                            self.connection_established(uI)
                            self.connection_established(puI)
                        else:
                            self.terminate_user_instance(uI)
                            self.terminate_user_instance(puI)
                    if puI["pid"] == uI["id"] and puI["role"] == "connect" and uI["role"] == "open":
                        mhash = SHA256.new(gmpy2.to_binary(puI["sessionkey"])).hexdigest()
                        if mhash == challenge:
                            self.connection_established(uI)
                            self.connection_established(puI)
                        else:
                            self.terminate_user_instance(uI)
                            self.terminate_user_instance(puI)

        pass

    def application(self):
        pass
