import platform
import sys


# 打印系统配置信息函数
def print_system_info() -> None:
    print()
    win32 = None
    if platform.system() == 'Windows':
        win32 = platform.win32_edition()

    print(platform.system(), platform.version(), win32, platform.platform(), platform.machine(),
          platform.architecture(), "\n", platform.processor())
    print("Python Version", sys.version, "\n", sys.version_info)
    print()
    pass
