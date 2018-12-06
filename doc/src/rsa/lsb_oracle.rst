**************
RSA LSB Attack
**************

The Least Significant Bit Oracle attack is a simpler variation of
Bleichenbacher.

It assumes a decryption oracle :math:`LSB(\cdot)` that accepts ciphertexts and returns the
least significant or parity bit of the decrypted plaintext.

This oracle leaks at least one bit of the plaintext, but can be used to reveal the whole plaintext using the multiplicative homomorphic property of RSA.

=========
Intuition
=========

.. note::
    RSA is multiplicative homomorphic, i.e :math:`a^e b^e \equiv (a b)^e \mod N`

We use the homomorphic property, i.e :math:`2^e m^e \equiv (2 m)^e \mod N`, and the fact that we can construct :math:`2^e \mod N` because we assume we have the public key :math:`(e, N)`.

Multiplying this value to our target ciphertext yields :math:`c_2 = (2 m)^e \mod N`, which we can query the LSB oracle with.

The value :math:`2 m` is an even, if the answer to our query is :math:`1`, we conclude that :math:`(2 m) \ge N`.
If it reveals 0, then :math:`2 m \leq N` must hold.
The resulting inequality reveals a bound on the plaintext.

We can iterate the attack with :math:`c_4 = (4 m)^e \mod N`.
Depending on the two bits revealed so far we get:

================    ================    ==============================
:math:`LSB(c_2)`    :math:`LSB(c_4)`    Bound
================    ================    ==============================
0                   0                   :math:`4 m \leq N`
0                   1                   :math:`4 m > N`
1                   0                   :math:`2 (2 m - N) \leq 2 N`
1                   1                   :math:`2 (2 m - N) > 2 N`
================    ================    ==============================

We can reformulate this as a tree:

.. image:: ../figures/lsb_tree.*
   :width: 100 %

The attack works by binary searching this tree and getting stricter bounds on
the plaintext in every step.

=======
Example
=======

The following example uses the cat library to exploit a LSB Oracle over TCP.

.. literalinclude:: examples/lsb_client.py
   :language: python
   :emphasize-lines: 30-38
   :linenos:
