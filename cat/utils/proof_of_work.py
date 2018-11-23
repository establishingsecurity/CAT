"""Methods for computing Proof of Works."""
import re
import types

from Cryptodome.Hash import SHA1

from cat.utils.compat.utils import hex_str
from cat.utils.utils import generate_brute_force
import itertools


def generate_with_alphabet(alphabet, prefix=b'', suffix=b'', min_length=1, max_length=None):
    alphabet = list(set(alphabet))
    lengths = range(min_length, max_length + 1) if max_length else itertools.count(min_length)
    for length in lengths:
        for value in itertools.product(alphabet, repeat=length):
            yield prefix + bytes(''.join(value), 'utf-8') + suffix


def wrap_hashlib(hasher):
    def _hasher(data):
        return hasher(data).hexdigest()

    return _hasher


def wrap_cryptodome(hasher):
    def _hasher(byte_str):
        return hasher.new(byte_str).hexdigest()

    return _hasher


def starts_with(prefix):
    def _starts_with(s):
        return s.startswith(prefix)

    return _starts_with


def ends_with(prefix):
    def _starts_with(s):
        return s.startswith(prefix)

    return _starts_with


def lor(*fns):
    """
    Functionally logical ors the given functions

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


def compute_suffix(hash_function, prefix, condition, input_source, **kwargs):
    """
    Compute a `suffix` for the given `prefix` and `input_source`, such that the resulting hash
    digest satisfies the given `condition`.

    >>> # Define a value source
    >>> def input_source(start):
    ...     for bf in generate_brute_force(start):
    ...         yield bytes(bf)
    >>> # Instantiate a generator
    >>> generator = input_source([0])
    >>> # Compute a hash digest whose hex representation ends with '123'
    >>> condition = lambda g: hex_str(g).endswith('123')
    >>> prefix = b'Hello, world!'
    >>> guess, suffix = compute_suffix(SHA1, prefix, condition, generator)
    >>> print(SHA1.new(suffix).hexdigest())


    :param prefix:        The prefix of the input to `hash_function`.
    :type prefix:         :class:`bytes`
    :param hash_function: The hash function to use (e.g. :class:`Crypto.Hash.SHA256.SHA256Hash`).
    :type hash_function:  All modern and historic hash algorithms listed in :doc:`src/hash/hash`.
    :param input_source:  A generator that creates input values for the hash function.
    :type input_source:   :class:`generator`
    :param kwargs:        Additional keyword arguments that get passed to `hash_function.new`
                          (e.g. `digest_bytes` for :class:`Crypto.Hash.BLAKE2s`).
    :type kwargs:         :class:`dict`
    :returns:             The computed suffix, such that `hash_function.new(prefix + suffix).digest()`
                          fulfills `condition`.
    :rtype:               :class:`bytes`
    """

    def wrap_input_source():
        for i in input_source:
            yield prefix + i

    return compute(hash_function, condition, wrap_input_source(), **kwargs)


def hash_pow(alphabet, hash_fn, prefix=b'', suffix=b'', hash_prefix='', hash_suffix=''):
    def _starts_or_endswith(h):
        h = hex_str(h)
        return h.startswith(hash_prefix) or h.endswith(hash_suffix)

    if type(hash_fn) is types.ModuleType and hash_fn.__package__ == 'Cryptodome.Hash':
        hash_fn = wrap_cryptodome(hash_fn)
    elif type(hash_fn) is types.BuiltinFunctionType and hash_fn.__module__ == '_hashlib':
        hash_fn = wrap_hashlib(hash_fn)
    if type(hash_fn) is not function:
        raise Exception('Invalid hash function')
    return compute(_starts_or_endswith, hash_fn, generate_with_alphabet(alphabet, prefix=prefix, suffix=suffix))


def compute_prefix(hash_function, suffix, condition, input_source, **kwargs):
    """
    Compute a `prefix` for the given `suffix`, such that the digest of `hash_function` with an input
    of `prefix + suffix` fulfills `condition`.

    >>> # Define a value source
    >>> def input_source(start):
    ...     for bf in generate_brute_force(start):
    ...         yield bytes(bf)
    >>> # Instantiate a generator
    >>> generator = input_source([0])
    >>> # Compute a hash digest whose hex representation starts with '123'
    >>> condition = lambda g: hex_str(g).startswith('123')
    >>> suffix = b'Goodbye, world!'
    >>> guess = compute_prefix(SHA1, suffix, condition, generator)

    :param suffix:        The suffix of the input to `hash_function`.
    :type suffix:         :class:`bytes`
    :param hash_function: The hash function to use (e.g. :class:`Crypto.Hash.SHA256.SHA256Hash`).
    :type hash_function:  All modern and history hash algorithms listed in :doc:`src/hash/hash`.
    :param input_source:  A generator that creates input values for the hash function. Defaults
                          to brute force starting at `0`.
    :type input_source:   :class:`generator`
    :param kwargs:        Additional keyword arguments that get passed to `hash_function.new`
                          (e.g. `digest_bytes` for :class:`Crypto.Hash.BLAKE2s`).
    :type kwargs:         :class:`dict`
    :returns:             The computed prefix, such that `hash_function.new(prefix + suffix).digest()`
                          fulfills `condition`.
    :rtype:               :class:`bytes`
    """

    def wrap_input_source():
        for i in input_source:
            yield i + suffix

    return compute(hash_function, condition, wrap_input_source(), **kwargs)


def compute_with_pattern(hash_function, pattern, input_source, **kwargs):
    """
    Compute a Proof of Work based on the given pattern.

    >>> # Compute a digest that starts and ends with a '1'
    >>> def input_source(init):
    ...     for bf in generate_brute_force(init):
    ...         yield bytes(bf)
    >>> guess = compute_with_pattern(SHA1, r'^1{h}1$', input_source([0]))
    >>> digest = SHA1.new(guess).hexdigest()
    >>> assert digest[0] == '1' and digest[-1] == '1'

    >>> # Compute a digest with '123' somewhere
    >>> guess = compute_with_pattern(SHA1, r'{h}123{h}', input_source([0]))
    >>> digest = SHA1.new(guess).hexdigest()
    >>> assert '123' in digest

    >>> # Compute a digest with '1', '2' and '3' separated by at least one
    >>> # value in-between
    >>> guess = compute_with_pattern(SHA1, r'{h}1{h}2{h}3{h}', input_source([0]))

    :param pattern:       The regex pattern that the resulting digest should conform to.
                          You can insert '{h}' wherever you want non fixed values, or '{h_}'
                          for an optional non fixed value (i.e. '{h_}' can result in '', '{h}'
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
    :param kwargs:        Additional keyword arguments that get passed to `hash_function.new`
                          (e.g. `digest_bytes` for :class:`Crypto.Hash.BLAKE2s`).
    :type kwargs:         :class:`dict`
    :returns:             A bytestring that produces a `hash_function` hexdigest of the form
                          specified by `pattern` when used as input for `hash_function.new`.
                          `suffix`.
    :rtype:               :class:`bytes`
    """
    block_size = getattr(hash_function, 'block_size', None)
    if block_size and len(pattern.replace('{h}', '').replace('{h_}', '')) >= block_size:
        raise Exception('Your pattern must be smaller than the block size of ' +
                        '{} (or you already know what your hash looks like)'.format(
                            hash_function))
    p = re.compile(pattern.format(h=r'\w+', h_=r'\w*'))
    match = lambda x: p.match(hex_str(x))
    return compute(hash_function, match, input_source, **kwargs)


def compute(hash_function, condition, input_source, **kwargs):
    """
    Compute a Proof of Work based on the given condition function and input source.

    >>> # Define a simple input source
    >>> def input_source(start):
    ...     for bf in generate_brute_force(start):
    ...         yield bytes(bf)
    >>> # Instantiate a generator
    >>> generator = input_source([0])
    >>> # Compute a digest with '123' somewhere
    >>> condition = lambda d: '123' in hex_str(d)
    >>> 
    >>> guess = compute(SHA1, condition, generator)
    >>> assert '123' in SHA1.new(data=guess).hexdigest()

    :param condition:     A function checking whether a given hexdigest fulfills the proof of
                          work condition.
    :type condition:      function(x: :class:`bytes`) -> :class:`bool`
    :param hash_function: The hash function to use (e.g. :class:`Crypto.Hash.SHA256.SHA256Hash`).
    :type hash_function:  All modern and history hash algorithms listed in :doc:`src/hash/hash`.
    :param input_source:  A generator that creates input values for the hash function.
    :type input_source:   :class:`generator` -> :class:`bytes`
    :param kwargs:        Additional keyword arguments that get passed to `hash_function.new`
                          (e.g. `digest_bytes` for :class:`Crypto.Hash.BLAKE2s`).
    :type kwargs:         :class:`dict`
    :returns:             A bytestring that produces a `hash_function` hexdigest of the form
                          specified by `condition` when used as input for `hash_function.new`.
    :rtype:               :class:`bytes`
    """

    def _compute_digest(data, **kwargs):
        return hash_function.new(data=data, **kwargs).digest()

    for guess in input_source:
        if condition(_compute_digest(guess, **kwargs)):
            return guess
