from binascii import unhexlify
from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from cat.symmetric.attacks import cbc_padding_oracle


def test_cbc_padding_oracle_single():
    plaintext = b"deadbeef"*4
    key = unhexlify("deadbeef"*4)
    base_iv = unhexlify("beefdead"*4)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    def oracle(iv, ciphertext):
        cipher = AES.new(base_key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(plaintext, AES.block_size)
        try:
            unpad(plaintext)
            return True
        except:
            return False

    assert plain == cbc_padding_oracle(iv, ciphertext, oracle)

