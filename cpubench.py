import time
import math
import psutil
from concurrent.futures import ProcessPoolExecutor

def cpu_task(n):
    """CPU-intensive task: sum of square roots"""
    total = 0
    for i in range(1, n):
        total += math.sqrt(i)
    return total

def benchmark_cpu(n_iter=10_000_000):
    cores = psutil.cpu_count(logical=True)
    print(f"Detected {cores} logical cores. Starting CPU benchmark...\n")

    start_time = time.time()

    # Launch one process per logical core
    with ProcessPoolExecutor(max_workers=cores) as executor:
        futures = [executor.submit(cpu_task, n_iter) for _ in range(cores)]
        # wait for all
        results = [f.result() for f in futures]

    total_time = time.time() - start_time
    print(f"Benchmark completed in {total_time:.2f} seconds")
    print(f"Average time per core: {total_time / cores:.2f} seconds")

    # Optional: show CPU usage during benchmark
    print("\nCPU Usage per core during benchmark (percent):")
    usage = psutil.cpu_percent(percpu=True, interval=1)
    for i, u in enumerate(usage):
        print(f"Core {i}: {u}%")

if __name__ == "__main__":
    benchmark_cpu()
