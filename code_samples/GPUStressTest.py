import torch
import time

def gpu_stress(matrix_size=4096, iterations=100):
    if not torch.cuda.is_available():
        print("No GPU detected or CUDA not available")
        return

    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name(device)}")

    # Create random matrices on GPU
    a = torch.randn((matrix_size, matrix_size), device=device)
    b = torch.randn((matrix_size, matrix_size), device=device)

    torch.cuda.synchronize()
    start_time = time.time()

    print(f"Starting GPU stress: {iterations} matrix multiplications of size {matrix_size}x{matrix_size}")

    for i in range(iterations):
        c = torch.matmul(a, b)
        if i % 10 == 0:
            print(f"Iteration {i+1}/{iterations} done")
    
    torch.cuda.synchronize()
    elapsed = time.time() - start_time
    print(f"GPU stress completed in {elapsed:.2f} seconds")

if __name__ == "__main__":
    gpu_stress()
