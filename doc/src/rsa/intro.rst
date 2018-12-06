Rivest-Shamir-Adleman (RSA)
===========================

.. epigraph::

    One of the first public-key cryptosystems widely used for secure transmission.

    -- `Wikipedia`_.

.. _Wikipedia: https://en.wikipedia.org/wiki/RSA_(cryptosystem)

Theory of RSA key generation
----------------------------

#. Choose two primes :math:`p` and :math:`q`. These primes should be:

    - chosen at random
    - sufficiently large
    - similar in magnitude to each other
    - different in length from each other

#. Compute the product: :math:`n = pq`

    - this product is known as the *modulus*
    - this product is part of both the private and public keys
    - its length in bits is the key length (must be 1024 and above, typically 1024, 2048 or 3072)

#. Compute the Euler's totient function: :math:`\phi(n) = (p - 1)(q - 1)`

    - it shows how many integers from the segment :math:`[1, n]` are relatively prime to :math:`n`
    - any integer :math:`e` relatively prime to :math:`n` is guaranteed to have an inverse integer :math:`d` modulo :math:`n`:

    .. math:: \exists d: ed = 1 \mod n

    - the `Carmichael totient function`_ is more often computed in practice instead

    .. _Carmichael totient function: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation

#. Choose an integer :math:`e` that is relatively prime to :math:`\phi(n)`

    - this integer is commonly known as the *public RSA exponent*
    - this integer is commonly set as :math:`e = 65537`

#. Compute the inverse :math:`d` of :math:`e`:

    .. math:: ed = 1 \mod\phi(n)

    - integer :math:`d` is commonly known as the *private RSA exponent*

Quick recap of things that should be kept secret or public:

.. table::
    :align: center

    +-------------------------------+-----------------------------+
    |Secret                         |Public                       |
    +===============================+=============================+
    |primes :math:`p, q`            |modulus :math:`n`            |
    +-------------------------------+-----------------------------+
    |private RSA exponent :math:`d` |public RSA exponent :math:`e`|
    +-------------------------------+-----------------------------+
    |:math:`\phi(n)`                |                             |
    +-------------------------------+-----------------------------+

Finally, pairs :math:`(n, d)` and :math:`(n, e)` are often referred to as private and public RSA keys respectively.

Examples of RSA key generation
------------------------------

If you are using the Cryptodome_ Python library:

.. _Cryptodome: https://pycryptodome.readthedocs.io/en/latest/

.. code-block:: python

    from Cryptodome.PublicKey import RSA
    RSA.generate(bits=2048)

You could also generate RSA keys with OpenSSH_:

.. _OpenSSH: https://www.openssh.com/

.. code-block:: sh

    ssh-keygen -b 2048 -t rsa -f *file_name*

The above command generates a 2048 bit RSA key pair. It stores private key in ``file_name`` and public key ``file_name.pub``. If you set a password, it will encrypt ``file_name``.

You could also generate RSA keys with OpenSSL_:

.. _OpenSSL: https://www.openssl.org/

.. code-block:: sh

    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

From this private key, you could extract the corresponding public key by doing:

.. code-block:: sh

    openssl rsa -pubout -in private_key.pem -out public_key.pem

.. note::

    Talk about different file formats that could be used to store these keys

.. Another option is to use GnuPG_:
..
.. .. _GnuPG: https://www.gnupg.org/
..
.. .. code-block:: sh
..
..     gpg --generate-key
..
.. The above command will guide you through a sequence of prompts,
