import psutil
import platform
import socket
import time
from datetime import datetime


def bytes_to_gb(b):
    return round(b / (1024 ** 3), 2)


def print_header(title):
    print(f"\n{'=' * 10} {title} {'=' * 10}")


# =========================
# BASIC SYSTEM INFO
# =========================
print_header("SYSTEM")
print("OS:", platform.system(), platform.release())
print("OS Version:", platform.version())
print("Architecture:", platform.machine())
print("Processor:", platform.processor())
print("Hostname:", socket.gethostname())
print("Boot Time:", datetime.fromtimestamp(psutil.boot_time()))

# =========================
# CPU INFO
# =========================
print_header("CPU")
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
print("Max Frequency:", psutil.cpu_freq().max, "MHz")
print("Min Frequency:", psutil.cpu_freq().min, "MHz")
print("Current Frequency:", psutil.cpu_freq().current, "MHz")

print("\nCPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")

print("Total CPU Usage:", psutil.cpu_percent(), "%")

# =========================
# MEMORY INFO
# =========================
print_header("MEMORY")
virtual_mem = psutil.virtual_memory()
swap_mem = psutil.swap_memory()

print("Total RAM:", bytes_to_gb(virtual_mem.total), "GB")
print("Available RAM:", bytes_to_gb(virtual_mem.available), "GB")
print("Used RAM:", bytes_to_gb(virtual_mem.used), "GB")
print("RAM Usage:", virtual_mem.percent, "%")

print("\nSwap Total:", bytes_to_gb(swap_mem.total), "GB")
print("Swap Used:", bytes_to_gb(swap_mem.used), "GB")
print("Swap Usage:", swap_mem.percent, "%")

# =========================
# DISK INFO
# =========================
print_header("DISKS")
for partition in psutil.disk_partitions():
    print(f"\nDevice: {partition.device}")
    print("Mountpoint:", partition.mountpoint)
    print("Filesystem:", partition.fstype)
    try:
        usage = psutil.disk_usage(partition.mountpoint)
        print("Total Size:", bytes_to_gb(usage.total), "GB")
        print("Used:", bytes_to_gb(usage.used), "GB")
        print("Free:", bytes_to_gb(usage.free), "GB")
        print("Usage:", usage.percent, "%")
    except PermissionError:
        print("Permission denied")

# =========================
# NETWORK INFO
# =========================
print_header("NETWORK")
net_io = psutil.net_io_counters()
print("Bytes Sent:", bytes_to_gb(net_io.bytes_sent), "GB")
print("Bytes Received:", bytes_to_gb(net_io.bytes_recv), "GB")

print("\nInterfaces:")
for iface, addrs in psutil.net_if_addrs().items():
    print(f"\n{iface}:")
    for addr in addrs:
        print(" ", addr.family, addr.address)

# =========================
# SENSORS (if supported)
# =========================
print_header("SENSORS")
if hasattr(psutil, "sensors_temperatures"):
    temps = psutil.sensors_temperatures()
    if temps:
        for name, entries in temps.items():
            print(f"\n{name}:")
            for entry in entries:
                print(f" {entry.label or 'N/A'}: {entry.current}°C")
    else:
        print("No temperature sensors available")
else:
    print("Sensors not supported on this platform")

# =========================
# PROCESSES INFO
# =========================
print_header("PROCESSES")
print("Total running processes:", len(psutil.pids()))

print("\nTop 5 processes by memory usage:")

processes = []

for p in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
    try:
        rss = p.info['memory_info'].rss
        processes.append({
            "pid": p.info['pid'],
            "name": p.info['name'],
            "rss": rss
        })
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

# Explicit key-based sort (safe)
processes.sort(key=lambda p: p["rss"], reverse=True)

for p in processes[:5]:
    print(f"PID {p['pid']} | {p['name']} | RAM {bytes_to_gb(p['rss'])} GB")


# =========================
# UPTIME
# =========================
print_header("UPTIME")
uptime_seconds = time.time() - psutil.boot_time()
print("System Uptime:", round(uptime_seconds / 3600, 2), "hours")
