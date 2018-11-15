The Least Significant Bit Oracle attack is a simpler variation of
Bleichenbacher.

It assumes a decryption oracle $LSB(\dot)$ that accepts ciphertexts and returns the
least significant or parity bit of the decrypted plaintext.

This oracle leaks at least one bit of the plaintext, but can be used to reveal the whole plaintext using the multplicative homomorphic property of RSA.

The attack works as follows:

1. Set the current ciphertext as the target ciphertext
2. Set the counter $c$ to $0$
3. Query for the LSB of the current ciphertext. \
    If the bit is $0$, $2^c m \leq N$ holds.\
    If the bit is $1$, $2^c m \ge N$ holds.
4. Set the current ciphertext to $c \dot 2^e \mod N$.
5. Increase the counter.
6. Repeat until you narrowed the searchspace of the plaintext enough.
