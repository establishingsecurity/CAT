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
In fact for Merkle-Damgård constructions, when we know the length of :math:`m\|k`, we may append a message :math:`m'` and compute :math:`\Mac_k(\pad(m) \| m') = H_{0^n}(pad(k\|m)\|m') = H_{\pad(k\|m)}(m')`.
We need to know the length of :math:`k` to pad the message correctly during hashing.

Example
-------

We expose the excellent hashpumpy_ library:

.. _hashpumpy: https://github.com/bwall/HashPump/

.. testcode ::

   from cat.hash import hashpump
   from hashlib import sha1
   key = b'secret'
   message = b'message'
   digest = sha1(key + message).hexdigest()
   to_add = b'hello world'

   new_digest, new_message = hashpump(digest, message, to_add, len(key))

   assert sha1(key + new_message).hexdigest() == new_digest
   assert new_message.endswith(to_add)
   assert new_message.startswith(message)

.. glossary::

   MAC

      Message Authentication Code. Enables symmetric authentication and verification of messages. In contrast to cryptographic hash functions, MACs are keyed, and provide entirely different properties.

   IV

      `Initialization Vector`_

      .. _`Initialization Vector`: https://en.wikipedia.org/wiki/Initialization_vector
