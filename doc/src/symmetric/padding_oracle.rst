*************************
CBC Padding Oracle Attack
*************************

The CBC Padding Oracle attack can be used to decrypt a target ciphertext by
using an oracle that returns whether the padding of the plaintext is valid or
not.

It assumes a decryption oracle :math:`PADDING(\cdot)` that accepts ciphertexts
and returns whether the padding of the decrypted plaintext is valid.

CBC Decryption works like depicted in the diagram

.. image:: ../figures/cbc_decryption.*
   :width: 100 %

The first step of the attack is to determine the least significant byte of the
plaintext. This is done by using the ciphertext block :math:`c_{n-1}` immediatly preceeding the
target ciphertext block :math:`c_{n}`.
The block :math:`c_{n-1}` is xored into :math:`i_{n}` to get the plaintext.
If we don't care about :math:`p_{n-1}` we can change :math:`c_{n-1}` to any
value and change the bytes that are xored into :math:`i+{n}` with it.
With this attack primitive, we can take a guess :math:`g` of the byte at the last position of
:math:`p_{n}` and change the last byte of :math:`c_{n-1}` to :math:`g \oplus 0x01 \oplus c_{n-1, m}`.

If our guess was correct, we expect a correct padding with high probability.

We now know the last byte and can change it to any arbitrary value.
Guessing the second to last byte of a plaintext block works by setting the last
byte to :math:`0x02` and the second to last byte of the preceeding ciphertext block to :math:`g \oplus 0x02 \oplus c_{n-1, m-1}`.
