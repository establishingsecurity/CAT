Length Extension Attacks
========================

.. math::

   \DeclareMathOperator{\Gen}{Gen}
   \DeclareMathOperator{\Mac}{Mac}
   \DeclareMathOperator{\Vrfy}{Vrfy}
   \DeclareMathOperator{\IV}{IV}
   \DeclareMathOperator{\pad}{pad}

The length extension attack terms a class of attacks arising from invalid use of hash functions as message authentication codes, enabling us to forge a valid tags for known but previously unauthenticated messages.

If you already know about hash functions and :term:`MACs<MAC>`, you may skip to the `length extension`_ section.

Cryptographic Hash Functions
----------------------------

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

:term:`MACs<MAC>` (Message Authentication Codes)
------------------------------------------------

A :term:`MAC` consists of three algorithms:

:math:`\Gen(1^n)`
   A key generation algorithm, given an input in the length of the security parameter :math:`n`.
:math:`\Mac_k(m)`
   A tag generation algorithm, which given a message :math:`m \in \{0,1\}^*` outputs a tag :math:`t \in \{0,1\}^n`.
:math:`\Vrfy_k(m, t)`
   A verification algorithm, which given a key :math:`k`, a message :math:`m` and a tag :math:`t` outputs whether the tag is a valid for the given message under the key :math:`k`.
   If the Mac is deterministic, then by canonical verification we can simply recompute the tag for the given message and key and check whether it's the tag :math:`t`.

A :term:`MAC` is considered secure if its infeasible to determine the tag of a (previously unauthenticated) message, when we are given access to a MAC oracle, which yields the tags of any requested message.

Length Extension
----------------

Let's try to construct a MAC using a Merkle-Damgård hash function :math:`H_{\IV}(\cdot)`.

.. math::

   \begin{align*}
      \Mac_k(m) &= H_{0^n}(k\|m)\\
      \Vrfy_k(m, t) &= H_{0^n}(k\|m) \stackrel{?}{=} t
   \end{align*}

This theoretical gap translates to a practical attack on the constructed insecure MAC.
In fact for Merkle-Damgård constructions, when we know :math:`m` and the length of :math:`k`, we may append another block and compute :math:`\Mac_k(\pad(m) \| m') = H_{0^n}(\pad(m)\|m') = H_{\pad(m)}(m')`.
We need to know the length of :math:`k` to pad the message correctly during hashing.

.. glossary::

   MAC

      Message Authentication Code. Enables symmetric authentication and verification of messages. In contrast to cryptographic hash functions, MACs are keyed, and provide entirely different properties.

   IV

      `Initialization Vector`_

      .. _`Initialization Vector`: https://en.wikipedia.org/wiki/Initialization_vector
