import hashlib
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import time
from functools import wraps
import argparse



parser = argparse.ArgumentParser(description='Parallel workers test.')
parser.add_argument('--N_workers', default="3", type=int,  help='number of workers (default: 3)')
args = vars(parser.parse_args())

N_workers = args["N_workers"]


def timeit(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        print(f"{method.__name__} => {(end_time-start_time)*1000} ms")

        return result

    return wrapper


def hash_one(n):
    """A somewhat CPU-intensive task."""

    for i in range(1, n):
        hashlib.pbkdf2_hmac("sha256", b"password", b"salt", i * 10000)

    return "done"


@timeit
def hash_all(n):
    """Function that does hashing in serial."""

    with ProcessPoolExecutor(max_workers=N_workers) as executor:
        for arg, res in zip(range(n), executor.map(hash_one, range(n), chunksize=2)):
            pass

    return "done"


if __name__ == "__main__":
    hash_all(20)

