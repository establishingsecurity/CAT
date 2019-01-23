.. cat documentation master file, created by
   sphinx-quickstart on Sun Oct 28 18:08:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cat's documentation!
===============================

The Cryptographic Attack Toolkit is a library implementing and explaining attacks in a general way.

We expect cat to be useful in three different domains:

1. During Capture The Flag (CTF) contests while implementing attacks on cryptographic challenges
2. During penetration tests in attacking custom cryptographic implementations, and
3. As a reference for people that want to learn about cryptanalysis, by providing documentation and ready to use attacks.

Non-functional requirements and cross-cutting concerns are a major part of this project.
The main ones are the following:

- Offer a uniform interface to analyses and attacks
- Consolidation of attacks against primitives
- Attacks are accompanied by thorough and comprehensible documentation
- Each attack is documented by an accompanying tutorial in a corresponding attack-scenario
- Progress is saved periodically or between stages during long running attacks
- Extensible and modular architecture
- The framework can be used in Python 2 and Python 3

Installation
------------

Soon you should be able to :code:`pip install <InsertPyPi Name>`. For now, refer to :file:`CONTRIBUTE.md` for installation instructions.

.. toctree::
   :maxdepth: 4
   :caption: Contents

   rsa.rst
   hash.rst
   utils.rst
   symmetric.rst


Package and Module Index
------------------------

.. toctree::
   :glob:
   :maxdepth: 4

   modules/cat.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
