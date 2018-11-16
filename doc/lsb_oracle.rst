**************
RSA LSB Attack
**************

The Least Significant Bit Oracle attack is a simpler variation of
Bleichenbacher.

It assumes a decryption oracle :math:`LSB(\cdot)` that accepts ciphertexts and returns the
least significant or parity bit of the decrypted plaintext.

This oracle leaks at least one bit of the plaintext, but can be used to reveal the whole plaintext using the multplicative homomorphic property of RSA.

=========
Intuition
=========

.. note::
    RSA is multiplicative homomorphic, i.e :math:`a^e * b^e \equiv (a * b)^e \mod N`

We use the homomorphic property, i.e :math:`2^e * m^e \equiv (2 * m)^e \mod N`, and the fact that we can construct :math:`2^e \mod N` because we assume we have the public key :math:`(e, N)`.

Multiplying this value to our target ciphertext yields :math:`(2 * m)^e \mod N`, which we can query the LSB oracle with.

The value :math:`(2 * m)` is an even, if the answer to our query is :math:`1`, we conclude that :math:`(2 * m) \ge N`.
If it reveals 0, then :math:`2^c m \leq N` must hold.
The resulting inequality reveals a bound on the plaintext.


..
    1. Set the current ciphertext as the target ciphertext
    2. Set the counter :math:`c` to :math:`0`
    3. Query for the LSB of the current ciphertext. \
    4. Set the current ciphertext to :math:`c \dot 2^e \mod N`.
    5. Increase the counter.
    6. Repeat until you narrowed the searchspace of the plaintext enough.
