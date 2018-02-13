from Cryptodome.Hash import SHA256
from Cryptodome.Util.number import bytes_to_long
from ctypes import c_ulonglong
from binascii import hexlify
import struct

from .extendable import *

import pytest

def test_load_stateorder():
    # Prepare test state for load input
    data = [b'ABCD', b'EFGH', b'IJKL', b'MNOP', b'QRST', b'UVWX', b'YZ12', b'3456']
    load_state = [i for s in data for i in s]
    
    # Load state into hash object
    hash_object = load(load_state, 32)

    # Retrieve internal state
    state_pointer = hash_object._state.get()
    state_type = c_ulonglong * 8
    state = state_type.from_buffer(state_type.from_address(state_pointer.value))

    # State must match test state with groups of 4 bytes switched
    assert struct.pack('!Q',state[0]) == data[1] + data[0]
    assert struct.pack('!Q',state[1]) == data[3] + data[2]
    assert struct.pack('!Q',state[2]) == data[5] + data[4]
    assert struct.pack('!Q',state[3]) == data[7] + data[6]
