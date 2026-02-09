import subprocess
import os
import re

def ping_address_vulnerable(address):
    command = f"ping -c 1 {address}"
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    except Exception as e:
        return str(e)


def ping_address_safe(address):
    if not re.match(r"^[a-zA-Z0-9.\-]+$", address):
        return "Invalid input format"
    command = ["ping", "-c", "1", address]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    except Exception as e:
        return str(e)
