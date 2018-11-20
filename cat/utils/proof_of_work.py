"""Methods for computing Proof of Works."""
import os
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
    def wrap_input_source():
        for i in input_source:
            yield prefix + i
    return compute(hash_function, condition, wrap_input_source(), **kwargs)


def compute_prefix(hash_function, suffix, condition, input_source, **kwargs):
    def wrap_input_source():
        for i in input_source:
            yield i + suffix
    return compute(hash_function, condition, wrap_input_source(), **kwargs)


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
