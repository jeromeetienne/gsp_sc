import numpy as np
import time

# Generate 1 million random numbers between 0 and 1
numbers = np.random.rand(1_000_000)

# Measure sorting time
start = time.perf_counter()
sorted_numbers = np.sort(numbers)
end = time.perf_counter()

print(f"Sorted 1,000,000 numbers in {end - start:.6f} seconds")
