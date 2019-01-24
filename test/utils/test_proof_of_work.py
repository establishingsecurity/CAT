"""Tests for the proof-of-work module"""
import hashlib
import sys

import pytest
from Cryptodome.Hash import (
    MD2,
    MD5,
    RIPEMD160,
    SHA1,
    SHA3_224,
    SHA3_256,
    SHA3_384,
    SHA3_512,
    SHA224,
    SHA256,
    SHA384,
    SHA512,
    BLAKE2b,
    BLAKE2s,
    keccak,
)
from hypothesis import given
from hypothesis.strategies import binary, sampled_from

from cat.utils import proof_of_work
from cat.utils.proof_of_work import wrap_cryptodome, wrap_hashlib
from cat.utils.utils import generate_brute_force


def input_source(start):
    for bf in generate_brute_force(start):
        yield bytes(bf)


def hashes_test(
    hashes,
    wrapper,
    test_unwrapped=True,
    prefix=b"challenge",
    suffix=b"suffix",
    **kwargs
):
    for hash_function in hashes:
        condition = lambda d: d.startswith("0")
        wrapped = wrapper(hash_function, **kwargs)
        if test_unwrapped:
            guess = proof_of_work.hash_pow(
                "alphabet", hash_function, prefix, suffix, condition=condition
            )
            digest = wrapped(prefix + guess + suffix)
            assert condition(digest)
        guess = proof_of_work.hash_pow(
            "alphabet", wrapped, prefix, suffix, condition=condition
        )
        digest = wrapped(prefix + guess + suffix)
        assert condition(digest)


def test_sha2_hash_functions():
    """Test SHA-2 family"""
    hashes_test([SHA224, SHA256, SHA384, SHA512], wrap_cryptodome)


def test_sha3_hash_functions():
    """Test SHA-3 family"""
    hashes_test([SHA3_224, SHA3_256, SHA3_384, SHA3_512], wrap_cryptodome)


def test_blake2_hash_functions():
    if sys.version_info[0] >= 3:
        hashes_test(
            [BLAKE2s, BLAKE2b], wrap_cryptodome, digest_bytes=32, test_unwrapped=False
        )
    else:
        assert True


def test_legacy_hash_functions():
    hashes_test([SHA1, MD2, MD5, RIPEMD160], wrap_cryptodome)


def test_keccak():
    hashes_test([keccak], wrap_cryptodome, digest_bytes=32, test_unwrapped=False)


def test_sha2_hashlib_functions():
    """Test SHA-2 family"""
    hashes_test(
        [hashlib.sha224, hashlib.sha256, hashlib.sha384, hashlib.sha512], wrap_hashlib
    )


def test_sha3_hashlib_functions():
    """Test SHA-3 family"""
    if sys.version_info[0] >= 3:
        hashes_test(
            [hashlib.sha3_224, hashlib.sha3_256, hashlib.sha3_384, hashlib.sha3_512],
            wrap_hashlib,
        )
    else:
        assert True


def test_blake2_hashlib_functions():
    if sys.version_info[0] >= 3:
        hashes_test([hashlib.blake2s, hashlib.blake2b], wrap_hashlib)
    else:
        assert True


def test_legacy_hashlib_functions():
    hashes_test([hashlib.sha1, hashlib.md5], wrap_hashlib)


def test_shake():
    if sys.version_info[0] >= 3:
        hashes_test(
            [hashlib.shake_128, hashlib.shake_256],
            wrap_hashlib,
            length=32,
            test_unwrapped=False,
        )
    else:
        assert True


@pytest.mark.slow
@given(binary(), binary(), sampled_from([SHA1, SHA512, SHA3_224, MD5]))
def test_hypothesis(prefix, suffix, hash_fn):
    hashes_test([hash_fn], wrap_cryptodome, True, prefix, suffix)


@pytest.mark.slow
@given(
    binary(),
    binary(),
    sampled_from([hashlib.sha1, hashlib.sha384, hashlib.sha512, hashlib.md5]),
)
def test_hypothesis(prefix, suffix, hash_fn):
    hashes_test([hash_fn], wrap_hashlib, True, prefix, suffix)


def test_is_hashlib():
    pass
