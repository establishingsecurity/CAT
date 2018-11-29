"""Tests for the proof-of-work module"""

import re
import pytest

from Cryptodome.Hash import (
    SHA224, SHA256, SHA384, SHA512,
    SHA3_224, SHA3_256, SHA3_384, SHA3_512,
    BLAKE2s, BLAKE2b,
    SHA1, MD2, MD5, RIPEMD160, keccak
)
from unittest.mock import patch


from cat.utils import proof_of_work
from cat.utils.utils import generate_brute_force


def input_source(start):
    for bf in generate_brute_force(start):
        yield bytes(bf)


def test_sha2_hash_functions():
    hashes = [SHA224, SHA256, SHA384, SHA512]

    for hash_function in hashes:
        condition = lambda d: d.hex().startswith('0')

        generator = input_source([0])
        pow_ = proof_of_work.compute_prefix(hash_function, b'', condition, generator)
        pow_ = hash_function.new(data=pow_).digest()
        assert condition(pow_)


def test_sha3_hash_functions():
    """Test SHA-3 family"""
    hashes = [SHA3_224, SHA3_256, SHA3_384, SHA3_512]

    for hash_function in hashes:
        condition = lambda d: d.hex().startswith('0')

        generator = input_source([0])
        pow_ = proof_of_work.compute_prefix(hash_function, b'', condition, generator)
        pow_ = hash_function.new(data=pow_).digest()
        assert condition(pow_)


def test_blake2_hash_functions():
    hashes = [BLAKE2s, BLAKE2b]
    for hash_function in hashes:
        condition = lambda d: d.hex().startswith('0')

        generator = input_source([0])
        pow_ = proof_of_work.compute_prefix(hash_function, b'', condition, generator)
        pow_ = hash_function.new(data=pow_).digest()
        assert condition(pow_)


def test_legacy_hash_functions():
    hashes = [SHA1, MD2, MD5, RIPEMD160]

    for hash_function in hashes:
        condition = lambda d: d.hex().startswith('0')

        generator = input_source([0])
        pow_ = proof_of_work.compute_prefix(hash_function, b'', condition, generator)
        pow_ = hash_function.new(data=pow_).digest()
        assert condition(pow_)

    generator = input_source([0])
    pow_ = proof_of_work.compute_prefix(keccak, b'', condition, generator, digest_bytes=32)
    pow_ = keccak.new(data=pow_, digest_bytes=32).digest()
    assert condition(pow_)
