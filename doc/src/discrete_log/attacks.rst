Possible Attacks
================

Checks for the group's public parameters
----------------------------------------

:func:`cat.discrete_log.analysis.check_components` takes as input a generator :math:`g`, a group order :math:`q` together with a bound :math:`B` that defaults to :math:`512` and checks whether the following holds:

1. Is :math:`q` a prime number?
2. Is the bit size of :math:`q` greater than :math:`2*B`?
3. Is :math:`q` a safe prime?
4. Does :math:`g` generate a small subgroup?

If some of these checks fail, different possible attack scenarios open up. There are general purpose attacks such as `baby step-giant step`_ or `Pollard's Rho`_, which run in time :math:`\mathcal{O}(\sqrt{q} * polylog(q))`.
If the group's modulus has small prime factors then `Pohlig-Hellman decomposition`_ can be used to solve the discrete logarithm problem in :math:`\mathcal{O}(\sum_i e_i(log p + \sqrt(p_i)))` time where :math:`\prod_i p_i^{e_i}` is the prime factorization of :math:`q`.

The relation of the attacks to the performed checks is straightforward:

Non-prime Group Order
~~~~~~~~~~~~~~~~~~~~~

If the group order :math:`q` is not prime, it has smaller prime factors by definition and allows for `Pohlig-Hellman decomposition`_.

Small bit size of the group order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the security parameter defined in :math:`B` to hold (e.g. targeting 512 bit), the group order's bit size needs to be at least :math:`2*B`, due to the runtime of the general purpose algorithms `baby step-giant step`_ and `Pollard's Rho`_.

Safe prime group order
~~~~~~~~~~~~~~~~~~~~~~

Ideally the group order is a safe prime, meaning that it is of the form :math:`q = 2*p + 1` where both :math:`p` and :math:`q` are prime numbers.
If :math:`q` is of this form, then the only possible subgroup's have size :math:`1, 2, p, 2p` and any generator :math:`1 < g < p-1` generates a subgroup of order :math:`p` or :math:`2p`.
Since :math:`p` can be computed efficiently, it's easy to check whether :math:`||p|| > B` (where :math:`||p||` is the bit size of :math:`p`) and whether the given generator generates a subgroup of order :math:`p` or :math:`2p`.
This effectively prevents all listed attacks for computing discrete logarithms.

Small subgroups
~~~~~~~~~~~~~~~

There are some simple checks that can be performed efficiently to check whether the given :math:`g` generates a small subgroup.
If :math:`g` is the identity element it generates a subgroup of order :math:`1`, if :math:`g` is either :math:`0` or :math:`q` it generates a subgroup of order :math:`2`.

.. warning::
    Since it is infeasible in general to factor :math:`q`, it is possible in general that :math:`q` contains one or more small prime factors which would
    allow for small subgroups depending on the choice of :math:`g`. Ruling out small subgroups is only possible if :math:`q` is a **safe prime**!

Results
~~~~~~~

Results are returned as instances of :class:`cat.utils.result.Result`. See the bottom of the page for the results returned for discrete logarithm checks.

.. _`baby step-giant step`: https://en.wikipedia.org/wiki/Baby-step_giant-step
.. _`Pohlig-Hellman decomposition`: https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm


Checks for the Private Exponent
-------------------------------

:func:`cat.discrete_log.check_private_exponent` takes a private exponent :math:`a` as input and an optional bound :math:`B` that defaults to :math:`512`.
It returns the bit size of :math:`a` and the probability that you received a value of that bit size if you asked an RNG for a random number of size :math:`B`.
The lower the probability of the return value, the likelier it is, that there is something fishy with the RNG.


Results for Discrete Logarithm Checks
-------------------------------------

.. autoclass:: cat.discrete_log.analysis.DiscreteLogResult
    :members:
    :noindex:
