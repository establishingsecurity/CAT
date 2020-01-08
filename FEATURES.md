# General Features

A set of general features that we feel are important to have a usable framework.
We feel that they are implemented to an acceptable degree in the current state (Documentation for example can always be better) and we'd like them to be considered when implementing further analysis and attack techniques.

- [x] Save and Restore Functionality in long running attacks that saves the state on return.
- [x] Python2 and Python3 support
- [x] Great Documentation you can learn from
- A fancy logo ~hard

# Basic Checks

Basic checks are implemented for different primitives to catch mistakes in deployment and general usage of them.
They are easily overlooked on CTF Challenges and Assessments and can often be detected by performing simple checks on available data and parameters.

- [x] RSA
- [x] ElGamal
- [x] Diffie-Hellman
- ECDH ~easy
- LWE/RLWE/MLWE/LWR/... ~advanced

# Symmetric

Techniques that help in the analysis of symmetric primitives.

- Add a method to calculate the linear approximation table for some given sbox ~advanced
- Add a framework to be able to trace single bytes or even single bits through permutation steps in SPNs for example. The types have to store the beginning position in the block at least. This tracing has to survive substitutions and bitwise permutations. If necessary with it's own functions/methods for substitutions bitwise access and permutations. ~hard
- Half-Trivium attack ~advanced

## RSA

Analysis techniques and attacks for the RSA Cryptosysytem.

- Factoring
    - [x] Fermat Factoring
    - ...
- Different Coppersmith-like Attacks ~hard
    * Boneh-Durfee-Frankel ~hard
    * ...
- Wiener's Attack ~advanced
* Boneh-Durfee ~hard
- Oracle Attacks
    - Bleichenbacher ~advanced
    - [x] LSB-Oracle
    * Automate Oracle attacks https://eprint.iacr.org/2019/958
	- ...
- Common Modulus
    - [x] Batch GCD

## Diffie-Hellman

Analysis techniques and attacks for the Diffie-Hellman-Merkle Key Exchange.

- Small Subgroup Attacks ~hard
- Discrete Log Algorithms ~hard
- Meneses and Wu Algorithms for DH over matrices ~hard

## (EC)DSA

* Nonce Reuse ~easy
* Weak Nonce Generators ~advanced to ~hard

## LWE

Analysis techniques and attacks for schemes based on LWE/RLWE/MLWE/LWR/... .

- Fluhrer's Attack (https://eprint.iacr.org/2016/085.pdf) ~hard

## Hashing

Analysis techniques and attacks for schemes based on cryptographic hashing.

- [x] Length Extension for MD-Constructions
- [x] ProofOfWork Hashing

## TLS

Analysis techniques and attacks for the TLS stack.

- Ability to run as a TLS server and client (to test the counterpart) ~easy
- Checks of accepted and proposed parameters (SafePrimes?, KeyLength?,...) ~easy
- Array of TLS attacks of the last years ~hard
- Certificate (chain) validation attacks and nuances ~advanced

## PRNG

Analysis techniques and attacks for Pseudo Random Number Generators.

- [x] Get LCG seed
- get secret LCG parameters (see https://link.springer.com/chapter/10.1007%2F11506157_5) ~advanced
- Mersenne Untwister (see e.g. https://www.ambionics.io/blog/php-mt-rand-prediction) ~advanced
