# cat - Crypto Attack Toolkit

`cat`, the Crypto Attack Toolkit, is a Python framework to help implement cryptographic attacks against weak primitives or primitives constructed for educational purposes.

We expect `cat` to be useful in three different domains:

1. During Capture The Flag (CTF) contests while implementing attacks on cryptographic challenges
2. During penetration tests in attacking custom cryptographic implementations, and
3. As a reference for people that want to learn about cryptanalysis, by providing documentation and ready to use attacks.

Non-functional requirements and cross-cutting concerns are a major part of this project.
The main ones are the following:

* Offer a uniform interface to analyses and attacks
* Consolidation of attacks against primitives
* Attacks are accompanied by thorough and comprehensible documentation
* Each major attack is documented by an accompanying tutorial in a corresponding attack scenario
* Code is easy to read and understand with inline and external documentation
* Progress is saved during long running attacks
* Extensible and modular architecture
* The framework can be used in Python 2 and Python 3

## Why build another crypto attack library?

There are many different implementations of attacks against cryptographic primitives scattered across the internet.
Most of them suffer from a combination of the following drawbacks:

* Unmaintained
* Undocumented
* Unpackaged
* Hard to use and install
* Specific use cases or implementations are attacked
* Outright broken

In short, no framework fulfills our requirements and consolidates these code pieces.

# Documentation

You can view the documentation here: https://crave.gitlab.io/cat/

# Developer Channel

Chat with us on [Gitter](https://gitter.im/crypto-attack-toolkit).

# Install

You may install `cat` using `pip`.

## Arch Linux

From 0 to `cat`:

```bash
pacman -Sy python-pip base-devel python-virtualenv git
python -m venv .venv
. .venv/bin/activate
git clone https://gitlab.com/crave/cat.git
cd cat
pip install -e .
```

Then you can import it in python:

```python
from cat.factorize.fermat import factor

print(factor(4298375219))
```
