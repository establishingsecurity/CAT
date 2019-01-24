Linear Congruential Generators
==============================

.. math::
    \newcommand{\lat}{\mathcal{L}}
    \DeclareMathOperator{\LLL}{LLL}


.. TODO Change vector and matrix/basis notation to bold?

Linear Congruential Generators, or LCGs, are a type of random number generator.
They are parameterized by:

* a multiplier :math:`a`
* an increment :math:`b`
* a modulus :math:`m`

The LCG is initialized with a seed :math:`s_0`.
The outputs of the LCG are computed by the recurrence relation

.. math::
    s_{i+1} = a \cdot s_i + b \mod m

If the modulus is :math:`n` bits long, the LCG has about :math:`n` bits state.

A simple generator of this form provides no security at all, because we get the
full state as output and are able to generate all the following states
ourselves.
Because of this a truncated variant of the LCG is used, where the output only
consists of a few bits of the state. Most implementations output the most
significant half of the state bits: :math:`h_i = \lfloor{\frac{s_i}{2^\ell}}\rfloor`.


Attacking Truncated Lehmer style LCGs
-------------------------------------

.. warning::
    The following attack to reconstruct a state contains heavy math.
    Knowledge of linear algebra and lattices will be helpful.

    Viewer discretion is advised.


A Lehmer style LCG is a simpler form of an LCG where the increment :math:`b` is
set to 0, yielding the recurrence relation:

.. math::
    s_{i+1} = a \cdot s_i \mod m

Given the parameters :math:`a, m` and consecutive truncated outputs :math:`h_1, \dots, h_l` of a Lehmer style LCG,
we can reconstruct the states :math:`s_1, \dots, s_l`.

We first construct a system of linear congruences from the parameters, such that
evaluating the congruences on valid LCG states yields a zero value modulo
:math:`m`, like

.. math::

    M s_1 &= 0 \\
    a s_1 - s_2 &= 0 \\
    a^2 s_1 - s_3 &= 0 \\
    \dots

.. TODO matrix structure

The matrix form of these equations builds a lattice, the dual of the lattice
contains all the possible solutions of an LCG with the specified parameter set.

.. TODO Check the claim about the dual lattice again

.. note::

    An :math:`n`-dimensional lattice :math:`\lat` is a discrete additive subgroup of :math:`\mathcal{R}^n`,
    where discrete means that there is a neighborhood around each lattice vector :math:`\vec{v}` in which :math:`\vec{v}` is the only lattice vector

    An additive subgroup of :math:`G` is a subset :math:`U` of :math:`G`
    such that for any elements :math:`a, b \in U`
	* :math:`-a \in U`
	* :math:`a + b \in U`

    :math:`U` with the same operation as on :math:`G` is then a group itself.

We now have the Lehmer style LCG in lattice form and can apply the :math:`\LLL` algorithm
to the lattice basis to obtain a different basis :math:`B` of the same lattice with
shorter basis vectors.

.. note::

    Pretty simplified, :math:`\LLL` is a lattice basis reduction algorithm.
    Given an arbitrary basis of a lattice, it computes a basis for the same
    lattice that is better in the sense that the basis vectors are shorter.

For the basis :math:`B` and LCG states as a vector :math:`\vec{s}` the equations

.. math::
    B \cdot \vec{s} &\equiv 0 &\mod m \\
    B \cdot \vec{s} &\equiv m \cdot \vec{k} &\mod m\\
    B \cdot (\vec{l} + \vec{h}) &\equiv m \cdot \vec{k} &\mod m\\
    B \cdot \vec{l} &\equiv m \cdot \vec{k} - B \cdot \vec{h} &\mod m\\

where :math:`\vec{k}` is unknown and :math:`\vec{l}` and :math:`\vec{h}` are the
low and high bits of the state vector :math:`\vec{s}`, hold true.
We expect the unknown :math:`\vec{k}` to be small and can then solve for
:math:`\vec{l}` when given the high bits of the states :math:`\vec{h}`.
If we manage to retrieve the low bits :math:`\vec{l}` we can combine them with
:math:`\vec{h}` again and compute the state vector :math:`\vec{s}`.
