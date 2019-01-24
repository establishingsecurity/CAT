"""Methods for computing Proof of Works."""
import hashlib
import inspect
import itertools
import re
import types
from typing import Callable, Iterator, TypeVar

from cat.utils.compat.utils import hex_str
from cat.utils.utils import generate_brute_force


def generate_with_alphabet(
    alphabet, prefix=b"", suffix=b"", min_length=0, max_length=None
):
    """
    Generator returning strings of all possible combinations of letters from the given :attr:`alphabet`
    of length :math:`i`, where :math:`\mathit{min\_length} \leq i \leq \mathit{max\_length}`.

    The :attr:`prefix` and :attr:`suffix` are prepended and appended to each yielded value, respectively.

    Shorter strings are yielded before longer ones.
    The order of the returned strings within a single length may change with each run.

    >>> lencmp = lambda x: (len(x[0]), x[0])
    >>> result = sorted(list(generate_with_alphabet('abc', min_length=1, max_length=2)), key=lencmp)
    >>> expected = [(b'a', b'a'), (b'b', b'b'), (b'c', b'c'), (b'aa', b'aa'), (b'ab', b'ab'),
    ...             (b'ac', b'ac'), (b'ba', b'ba'), (b'bb', b'bb'), (b'bc', b'bc'), (b'ca', b'ca'),
    ...             (b'cb', b'cb'), (b'cc', b'cc')]
    >>> all([r[0] == e[0] and r[1] == e[1] for r, e in zip(result, expected)])
    True

    >>> result = sorted(list(generate_with_alphabet('abc', prefix=b'hi', max_length=2)), key=lencmp)
    >>> expected = [(b'hi', b''), (b'hia', b'a'), (b'hib', b'b'), (b'hic', b'c'), (b'hiaa', b'aa'),
    ...             (b'hiab', b'ab'), (b'hiac', b'ac'), (b'hiba', b'ba'), (b'hibb', b'bb'),
    ...             (b'hibc', b'bc'), (b'hica', b'ca'), (b'hicb', b'cb'), (b'hicc', b'cc')]
    >>> all([r[0] == e[0] and r[1] == e[1] for r, e in zip(result, expected)])
    True

    :param alphabet: A set of characters
    :param prefix: A prefix to prepend to the yielded value
    :param suffix: A suffix to append to the yielded value
    :param min_length: The minimum length of the returned bytes
    :param max_length: The maximum length of the returned bytes, or None for unbounded
    :return: Generator yielding bytes
    """
    alphabet = list(set(alphabet))
    lengths = (
        range(min_length, max_length + 1) if max_length else itertools.count(min_length)
    )
    for length in lengths:
        for value in itertools.product(alphabet, repeat=length):
            guess = "".join(value).encode("utf-8")
            yield prefix + guess + suffix, guess


def wrap_hashlib(hasher, length=None):
    """
    Wraps hashlib's functions, returning a function that returns the hex-digest of its input.

    >>> from hashlib import sha1
    >>> wrap_hashlib(sha1)(b'heyo')
    'f8bb1031d6d82b30817a872b8a2ec31d5380cee5'

    :param hasher: A function from :py:module:`hashlib`
    :return: Function
    """

    args = []
    if length is not None:
        args = [length]

    def _hasher(data):
        return hasher(data).hexdigest(*args)

    return _hasher


def wrap_cryptodome(hasher, **kwargs):
    """
    Wraps cryptodome's modules, returning a function that returns the hex-digest of its input.

    >>> from Cryptodome.Hash import SHA1
    >>> wrap_cryptodome(SHA1)(b'heyo')
    'f8bb1031d6d82b30817a872b8a2ec31d5380cee5'

    :param hasher: A module from :py:class:`Cryptodome.Hash`
    :return: Function
    """

    def _hasher(byte_str):
        return hasher.new(data=byte_str, **kwargs).hexdigest()

    return _hasher


def starts_with(prefix):
    """
    Returns a function calling startswith using the given prefix on a given value.

    >>> starts_with('abc')('abc123')
    True
    >>> starts_with('123')('abc123')
    False

    :param prefix: Prefix to check
    :return: Function
    """

    def _starts_with(s):
        return s.startswith(prefix)

    return _starts_with


