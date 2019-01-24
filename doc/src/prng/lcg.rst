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


Attacking Truncated Lehmer Style LCGs
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
    B \cdot \vec{s} &= m \cdot \vec{k}\\
    B \cdot (\vec{l} + \vec{h}) &= m \cdot \vec{k}\\
    B \cdot \vec{l} &= m \cdot \vec{k} - B \cdot \vec{h}\\

where :math:`\vec{k}` is unknown and :math:`\vec{l}` and :math:`\vec{h}` are the
low and high bits of the state vector :math:`\vec{s}`, respectively.
We expect the unknown :math:`\vec{k}` to be small and can then solve for
:math:`\vec{l}` when given the high bits of the states :math:`\vec{h}`.
If we manage to retrieve the low bits :math:`\vec{l}` we can combine them with
:math:`\vec{h}` again and compute the state vector :math:`\vec{s}`.

Attacking Full LCGs (with increment)
------------------------------------

By subtracting consecutive states of an LCG we obtain again a Lehmer style LCG:

.. math::
    s_2 - s_1 &\equiv a^0 ((a-1)s_1 + b) &\mod m\\
    s_3 - s_2 &\equiv a^1 ((a-1)s_1 + b) &\mod m\\
    s_4 - s_3 &\equiv a^2 ((a-1)s_1 + b) &\mod m\\
    \vdots\\
    s_{i+1} - s_i &\equiv a^{i-1} ((a-1)s_1 + b) &\mod m

If we knew the upper bits of the differences, we could, using the above attack, recover the state :math:`((a-1)s_1 + b)` of the derived Lehmer style LCG, containing the desired :math:`s_1`.

Let :math:`h^l_i = \lfloor \frac{s_{i+1} - s_i}{2^\ell} \rfloor` be the upper bits of the derived Lehmer style LCG.

We don't know the exact differences :math:`h^l_i`, since we only know the upper bits :math:`h_i` of the full LCG.
The uncertainty stems from the carry bit during subtraction.
Thus, we simply guess the carry bit of each subtraction:

.. math::
    h^l_i = \begin{cases}
	h_{i+1} - h_i & \text{if no carry}\\
	h_{i+1} - h_i - 2^\ell & \text{if carry}
    \end{cases}

For each combination of guessed carry bits we obtain :math:`s^l_1 = ((a-1)s_1+b)` by the Lehmer style LCG attack, from which we recover the initial state of the full LCG:

If :math:`\gcd(a-1, m) = 1`, then :math:`a-1` is invertible modulo :math:`m`, and we simply compute :math:`s_1` as:

.. math::
    s^l_1 &\equiv (a-1)s_1+b &\mod m\\
    s^l_1 - b&\equiv (a-1)s_1 &\mod m\\
    {(s^l_1 - b)}{(a-1)}^{-1}&\equiv s_1 &\mod m\\

Otherwise, if :math:`\gcd(a-1, m) = d \neq 1`, there may be no or no unique pre-image.

.. math::
    s^l_1 &\equiv (a-1)s_1+b &\mod m\\
    s^l_1 - b&\equiv (a-1)s_1 &\mod m\\
    \frac{s^l_1 - b}{d}&\equiv \frac{(a-1)}{d}s_1 &\mod \frac{m}{d}\\

If :math:`s^l_1 - b` is not divisible by :math:`d`, no solution exists.
Otherwise, we can now invert :math:`\frac{(a-1)}{d} \mod \frac{m}{d}`, and compute a set of :math:`d` candidates:

.. math::
    s_1 \in \Big\{\frac{s^l_1 - b}{d} * {\Big(\frac{(a-1)}{d}\Big)}^{-1} + \frac{m}{d} \cdot k \mod m \mid k\in \{1, \dots, d\}\Big\}


.. [LLLLCG] https://crypto.stackexchange.com/questions/37836/problem-with-lll-reduction-on-truncated-lcg-schemes
.. [LCGBB] https://crypto.stackexchange.com/questions/20495/how-brittle-are-lcg-cracking-techniques
