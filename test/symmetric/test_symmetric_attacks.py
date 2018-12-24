from binascii import unhexlify

import pytest
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from hypothesis import assume, example, given, settings
from hypothesis.strategies import binary, integers

from cat.symmetric.attacks import *
from cat.symmetric.util import block_chunks


def test_cbc_padding_oracle_single():
    plaintext = pad(b"A" * 30, AES.block_size)
    key = unhexlify("deadbeef" * 4)
    base_iv = unhexlify("beefdead" * 4)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(block_chunks(cipher.encrypt(plaintext), AES.block_size))

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except:
            return False

    recovered = b"".join(list(cbc_padding_oracle(base_iv, ciphertext, oracle)))
    assert len(plaintext) == len(recovered)
    assert plaintext == recovered


@example(
    # Changing byte_15 to 0x02 here is a valid padding which might break things
    key=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    base_iv=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    plaintext=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01",
)
@given(
    binary(min_size=16, max_size=16),
    binary(min_size=16, max_size=16),
    binary(min_size=16, max_size=16),
)
@settings(deadline=None)
@pytest.mark.slow
def test_guess_cbc_byte(key, base_iv, plaintext):
    plaintext = pad(plaintext, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(block_chunks(cipher.encrypt(plaintext), AES.block_size))

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except:
            return False

    for byte_pos in range(len(base_iv)):
        recovered = guess_cbc_byte(
            base_iv, ciphertext[0], oracle, byte_pos, plaintext[byte_pos + 1 : 16]
        )
        assert recovered == plaintext[byte_pos].to_bytes(1, byteorder="big")


@example(
    key=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    base_iv=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    plaintext=b"\x00",
)
@given(
    binary(min_size=16, max_size=16),
    binary(min_size=16, max_size=16),
    binary(min_size=1, max_size=32),
)
@settings(deadline=None)
@pytest.mark.slow
def test_cbc_padding_oracle_arbitrary(key, base_iv, plaintext):
    plaintext = pad(plaintext, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(block_chunks(cipher.encrypt(plaintext), AES.block_size))

    def oracle(iv, ciphertext):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        try:
            unpad(plaintext, AES.block_size)
            return True
        except:
            return False

    recovered = b"".join(list(cbc_padding_oracle(base_iv, ciphertext, oracle)))
    assert len(plaintext) == len(recovered)
    assert plaintext == recovered


@example(
    key=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    base_iv=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    plaintext=b"\x00",
)
@given(
    binary(min_size=32, max_size=32),
    binary(min_size=16, max_size=16),
    binary(min_size=1, max_size=32),
)
@settings(deadline=None)
@pytest.mark.slow
def test_cbc_padding_oracle_arbitrary_256(key, base_iv, plaintext):
    plaintext = pad(plaintext, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv=base_iv)

    ciphertext = list(block_chunks(cipher.encrypt(plaintext), AES.block_size))

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


@given(
    binary(min_size=16, max_size=16),
    binary(min_size=16, max_size=16),
    binary(min_size=1, max_size=32),
)
def test_cbc_padding_oracle_length(key, base_iv, plaintext):
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


@given(
    binary(min_size=32, max_size=32),
    binary(min_size=16, max_size=16),
    binary(min_size=1, max_size=32),
)
def test_cbc_padding_oracle_length_256(key, base_iv, plaintext):
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
