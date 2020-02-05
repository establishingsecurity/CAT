from cat.zkpake.offline_dictionary import OfflineDictionaryAttack
from cat.zkpake.zkpake_client import ZkPakeClient
from cat.zkpake.zkpake_server import ZkPakeServer

password = "test"
transcription = []

def __setup():
    client = ZkPakeClient(password)
    server = ZkPakeServer(password)
    message = server.send()
    __update_transcription(message, "server", "client")
    client.receive(message)
    message = client.send()
    __update_transcription(message, "client", "server")
    server.receive(message)

def __update_transcription(message, sender, receiver):
    msg = {"From": sender, "To": receiver}
    msg.update(message)
    transcription.append(msg)

def __getValue(transcription, value):
    for msg in transcription:
        if value in msg:
            return msg[value]


def test_offline_dictionary():
    __setup()
    N = __getValue(transcription, "N")
    p = __getValue(transcription, "p")
    g = __getValue(transcription, "g")
    u = __getValue(transcription, "u")
    hc = __getValue(transcription, "hc")

    offline_dictionary_attack = OfflineDictionaryAttack("dictionary.txt")
    pw = offline_dictionary_attack.crack_password(N, u, hc, p, g)
    assert(pw == password)
