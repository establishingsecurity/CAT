"""Methods for computing Proof of Works."""
import os
import re
import Cryptodome

from Cryptodome import Hash
from multiprocessing import Process, Queue

from cat.utils.utils import generate_brute_force


def _guess(compute, condition, guesses, correct_guesses, **kwargs):
    while correct_guesses.empty():
        try:
            guess = guesses.get(timeout=1)
            if condition(compute(guess, **kwargs)):
                correct_guesses.put(guess)
                return
        except Queue.Empty:
            pass


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
    >>> condition = lambda g: g.hex().endswith('123')
    >>> prefix = b'Hello, world!'
    >>> pow_ = compute_suffix(Cryptodome.Hash.SHA1, prefix, condition, generator)
    >>> print(pow_.hex())
    48656c6c6f2c20776f726c642109f2
    >>> print(pow_[:13])
    b'Hello, world!'
    >>> print(Cryptodome.Hash.SHA1.new(data=pow_).hexdigest())
    af480840fd76a7371ac29988b4b62eba1516f123

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
    >>> condition = lambda g: g.hex().startswith('123')
    >>> suffix = b'Goodbye, world!'
    >>> pow_ = compute_prefix(Cryptodome.Hash.SHA1, suffix, condition, generator)
    >>> print(pow_.hex())
    0792476f6f646279652c20776f726c6421
    >>> print(pow_[-15:])
    b'Goodbye, world!'
    >>> print(Cryptodome.Hash.SHA1.new(data=pow_).hexdigest())
    12319f09d5cbd7bf26840c9c93842ea180474da4

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
    >>> pow_ = compute_with_pattern(Cryptodome.Hash.SHA1, r'^1{h}1$', input_source([0]))
    >>> print(bytes(pow_).hex())
    0d
    >>> print(Cryptodome.Hash.SHA1.new(data=bytes(pow_)).hexdigest())
    11f4de6b8b45cf8051b1d17fa4cde9ad935cea41

    >>> # Compute a digest with '123' somewhere
    >>> pow_ = compute_with_pattern(Cryptodome.Hash.SHA1, r'{h}123{h}', input_source([0]))
    >>> print(bytes(pow_).hex())
    0178
    >>> print(Cryptodome.Hash.SHA1.new(data=bytes(pow_)).hexdigest())
    754da6b34a4b1c42f5aa7ef08123ca5b5ac72f03

    >>> # Compute a digest with '1', '2' and '3' separated by at least one
    >>> # value in-between
    >>> pow_ = compute_with_pattern(Cryptodome.Hash.SHA1, r'{h}1{h}2{h}3{h}', input_source([0]))
    >>> print(bytes(pow_).hex())
    00
    >>> print(Cryptodome.Hash.SHA1.new(data=bytes(pow_)).hexdigest())
    5ba93c9db0cff93f52b521d7420e43f6eda2784f

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
    match = lambda x: p.match(x.hex())
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
    >>> condition = lambda d: '123' in d.hex()
    >>> pow_ = compute(Cryptodome.Hash.SHA1, condition, generator)
    >>> print(pow_.hex())
    0178
    >>> print(Cryptodome.Hash.SHA1.new(data=pow_).hexdigest())
    754da6b34a4b1c42f5aa7ef08123ca5b5ac72f03

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

    correct_guesses = Queue()
    guesses = Queue(maxsize=500)
    procs = []
    cpus = os.cpu_count()

    for i in range(0, cpus):
        args = (_compute_digest, condition, guesses, correct_guesses)
        proc = Process(target=_guess, args=args, kwargs=kwargs)
        procs.append(proc)
        proc.start()

    while correct_guesses.empty():
        guesses.put(next(input_source), timeout=5)

    correct_guess = correct_guesses.get()

    for proc in procs:
        proc.join()

    guesses.close()
    guesses.join_thread()
    correct_guesses.close()
    correct_guesses.join_thread()

    return correct_guess
