"""
A collection of utility functions.
"""
import dask.bag as parallel


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


def pmap(function, *inputs, filter_=None):
    # type: (Callable[Any, Any], Iterable[Iterable[Any]], Callable[Any, Any]) -> Iterable[Any]
    """
    Do a parallel map of the given :code:`function` on the given :code:`inputs` and optionally
    filter its results with :code:`filter_`. This is a simple wrapper for `dask`_ and works
    like :func:`map` but in parallel.

    .. code-block:: python

      fun = lambda d: SHA1.new(d).hexdigest()
      inputs = [b'1234', b'5678', b'9101', b'1121']
      assert (pmap(fun, inputs) ==
          ['7110eda4d09e062aa5e4a390b0a572ac0d2c0220',
           '2abd55e001c524cb2cf6300a89ca6366848a77d5',
           'f5a6fe40024c28967a354e591bb9fa21b784bf00',
           '784e9240155834852dff458a730cceb50229df32'])

      filter_ = lambda d: d.endswith('0')
      assert (pmap(fun, inputs, filter_=filter_) ==
          ['7110eda4d09e062aa5e4a390b0a572ac0d2c0220',
           'f5a6fe40024c28967a354e591bb9fa21b784bf00'])

    .. _`dask`: https://docs.dask.org/en/latest/

    :param function:    An arbitrary function that's mapped to the :code:`inputs`.
    :param inputs:      Inputs for :code:`function`. Pass multiple if your function
                        takes multiple inputs.
    :param filter_:     An optional filter function to filter the results of the
                        computation. If none is passed, all results will be returned.
    :returns:           The results of applying :code:`function` to :code:`inputs`.

    .. CAUTION::
       :code:`filter_` needs to be passed as a **keyword argument**, otherwise it will
       be treated as an input parameter to :code:`function`!
    """
    promises = parallel.map(function, *[parallel.from_sequence(i) for i in inputs])
    if not filter_:
        return list(promises)
    else:
        return list(promises.filter(filter_))
