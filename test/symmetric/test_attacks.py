from hypothesis import given
from hypothesis.strategies import binary

from binascii import unhexlify
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

from cat.symmetric.attacks import cbc_padding_oracle, cbc_padding_oracle_length
from cat.symmetric.util import block_chunks


def test_cbc_padding_oracle_single():
    plaintext = b"\x01" * 31
    key = unhexlify("deadbeef" * 4)
    base_iv = unhexlify("beefdead" * 4)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(
        block_chunks(cipher.encrypt(pad(plaintext, AES.block_size)), AES.block_size)
    )

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except:
            return False

    recovered = b"".join(list(cbc_padding_oracle(base_iv, ciphertext, oracle)))
    assert plaintext == recovered

@given(binary(min_size=16, max_size=16), binary(min_size=16, max_size=16), binary(min_size=16, max_size=16))
def test_cbc_padding_oracle_full_block(key, base_iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(
        block_chunks(cipher.encrypt(pad(plaintext, AES.block_size)), AES.block_size)
    )

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except:
            return False

    recovered = b"".join(list(cbc_padding_oracle(base_iv, ciphertext, oracle)))
    assert plaintext == recovered

@given(binary(min_size=16, max_size=16), binary(min_size=16, max_size=16), binary(min_size=0, max_size=32))
def test_cbc_padding_oracle_arbitrary(key, base_iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(
        block_chunks(cipher.encrypt(pad(plaintext, AES.block_size)), AES.block_size)
    )

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except:
            return False

    recovered = b"".join(list(cbc_padding_oracle(base_iv, ciphertext, oracle)))
    assert plaintext == recovered

def test_cbc_padding_oracle_length():
    plaintext = b"deadbeef" * 7
    key = unhexlify("deadbeef" * 4)
    base_iv = unhexlify("beefdead" * 4)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(
        block_chunks(cipher.encrypt(pad(plaintext, AES.block_size)), AES.block_size)
    )

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except ValueError:
            return False

    assert len(plaintext) == cbc_padding_oracle_length(base_iv, ciphertext, oracle)


def test_cbc_padding_oracle_length_full():
    plaintext = b"deadbeef" * 8
    key = unhexlify("deadbeef" * 4)
    base_iv = unhexlify("beefdead" * 4)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(
        block_chunks(cipher.encrypt(pad(plaintext, AES.block_size)), AES.block_size)
    )

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except ValueError:
            return False

    assert len(plaintext) == cbc_padding_oracle_length(base_iv, ciphertext, oracle)
