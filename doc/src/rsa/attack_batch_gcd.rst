Batch GCD attack on RSA
=======================

.. note::

    Another gentle introduction into RSA and batch GCD attack could be found in
    [schoen]_.


An important thing to remember when trying to understand this attack is that multiplying two numbers is *a lot* faster than taking the product and breaking it down into factors. For example, you could probably compute the following product with pen and pencil in about two minutes (and in milliseconds with a computer):

.. math::

         17477852958781876547 \times 15241555427044345769

However, checking that just the second of those integers is a prime would take you about ten *minutes* of processing time. This is a huge difference!

In a different twist of algorithmic complexity, it turns out that if you are given two numbers, then computing their common factors is a much *quicker* operation then trying to factorize even just one of those numbers. In other words, a computer could check in milliseconds that there are no common factors for the two numbers above.

So, when you are presented with two (or more) values for the RSA modulus :math:`n_1 = p_1 q_1` and :math:`n_2 = p_2 q_2`, you generally cannot hope to be able to factorize :math:`n_1` or :math:`n_2` on their own. However, you could quickly check if :math:`n_1` and :math:`n_2` accidentally share the same factor.

Finally, suppose you collect a large number of different values for the RSA modulus. Checking each pair would take you a quadratic number of calls of the GCD algorithm with two large input values. What the batch GCD algorithm allows you to achieve is a linear number of calls of the GCD algorithms at the cost of building some additional data structures.

For the details behind those data structures, please take a look at `attack_batch_gcd.py`, which was implemented partially based on [bernstein-et-al]_.

Other implementations of the batch GCD algorithm that might be useful:

#. https://factorable.net/resources.html
#. https://github.com/dieggoluis/RSA-Attack


.. [schoen] Understanding Common Factor Attacks: An RSA-Cracking Puzzle

    http://www.loyalty.org/~schoen/rsa/

.. [bernstein-et-al] RSA factorization in the real world

    http://facthacks.cr.yp.to/batchgcd.html
