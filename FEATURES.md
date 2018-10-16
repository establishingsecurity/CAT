# General Features
- Save and Restore Functionality in long running attacks that saves the state
  every minute or so by default.
- A fancy logo

# Basic Checks
- RSA
- ElGamal
- Diffie-Hellman
- ECDH
- (Ring-)LWE

# Analysis
- Add a method to calculate the linear approximation table for some given sbox
- Add a framework to be able to trace single bytes or even single bits through permutation steps in SPNs for example. The types have to store the beginning position in the block at least. This tracing has to survive substitutions and bitwise permutations. If necessary with it's own functions/methods for substitutions bitwise access and permutations.

# Attacks

## RSA
- Factoring
	- [x] Fermat Factoring
- Different Coppersmith Attacks
- Wiener's Attack
- Oracle Attacks
	- Bleichenbacher
	- [x] LSB-Oracle
	- ...
- Common Modulus
    - Batch GCD

## Diffie-Hellman
- Small Subgroup Attacks
- Discrete Log Algorithms
- Meneses and Wu Algorithms for DH over matrices

## (Ring-)LWE
- Fluhrer's Attack

## Hashing
- Length Extension for MD-Constructions

## TLS
- Ability to run as a TLS server and client (to test the counterpart)
- Checks of accepted and proposed parameters (SafePrimes?, KeyLength?,...)
- Array of TLS attacks of the last years
- Certificate (chain) validation attacks and nuances

## RNG

- Get LCG seed
  - see https://www.math.cmu.edu/~af1p/Texfiles/RECONTRUNC.pdf

# Helpers and Convenience
- Converter from many formats to bytes and back
- ProofOfWork Hashing