def ends_with(suffix):
    """
    Returns a function calling endswith using the given prefix on a given value.

    >>> ends_with('123')('abc123')
    True
    >>> ends_with('abc')('abc123')
    False

    :param suffix: Suffix to check
    :return: Function
    """

    def _ends_with(s):
        return s.endswith(suffix)

    return _ends_with


def contains(str):
    """
    Returns a function checking if the input contains the given string.

    >>> contains('123')('abc123')
    True
    >>> contains('fgh')('abc123')
    False

    :param str: String that must be contained in the string that's given to the returned function
    :return: function
    """

    def _contains(s):
        return str in s

    return _contains


def lor(*fns):
    """
    Functionally logical ors the given functions.

    >>> lor(starts_with('123'), ends_with('asd'))('asd')
    True
    >>> lor(starts_with('123'), ends_with('asd'))('123')
    True
    >>> lor(starts_with('123'), ends_with('asd'))('fgh')
    False

    :param fns: Functions to or
    :return: False if none of the functions returned a truthy value, the truthy value otherwise.
    """

    def _f(*args, **kwargs):
        for f in fns:
            v = f(*args, **kwargs)
            if v:
                return v
        return False

    return _f


def land(*fns):
    """
    Functionally logical ands the given functions.

    >>> lor(starts_with('123'), ends_with('asd'))('123asd')
    True
    >>> land(starts_with('123'), ends_with('asd'))('asd')
    False
    >>> land(starts_with('123'), ends_with('asd'))('123')
    False

    :param fns: Functions to and
    :return: True if all of the functions return a truthy value, otherwise the first falsey value
    """

    def _f(*args, **kwargs):
        for f in fns:
            v = f(*args, **kwargs)
            if not v:
                return v
        return True

    return _f


_MEMBERS = dict(inspect.getmembers(hashlib))


def is_hashlib(obj):
    """
    :param obj: Any object
    :return: True iff obj is an algorithm from :py:module:`hashlib`.
    """
    algorithms = _MEMBERS["algorithms_guaranteed"]
    return obj in map(lambda x: _MEMBERS[x], algorithms)


def hash_pow(
    alphabet,
    hash_fn,
    prefix=b"",
    suffix=b"",
    hash_prefix="",
    hash_suffix="",
    min_length=0,
    max_length=None,
    condition=None,
):
    """
    Computes a :math:`g` such that:

    .. math::
        H_\it{hex}(\mathit{prefix} \| g \| \mathit{suffix}) = \mathit{hash\_prefix} \| \ldots \| \mathit{hash\_suffix}

    Where :math:`H_\it{hex}` is a function returning the hexadecimal digest of its input.

    >>> from Cryptodome.Hash import SHA1
    >>> response = hash_pow('abc', SHA1, prefix=b'challenge', hash_prefix='fff')
    >>> assert SHA1.new(b'challenge' + response).hexdigest().startswith('fff')

    :param alphabet: Letters to use in :math:`g`
    :param hash_fn: Hash function, e.g. hashlib.sha256 or Cryptodome.Hash.SHA256
                    Accepts arbitrary functions that turn data into a string
    :param prefix: Prefix prepended to the guess
    :param suffix: Suffix appended to the guess
    :param hash_prefix: The resulting digest must start with these bytes
    :param hash_suffix: The resulting digest must end with these bytes
    :param condition:   Additional condition the digest must conform to
    :param min_length: minimum length of :math:`g`
    :param max_length: maximum length of :math:`g`
    :return: :math:`g`
    """
    hash_condition = land(starts_with(hash_prefix), ends_with(hash_suffix))
    if condition:
        hash_condition = land(condition, hash_condition)

    if (
        isinstance(hash_fn, types.ModuleType)
        and hash_fn.__package__ == "Cryptodome.Hash"
    ):
        hash_fn = wrap_cryptodome(hash_fn)
    elif is_hashlib(hash_fn):
        hash_fn = wrap_hashlib(hash_fn)
    if not isinstance(hash_fn, types.FunctionType):
        raise Exception("Invalid hash function")
    values = generate_with_alphabet(
        alphabet,
        prefix=prefix,
        suffix=suffix,
        min_length=min_length,
        max_length=max_length,
    )
    return compute(hash_condition, hash_fn, values)[1]


