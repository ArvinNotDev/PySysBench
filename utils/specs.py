import psutil
import platform
import socket
import time
from datetime import datetime


class Specs:

    # -------------------------
    # UTILS
    # -------------------------
    @staticmethod
    def bytes_to_gb(b):
        return round(b / (1024 ** 3), 2)

    # -------------------------
    # SYSTEM
    # -------------------------
    @classmethod
    def get_system_info(cls):
        return {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": socket.gethostname(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }

    # -------------------------
    # CPU
    # -------------------------
    @classmethod
    def get_cpu(cls):
        freq = psutil.cpu_freq()

        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "frequency_mhz": {
                "max": freq.max if freq else None,
                "min": freq.min if freq else None,
                "current": freq.current if freq else None,
            },
            "usage_per_core_percent": psutil.cpu_percent(percpu=True, interval=1),
            "total_usage_percent": psutil.cpu_percent()
        }

    # -------------------------
    # MEMORY
    # -------------------------
    @classmethod
    def get_memory(cls):
        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()

        return {
            "virtual": {
                "total_gb": cls.bytes_to_gb(vm.total),
                "available_gb": cls.bytes_to_gb(vm.available),
                "used_gb": cls.bytes_to_gb(vm.used),
                "usage_percent": vm.percent
            },
            "swap": {
                "total_gb": cls.bytes_to_gb(sm.total),
                "used_gb": cls.bytes_to_gb(sm.used),
                "usage_percent": sm.percent
            }
        }

    # -------------------------
    # DISKS
    # -------------------------
    @classmethod
    def get_disks(cls):
        disks = []

        for partition in psutil.disk_partitions():
            disk = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "filesystem": partition.fstype
            }

            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk["usage"] = {
                    "total_gb": cls.bytes_to_gb(usage.total),
                    "used_gb": cls.bytes_to_gb(usage.used),
                    "free_gb": cls.bytes_to_gb(usage.free),
                    "usage_percent": usage.percent
                }
            except PermissionError:
                disk["usage"] = None

            disks.append(disk)

        return disks

    # -------------------------
    # NETWORK
    # -------------------------
    @classmethod
    def get_network(cls):
        net_io = psutil.net_io_counters()

        interfaces = {}
        for iface, addrs in psutil.net_if_addrs().items():
            interfaces[iface] = [
                {
                    "family": str(addr.family),
                    "address": addr.address
                }
                for addr in addrs
            ]

        return {
            "io": {
                "bytes_sent_gb": cls.bytes_to_gb(net_io.bytes_sent),
                "bytes_received_gb": cls.bytes_to_gb(net_io.bytes_recv)
            },
            "interfaces": interfaces
        }

    # -------------------------
    # SENSORS
    # -------------------------
    @classmethod
    def get_sensors(cls):
        if not hasattr(psutil, "sensors_temperatures"):
            return None

        temps = psutil.sensors_temperatures()
        if not temps:
            return None

        sensors = {}
        for name, entries in temps.items():
            sensors[name] = [
                {
                    "label": entry.label or "N/A",
                    "current_c": entry.current
                }
                for entry in entries
            ]

        return sensors

    # -------------------------
    # PROCESSES
    # -------------------------
    @classmethod
    def get_processes(cls, top_n=5):
        processes = []

        for p in psutil.process_iter(attrs=["pid", "name", "memory_info"]):
            try:
                processes.append({
                    "pid": p.info["pid"],
                    "name": p.info["name"],
                    "rss_gb": cls.bytes_to_gb(p.info["memory_info"].rss)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(key=lambda p: p["rss_gb"], reverse=True)

        return {
            "total_processes": len(psutil.pids()),
            "top_by_memory": processes[:top_n]
        }

    # -------------------------
    # UPTIME
    # -------------------------
    @classmethod
    def get_uptime(cls):
        uptime_seconds = time.time() - psutil.boot_time()
        return {
            "uptime_seconds": int(uptime_seconds),
            "uptime_hours": round(uptime_seconds / 3600, 2)
        }

    # -------------------------
    # AGGREGATOR
    # -------------------------
    @classmethod
    def run_all(cls):
        return {
            "system": cls.get_system_info(),
            "cpu": cls.get_cpu(),
            "memory": cls.get_memory(),
            "disks": cls.get_disks(),
            "network": cls.get_network(),
            "sensors": cls.get_sensors(),
            "processes": cls.get_processes(),
            "uptime": cls.get_uptime()
        }
