import platform
import re
import socket
import sys

from colorama import Fore, Style


# 打印系统配置信息函数
def print_system_info() -> None:
    print()
    win32 = None
    if platform.system() == 'Windows':
        win32 = platform.win32_edition()
        pass

    print(platform.system(), platform.version(), win32, platform.platform(), platform.machine(),
          platform.architecture(), "\n", platform.processor())
    print("Python Version", sys.version, "\n", sys.version_info)
    print()
    pass


# 配置文件检查函数
def config_check(import_config: dict) -> None:
    # General块检查
    def general():
        # 类型检查
        if not isinstance(import_config["General"]["enable"], bool):
            sys.exit(Fore.RED + "enable is the wrong variable type" + Style.RESET_ALL)
        if not isinstance(import_config["General"]["logs"], bool):
            sys.exit(Fore.RED + "logs is the wrong variable type" + Style.RESET_ALL)
        if not isinstance(import_config["General"]["debuglevel"], int):
            sys.exit(Fore.RED + "debuglevel is the wrong variable type" + Style.RESET_ALL)
        if not isinstance(import_config["General"]["ip"], str):
            sys.exit(Fore.RED + "ip is the wrong variable type" + Style.RESET_ALL)
        if not isinstance(import_config["General"]["port"], int):
            sys.exit(Fore.RED + "enable is the wrong variable type" + Style.RESET_ALL)
        # 判断配置文件是否启用
        if not import_config["General"]["enable"]:
            sys.exit(Fore.RED + "[CONFIG NOT ENABLE]" + Style.RESET_ALL)
        # 检查IP地址格式是否正确
        try:
            socket.inet_aton(import_config["General"]["ip"])
            pass
        except socket.error:
            sys.exit(Fore.RED + "[The IP address is incorrect]" + Style.RESET_ALL)
        # 检查debuglevel值是否在范围内
        debuglevel_value = (1, 2)
        if not import_config["General"]["debuglevel"] in debuglevel_value:
            sys.exit(Fore.RED + "debuglevel value is incorrect" + Style.RESET_ALL)
        # 检查端口是否在正确范围内
        if not 1 <= import_config["General"]["port"] <= 65535:
            sys.exit(Fore.RED + "port value is incorrect" + Style.RESET_ALL)
        pass

    # 检查Server块
    def server():
        # 检查IP URL格式
        def check_ip(ip):
            try:
                socket.inet_aton(ip)
                return True
            except socket.error:
                return False

        # 检查普通URL格式
        def check_url(url):
            url_pattern = re.compile(r'^(http|https)://[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+')
            if url_pattern.match(url):
                return True
            else:
                return False

        # 使用for循环检查多个服务器链接和格式
        for i in range(len(import_config["Server"])):
            # 检查变量格式
            if not isinstance(import_config["Server"][str(i)]["Name"], str):
                sys.exit(Fore.RED + f"Name is the wrong variable type in Server.{i}" + Style.RESET_ALL)
            if not isinstance(import_config["Server"][str(i)]["Url"], str):
                sys.exit(Fore.RED + f"Url is the wrong variable type in Server.{i}" + Style.RESET_ALL)
            # 执行网址检查
            if check_ip(import_config["Server"][str(i)]["Url"]):
                pass
            elif check_url(import_config["Server"][str(i)]["Url"]):
                pass
            else:
                sys.exit(Fore.RED + f"The Server.{i} URL is incorrect" + Style.RESET_ALL)
        pass

    general()
    server()
    pass
