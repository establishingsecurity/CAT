"""Methods for computing Proof of Works."""
import os

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


def compute(hash_function, condition, input_source, **kwargs):
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
