import psutil


def print_temps():
    if not hasattr(psutil, "sensors_temperatures"):
        print("Temperature sensors API not available on this platform")
        return

    temps = psutil.sensors_temperatures()

    if not temps:
        print("No temperature sensors detected")
        return

    for sensor_name, entries in temps.items():
        print(f"\n{sensor_name}:")
        for entry in entries:
            label = entry.label if entry.label else "N/A"
            print(f"  {label}: {entry.current} °C")


if __name__ == "__main__":
    print_temps()
