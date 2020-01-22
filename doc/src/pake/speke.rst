Simple Password Exponential Key Exchange (SPEKE)
================================================

The Simple Password Exponential Key Exchange protocol (SPEKE) is one of the easier PAKE protocols that exist.
It was invented by David P. Jablon in 1996 and could be seen as a extension of the basic Diffie-Hellman key exchange.
Due to the simplicity of this protocol, it is one of the most well known PAKE protocols.
Furthermore, it is even can be found in the standards IEEE 1363.2 and ISO/IEC 11770-4.
Another point that makes this protocol interesting is, that it is/was also used in in commercial products like BlackBerry devices.


However, the SPEKE protocols have some serious security flaws. One example is, that a Unknown Key Share (UKS) attack is possible.
To understand the Unknown Key Share attack in its detail, it is important to take a closer look at the SPEKE protocol.

SPEKE Protocol
--------------

The protocol consists of two stages, the first one is a DH key exchange.
The DH key exchange in the SPEKE protocol has a speciality, the primitive base, is not fixed, instead the chosen password is converted into a suitable base.
In the second stage, both parties proof the knowledge of the shared secrete K to each other. After that both uses K as session key.
The complete protocol flow can be seen in figure below.


To be able to understand the protocol flow in every detail, the most important symbols used in figure below listed below.
	* S: shared password between A and B
	* f(S): a function for converting the low-entropy password S to a DH base.
	* h(m): a strong one-way hash function
	* K: the established session key

.. image:: ../figures/speke.*
   :width: 100 %

Instead of verifying the hashes of the session key, it is also possible to send an random challenge that is encrypted to the opponent.
In this case Bob needs to answer with an encrypted message, that contains both, the challenge from Alice and his own.
However, this form of verifying the opponent needs one additional communication step, if not optimized.
Also the function that converts the password to a suitable DH-base must be chosen very carefully.

For the function that converts a password into a suitable DH base, Jablon makes two suggestion.
The first one is :math:`f(S) = g_q^S mod p`, where :math:`g_q` is of order :math:`q`.
The second suggestion is :math:`f(S) = S^{(p-1)/q} mod p`, this version is used in the example implementation, where I showed, that an UKS attack on the SPEKE protocol could be done with very little effort.

Unknown Key Share (UKS) attack
-------------------------------

For this attack it is assumed that parties, that implement the SPEKE protocol are able to establish several concurrent SPEKE sessions.
Furthermore, the parties Alice (A) and Bob (B) share a common password.
In the figure below the protocol flow of the attack can be seen. In this case Mallory (M) impersonates Bob.
Alice initiates the protocol by picking a random :math:`a` from :math:`Z_p` and then sending Bob the message :math:`g^a`.
Mallory intercepts this message and picks a random value $b$ from :math:`Z_p` and raise the intercepted message to the power of :math:`b`.
Mallory initiates another session with Alice, pretending being Bob and sends :math:`g^ab` to Alice.
Alice answers in the second session with :math:`g^c`, where $c$ is an arbitrary value out of :math:`Z_p`.
Mallory raise :math:`g^c` by the power of $b$ and sends the new value to the first session with Alice.
With the use of :math:`b` Mallory is able to create two different messages, hence Alice has to consider both sessions as valid.
Alice generates in the first session the
After this step, Mallory forwards the verification messages.
Now Alice has established a valid Session with herself over Mallory, but thinks she is talking to Bob twice.

.. image:: ../figures/speke_uks.*
    :width: 100 %

In this attack Mallory is not able to decrypt any of the messages. However, since Alice has established a valid connection, Mallory just can forward all messages.
This could be for example a problem in an banking environment, with automated systems, where Alice sends the request "send me 100 Euro" to Bob.
If Mallory hosts the described UKS attack, then Alice gets on a second session her request from Bob, resulting her sending Bob 100 Euro.
