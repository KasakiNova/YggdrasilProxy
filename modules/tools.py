import platform
import sys
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
        local_proxies = {
            "http": f"{Var.proxyUsername}:{Var.proxyPassword}@{Var.proxyLink}",
            "https": f"{Var.proxyUsername}:{Var.proxyPassword}@{Var.proxyLink}"
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
