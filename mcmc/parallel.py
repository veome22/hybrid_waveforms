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


def integrate_one(indices):
    """A somewhat CPU-intensive task."""
    print(f"evaluating {indices[0]} to {indices[1]}")
    result = 0.0

    for i in range(indices[0], indices[1]):
        for j in range(indices[0], indices[1]):
            result = result + j**2    

    return result


@timeit
def compute_integral(n):
    """Function that integrates."""
    
    # determine how many events will be handled by each processor
    size = n // N_workers
    remainder = n % N_workers

    # split N_events into separate ranges for each processor
    indices = []
    for i in range(N_workers):
        indices.append([i*size, (i+1)*size])

    # add the remaining events to the last processpr
    indices[-1][1] = indices[-1][1]+remainder
    
    result_tot = 0.0
    with ProcessPoolExecutor(max_workers=N_workers) as executor:
        for res in executor.map(integrate_one, indices):
            result_tot = result_tot + res

    return result_tot


if __name__ == "__main__":
    print(compute_integral(1000))

