from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from hypothesis import given
from hypothesis.strategies import binary

from cat.symmetric.util import *


@given(binary(min_size=16, max_size=16), binary(min_size=16, max_size=16))
def test_edit_cbc_block(key, iv):
    plaintext = pad(b"de11beef" + b"deadbeef" * 3, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    ciphertext = cipher.encrypt(plaintext)

    edited = edit_cbc_block(iv, 2, b"11", b"ad")
    cipher = AES.new(key, AES.MODE_CBC, iv=edited)
    decrypted = cipher.decrypt(ciphertext)
    assert len(decrypted) == len(plaintext)
    assert decrypted == pad(b"deadbeef" * 4, AES.block_size)

    edited = edit_cbc_block(edited, 2, b"ad", b"11")
    cipher = AES.new(key, AES.MODE_CBC, iv=edited)
    decrypted = cipher.decrypt(ciphertext)
    assert len(decrypted) == len(plaintext)
    assert edited == iv
    assert decrypted == plaintext
