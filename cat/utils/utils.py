"""
A collection of utility functions.
"""

def generate_brute_force(start):
    """
    A generator for brute-forcing. Given a start value `start` the generator
    yields an array of integers in the range 0-256 (i.e. byte values) that can
    be interpreted as a binary number (in big endian) that is increased by 1
    on each iteration.

    >>> brute = generate_brute_force([0])
    >>> next(brute)
    [0]
    >>> next(brute)
    [1]
    >>> next(brute)
    [2]
    >>> for i, bf in enumerate(generate_brute_force([0])):
    ...     if i == 256:
    ...         guess = bf
    ...         break
    ...
    >>> print(guess)
    [1, 0]
    >>> print(bytes(guess))
    b'\\x01\\x00'

    :param start:       A start value for the brute force attempt.
    :type start:        :class:`list` [:class:`int`]
    """
    length = len(start)

    def next_value(value, carry):
        carry = False
        sum_ = (value + 1 + carry) % 256
        if sum_ < value:
            carry = True
        return (carry, sum_)

    while True:
        val = start.copy()
        yield val
        carry = 0
        for i in range(length-1, -1, -1):
            carry, start[i] = next_value(start[i], carry)
            if not carry:
                break
        if carry:
            start.insert(0, 1)
            length += 1
