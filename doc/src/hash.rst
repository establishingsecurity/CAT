.. testsetup:: *
   from cat import *


:mod:`cat.hash` --- Hashing
===========================

Cryptographic hash functions reduce an arbitrary length input to a fixed length bit-string while adhering to three core properties.

.. math::

    H: \{0,1\}^* \to \{0,1\}^n

.. note::

    Properties of cryptographic hash functions:

    Collision resistance
        It's (computationally) infeasible to obtain two :math:`x` and :math:`x'`, such that :math:`H(x) = H(x')`.

    Second preimage resistance
        Given :math:`x \in \{0,1\}^*` its infeasible to obtain an :math:`x' \neq x`, such that :math:`H(x) = H(x')`.

    Preimage resistance (One-wayness)
        Given :math:`y = H(x)`, it's infeasible to find any :math:`x'`, such that :math:`H(x) = H(x')`.

Since it's hard to build and analyze a hash-function from the ground up, we build collision-resistant one-way compression functions instead:

.. math::

   h: \{0,1\}^m \to \{0,1\}^n


.. note::
    In general, collision resistance implies second preimage resistance.
    For hash functions collision resistance also implies one-wayness.

    .. For compression functions, one-wayness is only implied by collision resistance, when the compression function is sufficiently compressing (m = :math:`\omega(\log n)`).

Using the compression function we can apply a domain extension, like the Merkle-Damgård construction.

Given a fixed-length collision resistant compression function :math:`h: \{0,1\}^{2n} \to \{0,1\}^n`, the Merkle-Damgård constructs a collision resistant hash function :math:`H`:

#. Append a 1 bit at the end of the message
#. Pad the input with zeros to a multiple of :math:`n`.
#. Append a block containing the :math:`n` bit representation of the message length (or add it in the padding block, if there are at least :math:`n` padding bits)
#. Set :math:`z = \IV = 0^n` (the :term:`IV` may be arbitrary)
#. For each block :math:`i` set :math:`z = h(z_{i-1}\|x_i)`
#. Output :math:`z`

.. image:: ../figures/merkle_damgard.*
   :width: 100 %

Unfortunately, or luckily for us, hash functions were incorrectly used to construct :term:`MACs<MAC>`.
Reviewing the properties of cryptographic hash functions, they don't ensure that given :math:`H_{\IV}(m)` its infeasible to find :math:`H_{\IV}(\pad(m) \| m')`.
This is a property implied by the core security definition of :term:`MACs<MAC>`.
You may already see how, given :math:`H_{\IV}(m)` and the length of :math:`m`, it's possible to append another block at the end of the depicted chain and compute :math:`H_{\IV}(\pad(m) \| m')`.


.. toctree::
   :glob:

   hash/*

