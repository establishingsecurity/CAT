import datetime
from multiprocessing import Pool, TimeoutError
from multiprocessing.pool import ApplyResult, AsyncResult

import gmpy2

from cat.factorize.fermat import factor

if __name__ == "__main__":

    gmpy2.get_context().precision = 2048

    N = (
        123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123451234512345123
        + 100
    )
    M = N + 200

    print("Will work for length {}".format(len(bin(N)) - 2))

    processes, timeout = 4, 10

    with Pool(processes=processes) as pool:

        for n in range(N, M, 2 * processes):

            workers = []

            fst_time = datetime.datetime.now()

            for m in range(n, min(M, n + 2 * processes), 2):

                workers.append((pool.apply_async(factor, (gmpy2.mpz(m),)), m))

            for worker, number in workers:
                try:
                    result = worker.get(timeout=timeout)

                    print("Worked for {} with factor {}".format(number, result))
                except TimeoutError:
                    pass
                    # print('Timed out for {}'.format(number))

            lst_time = datetime.datetime.now()

            print("chunk done in {}".format(lst_time - fst_time))
