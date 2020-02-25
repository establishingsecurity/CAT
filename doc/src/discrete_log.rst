.. testsetup:: *
   from cat import *


:mod:`cat.discrete_log` --- Analyses for ElGamal/Diffie-Hellman-Merkle key exchange
===================================================================================

.. epigraph::

    Diffie–Hellman key exchange (DH) is a method of securely exchanging cryptographic keys over a public channel and was one of the first public-key protocols as originally conceptualized by Ralph Merkle and named after Whitfield Diffie and Martin Hellman.

    -- `Wikipedia on DH`_.

    [T]he ElGamal encryption system is an asymmetric key encryption algorithm for public-key cryptography which is based on the Diffie–Hellman key exchange.

    -- `Wikipedia on ElGamal`_.

.. _`Wikipedia on DH`: https://en.wikipedia.org/wiki/Diffie–Hellman_key_exchange
.. _`Wikipedia on ElGamal`: https://en.wikipedia.org/wiki/ElGamal_encryption


DH key exchange is a method that allows two parties to exchange a secret key securely via an *authenticated*, but insecure channel.
ElGamal then adapts the approach taken by DH key exchange to construct an encryption scheme for public-key encryption.
Both the security of DH key exchange and of ElGamal encryption is based on the **discrete logarithm problem**, which states that given a group :math:`\mathcal{G}` of order :math:`q`, a generator for that group :math:`g` and a group element :math:`h` it is hard for a polynomial-time adversary to compute :math:`x` such that :math:`h = g^x`.
If this is the case, then it is said that the discrete logarithm problem is hard relative to :math:`\mathcal{G}`.

.. note::
    If computing :math:`x` such that :math:`h=g^x` for uniform :math:`h \in \mathcal{G}` is hard in polynomial time, the discrete logarithm problem is hard relative to :math:`\mathcal{G}`.

As you can see, the hardness of computing discrete logarithms is not an absolute assumption, but *always with regards to a specific group* :math:`\mathcal{G}`.
This means that depending on the defining parameters of a group, computing discrete logarithms could be very easy:

.. note::
    Let us a define a multiplicative group :math:`\mathcal{G'}` with a modulus of :math:`4`. The group's elements are :math:`\{1,3\}`, with :math:`3` being the generator of the group.
    
    If given a group element :math:`h` sampled uniformly at random from :math:`\mathcal{G'}`, computing :math:`x` takes one operation since :math:`3^1 = 3 \pmod{4}` and :math:`3^2 = 9 = 1 \pmod{4}`.

    .. code-block:: python

        return 1 if h == 3 else 2

Choosing the wrong parameters for the group used by either DH or ElGamal can therefore have disastrous results.
:mod:`cat.discrete_log.analysis` therefore provides different checks for provided group parameters to see whether the specified group is vulnerable to attacks.


.. toctree::
   :glob:

   discrete_log/*

