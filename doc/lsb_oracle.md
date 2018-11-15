The Least Significant Bit Oracle attack is a simpler variation of
Bleichenbacher.

It assumes a decryption oracle `$ LSB(\cdot) $` that accepts ciphertexts and returns the
least significant or parity bit of the decrypted plaintext.

This oracle leaks at least one bit of the plaintext, but can be used to reveal the whole plaintext using the multplicative homomorphic property of RSA.


# Intuition

!!! note
    RSA is multiplicative homomorphic, i.e `$ a^e * v^e \equiv (a * b)^e \mod N $`

We use the homomorphic property, i.e `$ 2^e * m^e \equiv (2 * m)^e \mod N $`, and the fact that we can construct `$ 2^e \mod N $` because we assume we have the public key `$ (e, N) $`.

Multiplying this value to our target ciphertext yields `$ (2 * m)^e \mod N $`, which we can query the LSB oracle with.

The value `$ (2 * m) $` is an even, if the answer to our query is `$ 1 $`, we conclude that `$ (2 * m) \ge N $`.
If it reveals 0, then `$ 2^c m \leq N $` must hold.
The resulting inequality reveals a bound on the plaintext.



The attack works as follows:

1. Set the current ciphertext as the target ciphertext
2. Set the counter `$ c $` to `$ 0 $`
3. Query for the LSB of the current ciphertext. \
4. Set the current ciphertext to `$ c \dot 2^e \mod N $`.
5. Increase the counter.
6. Repeat until you narrowed the searchspace of the plaintext enough.
