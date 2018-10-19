# General Features
- Save and Restore Functionality in long running attacks that saves the state
  every minute or so by default.
- Python2 and Python3 support
- Great Documentation you can learn from
- A fancy logo

# Basic Checks [easy]
- RSA
- ElGamal
- Diffie-Hellman
- ECDH
- (Ring-)LWE

# Symmetric

- Add a method to calculate the linear approximation table for some given sbox [advanced]
- Add a framework to be able to trace single bytes or even single bits through permutation steps in SPNs for example. The types have to store the beginning position in the block at least. This tracing has to survive substitutions and bitwise permutations. If necessary with it's own functions/methods for substitutions bitwise access and permutations. [???]
- Half-Trivium attack

# Attacks

## RSA
- Factoring
    - [x] Fermat Factoring [easy]
    - ...
- Different Coppersmith Attacks [work in progress]
- Wiener's Attack [advanced]
- Oracle Attacks
    - Bleichenbacher [advanced]
    - [x] LSB-Oracle [easy]
	- ...
- Common Modulus
    - Batch GCD [easy]

## Diffie-Hellman
- Small Subgroup Attacks [hard]
- Discrete Log Algorithms [hard]
- Meneses and Wu Algorithms for DH over matrices [hard]

## (Ring-)LWE
- Fluhrer's Attack (https://eprint.iacr.org/2016/085.pdf) [???]

## Hashing
- Length Extension for MD-Constructions [easy]

## TLS
- Ability to run as a TLS server and client (to test the counterpart) [easy]
- Checks of accepted and proposed parameters (SafePrimes?, KeyLength?,...) [easy]
- Array of TLS attacks of the last years
- Certificate (chain) validation attacks and nuances [advanced]

## RNG

- Get LCG seed [advanced]
  - see https://www.math.cmu.edu/~af1p/Texfiles/RECONTRUNC.pdf
- get secret LCG parameters
  - see https://link.springer.com/chapter/10.1007%2F11506157_5
- Mersenne Untwister

# Helpers and Convenience
- Converter from many formats to bytes and back [easy]
- ProofOfWork Hashing [easy]