def with_pattern(pattern):
    """
    Compute a Proof of Work based on the given pattern.

    >>> # Compute a digest that starts and ends with a '1'
    >>> from Cryptodome.Hash import SHA1
    >>> guess = hash_pow('abc', SHA1, prefix=b'challenge', condition=with_pattern(r'^1{h}1$'))
    >>> digest = SHA1.new(b'challenge' + guess).hexdigest()
    >>> assert digest[0] == '1' and digest[-1] == '1'

    >>> # Compute a digest with '123' somewhere
    >>> guess = hash_pow('abc', SHA1, prefix=b'challenge', condition=with_pattern(r'{h}123{h}'))
    >>> digest = SHA1.new(b'challenge' + guess).hexdigest()
    >>> assert '123' in digest

    >>> # Compute a digest with '1', '2' and '3' separated by at least one
    >>> # value in-between
    >>> guess = hash_pow('abc', SHA1, prefix=b'challenge', condition=with_pattern(r'{h}1{h}2{h}3{h}'))
    >>> digest = SHA1.new(b'challenge' + guess).hexdigest()
    >>> # Check solution
    >>> assert re.match(r'.*1.*2.*3.*', digest)

    :param pattern:       The regex pattern that the resulting digest should conform to.
                          You can insert '{h}' wherever you want non fixed values, or '{h+}'
                          for an optional non fixed value (i.e. '{h+}' can result in '', '{h}'
                          reliably results in some character in the digest), which is just
                          r'\w+' and r'\w*' for people who hate regex.
                          The rest of the string is interpreted as a regex pattern. You want
                          to use the `r` prefix for Python to interpret the string as 'raw',
                          allowing you to avoid the backslash plague (e.g. you can pass `\d`
                          as `r'\d'` instead of `'\\d'`).
    :type pattern:        :class:`str`
    :param hash_function: The hash function to use (e.g. :class:`Crypto.Hash.SHA256.SHA256Hash`).
    :type hash_function:  All modern and history hash algorithms listed in :doc:`src/hash/hash`.
    :param input_source:  A generator that creates input values for the hash function. Defaults
                          to brute force starting at `0`.
    :type input_source:   :class:`generator`
    :param action:        An action performed on the `base_input` and the values from the
                          `input_source`. Defaults to appending the values to `base_input`.
    :type action:         :class:`function`
    :returns:             A bytestring that produces a `hash_function` hexdigest of the form
                          specified by `pattern` when used as input for `hash_function.new`.
                          `suffix`.
    :rtype:               :class:`bytes`
    """

    p = re.compile(pattern.format(**{"h": r"\w+", "h+": r"\w*"}))

    def _with_pattern(s):
        return p.match(s)

    return _with_pattern


ReturnType = TypeVar("ReturnType")
Guess = TypeVar("Guess")
Hash = TypeVar("Hash")


def compute(condition, fn, values_source):
    # type: (Callable[[Hash], bool], Callable[[ReturnType], Hash], Iterator[(Guess, ReturnType)]) -> (Guess, ReturnType)
    """
    Returns the first return-value from the generator where :code:`condition(fn(guess))` returns True.


    >>> # Define a simple input source
    >>> def input_source(start):
    ...     for bf in generate_brute_force(start):
    ...         yield bytes(bf), bf
    >>> # Instantiate a generator
    >>> generator = input_source([0])
    >>> # Compute a digest with '123' somewhere
    >>> condition = lambda d: '123' in d
    >>> from Cryptodome.Hash import SHA1
    >>> guess, _ = compute(condition, wrap_cryptodome(SHA1), generator)
    >>> assert '123' in SHA1.new(data=guess).hexdigest()

    :param condition:     A function checking whether a given  fulfills the proof of
    :type condition:      function(x: :class:`bytes`) -> :class:`bool`
    :param fn:            A function returning a :type:`Hash`
    :param input_source:  A generator that creates input values for the hash function.
    :type input_source:   :class:`generator` -> :class:`bytes`
    :returns:             A bytestring that produces a `hash_function` hexdigest of the form
                          specified by `condition` when used as input for `hash_function.new`.
    :rtype:               :class:`bytes`
    """

    for guess, rv in values_source:
        if condition(fn(guess)):
            return guess, rv
