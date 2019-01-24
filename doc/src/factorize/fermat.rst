Integer Factorization
=====================

.. epigraph::

   Not all numbers of a given length are equally hard to factor.


   -- `Wikipedia`_.

.. _Wikipedia: https://en.wikipedia.org/wiki/Integer_factorization

Fermat's Factorization Method
-----------------------------

Given an *odd* number :math:`N`, find its factorization of the form:

.. math::

   N = a^2 - b^2 = (a - b)(a + b)

Such a factorization always exists for odd numbers, because if :math:`N = xy`, then it could be represented as:

.. math::

   N = \left(\frac{x + y}{2}\right)^2 - \left(\frac{x - y}{2}\right)^2

Since :math:`N` is odd, then :math:`x` and :math:`y` are also odd and the fractions are integers.


The outline of the algorithm looks like this:

.. code-block:: python

    a = sqrt(N)
    b = a * a - N

    while not is_square(b):
        a = a + 1
        b = a * a - N

    return  a - sqrt(b)

The main idea is behind the :code:`is_square(b)` test which can be done very efficiently. It turns out, that there are only 22 combinations of the last two digits that can be present in perfetc square numbers [wolfram]_. This makes the test very fast approximately three times out of four.

Another informative resource on factoring large numbers is [microsoft]_.

.. [wolfram] Fermat's Factorization Method

    http://mathworld.wolfram.com/FermatsFactorizationMethod.html

.. [microsoft] Factoring Large Numbers

    https://blogs.msdn.microsoft.com/devdev/2006/06/19/factoring-large-numbers-with-quadratic-sieve/
