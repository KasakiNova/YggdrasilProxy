# coding=utf-8
import platform
import sys

YELLOW = "\033[33m"
RESET = "\033[0m"

def sysinfo():
    system_name = platform.system()
    print(f"{YELLOW}System:{RESET}", platform.system())
    print(f"{YELLOW}Version:{RESET}", platform.version())
    print(f"{YELLOW}Platform:{RESET}", platform.platform())
    print(f"{YELLOW}Machine:{RESET}", platform.machine())
    print(f"{YELLOW}Architecture:{RESET}", platform.architecture())
    print(f"{YELLOW}Processor:{RESET}", platform.processor())
    if system_name == "Windows":
        try:
            print(f"{YELLOW}Windows Edition:{RESET}", platform.win32_edition())
        except AttributeError:
            pass
            # print(f"{YELLOW}Windows Edition:{RESET} Not available")
    elif system_name in ["Linux", "Darwin"]:
        print(f"{YELLOW}Uname:{RESET}", platform.uname())

    print(f"{YELLOW}Python Version:{RESET}", sys.version)
