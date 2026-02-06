import time
import math
import psutil
from concurrent.futures import ProcessPoolExecutor
import GPUtil

class Benchmark:
    def __init__(self):
        self.cpu_cores = psutil.cpu_count(logical=True)
        self.gpu_list = GPUtil.getGPUs()
        self.selected_gpu = gpu_list[0]
        self.cpu_iter = 


    def select_gpu(self):
        print(f"select your gpu for benchmarks:", end=" ")
        for i, g in enumerate(self.gpu_list):
            print(f"Enter {i} for {g}")


    def set_cpu_iter(self):
