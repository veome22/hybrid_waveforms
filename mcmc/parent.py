#from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
import numpy as np
import time 
from concurrent.futures import ProcessPoolExecutor

def calc_squares(range_tuple):
        return range_tuple**2


if __name__ == '__main__':
    #comm = MPI.COMM_WORLD
    #size = comm.Get_size()
    #rank = comm.Get_rank()
    size = 5
    subranges = []

    for i in range(size):
        subranges.append(np.linspace(i*size, (i+1)*size, 10000000))
    
    start = time.time()

    executor = ProcessPoolExecutor()
    #for result in executor.map(calc_squares, subranges):
    #   print(sum)

    prime_sets = executor.map(calc_squares, subranges)
    executor.shutdown()
    
    end = time.time()

    print(f"completed in {end-start:.2f} s")
    
    summation = 0.0
    for result in prime_sets:
        summation += np.sum(result)
        
    print(summation)

    #primes = [p for plist in prime_sets for p in plist]
    #print((primes))
    #print(prime_sets[0].type)


