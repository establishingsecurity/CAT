import cat.speke.constants
from cat.speke.SpekeImpl import Speke
from cat.speke.unknownKeyShare import SpekeUKS


def __setup_alice(speke):
    const = cat.speke.constants
    # usernumber, id
    speke.initialize_user(1, "A")
    speke.set_password(1, "A", 1234)
    user_instance1 = {"i": 1, "j": 1}
    speke.initialize_user_instance(user_instance1, "A", const.open, "B")
    user_instance2 = {"i": 1, "j": 2}
    speke.initialize_user_instance(user_instance2, "A", const.connect, "B")
    return user_instance1


def test_unknown_key_share():
    speke = Speke()
    user_instance = __setup_alice(speke)
    uks = SpekeUKS("B")
    uks.uks(speke)

    for trans in speke.transcription:
        print(trans)

    assert user_instance["status"] == "connected"