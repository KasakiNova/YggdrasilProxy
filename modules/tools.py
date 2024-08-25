import platform
import re
import sys
import socket

import modules.globalVariables as Var


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


# 生成代理链接
def proxies_link() -> dict:
    # 判断是否使用账户验证
    if Var.proxyAuthEnable:
        protocol = Var.proxyLink.split("://")[0]
        link = Var.proxyLink.split("://")[1]
        local_proxies = {
            "http": f"{protocol}://{Var.proxyUsername}:{Var.proxyPassword}@{link}",
            "https": f"{protocol}://{Var.proxyUsername}:{Var.proxyPassword}@{link}"
        }
    else:
        local_proxies = {
            "http": f"{Var.proxyLink}",
            "https": f"{Var.proxyLink}"
        }

    # 检测协议
    if "https" in Var.proxyLink[0:5]:
        return local_proxies
    elif "http" in Var.proxyLink[0:4]:
        return local_proxies


class CheckLink:
    # IP检查器
    def check_ip(self: str):
        try:
            socket.inet_aton(self)
            return True
        except socket.error:
            return False

    # 检查普通URL格式
    def check_url(self: str):
        url_pattern = re.compile(r'^(http|https)://[a-zA-Z0-9-._~:/?#[\]@!$&\'()*+,;=]+')
        if url_pattern.match(self):
            return True
        else:
            return False
