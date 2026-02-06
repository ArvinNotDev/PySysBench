import configparser
from pathlib import Path


class SettingsManager:
    def __init__(self, path="config/settings.conf"):
        self.path = Path(path)
        self.config = configparser.ConfigParser()

        # create default config
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.config["benchmark"] = {
                "cpu_iterations": "10000000",
                "gpu_iterations": "10000000",
                "polling_interval_sec": "1"
            }
            self.config["cpu"] = {
                "monitor_usage": "true"
            }
            self.config["gpu"] = {
                "enable": "true",
                "vendor": "auto"  # auto / NVIDIA / AMD / None
            }
            self.config["output"] = {
                "json_path": "results.json",
                "log_to_file": "false"
            }
            self.save()
        self.config.read(self.path)

    # -------- benchmark --------
    def get_cpu_iterations(self):
        return self.config.getint("benchmark", "cpu_iterations", fallback=10_000_000)

    def set_cpu_iterations(self, n: int):
        if not self.config.has_section("benchmark"):
            self.config.add_section("benchmark")
        self.config.set("benchmark", "cpu_iterations", str(int(n)))

    def get_gpu_iterations(self):
        return self.config.getint("benchmark", "gpu_iterations", fallback=10_000_000)

    def set_gpu_iterations(self, n: int):
        if not self.config.has_section("benchmark"):
            self.config.add_section("benchmark")
        self.config.set("benchmark", "gpu_iterations", str(int(n)))

    def get_polling_interval(self):
        return self.config.getfloat("benchmark", "polling_interval_sec", fallback=1.0)

    def set_polling_interval(self, seconds: float):
        if not self.config.has_section("benchmark"):
            self.config.add_section("benchmark")
        self.config.set("benchmark", "polling_interval_sec", f"{float(seconds):.2f}")

    # -------- cpu --------
    def get_cpu_monitor_usage(self):
        return self.config.getboolean("cpu", "monitor_usage", fallback=True)

    def set_cpu_monitor_usage(self, enabled: bool):
        if not self.config.has_section("cpu"):
            self.config.add_section("cpu")
        self.config.set("cpu", "monitor_usage", "true" if enabled else "false")

    # -------- gpu --------
    def get_gpu_enable(self):
        return self.config.getboolean("gpu", "enable", fallback=True)

    def set_gpu_enable(self, enabled: bool):
        if not self.config.has_section("gpu"):
            self.config.add_section("gpu")
        self.config.set("gpu", "enable", "true" if enabled else "false")

    def get_gpu_vendor(self):
        return self.config.get("gpu", "vendor", fallback="auto")

    def set_gpu_vendor(self, vendor: str):
        if not self.config.has_section("gpu"):
            self.config.add_section("gpu")
        self.config.set("gpu", "vendor", str(vendor))

    # -------- output --------
    def get_json_path(self):
        return self.config.get("output", "json_path", fallback="results.json")

    def set_json_path(self, path: str):
        if not self.config.has_section("output"):
            self.config.add_section("output")
        self.config.set("output", "json_path", str(path))

    def get_log_to_file(self):
        return self.config.getboolean("output", "log_to_file", fallback=False)

    def set_log_to_file(self, enabled: bool):
        if not self.config.has_section("output"):
            self.config.add_section("output")
        self.config.set("output", "log_to_file", "true" if enabled else "false")

    # -------- save/load --------
    def save(self):
        """Save current settings to the config file"""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            self.config.write(f)
