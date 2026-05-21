import platform
import socket
import subprocess


def get_os_pretty_name():
    with open("/etc/os-release") as f:
        for line in f:
            if line.startswith("PRETTY_NAME="):
                return line.strip().split("=")[1].replace('"', '')

    return "Unknown OS"


def get_system_info():
    hostname = socket.gethostname()
    os_info = get_os_pretty_name()
    kernel = platform.release()

    uptime = subprocess.check_output(
        "uptime -p",
        shell=True
    ).decode().strip()

    return {
        "hostname": hostname,
        "os_info": os_info,
        "kernel": kernel,
        "uptime": uptime
    }
