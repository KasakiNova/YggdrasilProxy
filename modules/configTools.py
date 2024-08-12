import json
import os
import re
import socket
import sys
import tomllib

import json5
import requests.exceptions
import yaml
from colorama import Fore, Style

import modules.globalVariables as Var


class ConfigTools:
    # 选择扩展名
    def select_extension(self: str, import_list: set):
        # 判断并获取默认配置文件的后缀与文件名
        if self == 'toml':
            default_config_file = [file for file in import_list if file.endswith('.toml')]
        elif self == 'json':
            default_config_file = [file for file in import_list if file.endswith('.json')]
        elif self == 'json5':
            default_config_file = [file for file in import_list if file.endswith('.json5')]
        elif self == 'yaml':
            default_config_file = [file for file in import_list if file.endswith('.yaml')]
        else:
            # 这个检查是绝对的小丑
            default_config_file = None
            print(default_config_file)
            sys.exit(Fore.RED + "[Wrong choice of default suffix parameter]" + Style.RESET_ALL)
        return default_config_file

    # 配置文件内容检查
    def config_check(self: dict) -> None:
        # General块检查
        def general():
            # 类型检查
            if not isinstance(self["General"]["enable"], bool):
                sys.exit(Fore.RED + "enable is the wrong variable type" + Style.RESET_ALL)
            if not isinstance(self["General"]["logs"], bool):
                sys.exit(Fore.RED + "logs is the wrong variable type" + Style.RESET_ALL)
            if not isinstance(self["General"]["debuglevel"], int):
                sys.exit(Fore.RED + "debuglevel is the wrong variable type" + Style.RESET_ALL)
            if not isinstance(self["General"]["ip"], str):
                sys.exit(Fore.RED + "ip is the wrong variable type" + Style.RESET_ALL)
            if not isinstance(self["General"]["port"], int):
                sys.exit(Fore.RED + "enable is the wrong variable type" + Style.RESET_ALL)
            # 判断配置文件是否启用
            if not self["General"]["enable"]:
                sys.exit(Fore.RED + "[CONFIG NOT ENABLE]" + Style.RESET_ALL)
            # 检查IP地址格式是否正确
            try:
                socket.inet_aton(self["General"]["ip"])
                pass
            except socket.error:
                sys.exit(Fore.RED + "[The IP address is incorrect]" + Style.RESET_ALL)
            # 检查debuglevel值是否在范围内
            debuglevel_value = (1, 2)
            if not self["General"]["debuglevel"] in debuglevel_value:
                sys.exit(Fore.RED + "debuglevel value is incorrect" + Style.RESET_ALL)
            # 检查端口是否在正确范围内
            if not 1 <= self["General"]["port"] <= 65535:
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
            for i in range(len(self["Server"])):
                # 检查变量格式
                if not isinstance(self["Server"][str(i)]["Name"], str):
                    sys.exit(Fore.RED + f"Name is the wrong variable type in Server.{i}" + Style.RESET_ALL)
                if not isinstance(self["Server"][str(i)]["Url"], str):
                    sys.exit(Fore.RED + f"Url is the wrong variable type in Server.{i}" + Style.RESET_ALL)
                # 执行网址检查
                if check_ip(self["Server"][str(i)]["Url"]):
                    pass
                elif check_url(self["Server"][str(i)]["Url"]):
                    pass
                else:
                    sys.exit(Fore.RED + f"The Server.{i} URL is incorrect" + Style.RESET_ALL)
            pass

        general()
        server()
        pass

    # 打开配置文件
    def open_config(self: str) -> dict:
        _, ext = os.path.splitext(self)
        # 打开toml格式配置文件
        if ext.lower() == '.toml':
            with open(self, mode='rb') as fff:
                config_details = tomllib.load(fff)
                ConfigTools.config_check(config_details)
                return config_details
        # 打开json格式配置文件
        elif ext.lower() == '.json':
            with open(self, mode='rb') as fff:
                config_details = json.load(fff)
                ConfigTools.config_check(config_details)
                return config_details
        # 打开json5格式配置文件
        elif ext.lower() == '.json5':
            with open(self, mode='rb') as fff:
                config_details = json5.load(fff)
                ConfigTools.config_check(config_details)
                return config_details
        # 打开yaml格式配置文件
        elif ext.lower() == '.yaml':
            with (open(self, mode='rb') as fff):
                config_details = yaml.load(fff, Loader=yaml.FullLoader)
                ConfigTools.config_check(config_details)
                return config_details
        # 全都打不开执行这行退出程序，在这还整个退出搞得上面的检查是个小丑似的
        else:
            sys.exit(Fore.RED + "[Unsupported configuration file format]" + Style.RESET_ALL)
        pass


# 检查服务器是mojang官方还是第三方
def official_judgment(url):
    mojang_url = "sessionserver.mojang.com"
    blessing_url = "/api/yggdrasil"
    # 判断服务器类型
    if mojang_url in url:
        server_type = "official"
    elif blessing_url in url:
        server_type = "blessing"
    else:
        server_type = "shit"
    return server_type


# 载入配置到全局
def load_config_to_var(config_data):
    # 加载代理配置
    def read_proxy_config():
        Var.proxyEnable = config_data["Proxy"]["enable"]
        Var.proxyLink = config_data["Proxy"]["address"]
        Var.proxyAuthEnable = config_data["Proxy"]["enable_auth"]
        if Var.proxyAuthEnable:
            Var.proxyUsername = config_data["Proxy"]["username"]
            Var.proxyPassword = config_data["Proxy"]["password"]

    # 载入基本配置
    Var.logs = config_data["General"]["logs"]
    Var.debuglevel = config_data["General"]["debuglevel"]
    Var.ip = config_data["General"]["ip"]
    Var.port = config_data["General"]["port"]
    Var.updatePublickeysTime = config_data["General"]["UpdatePublickeysTime"]
    Var.proxyEnable = config_data["Proxy"]["enable"]
    if Var.proxyEnable:
        read_proxy_config()


# 检查Proxy是否能够访问
def check_proxy():
    from modules.tools import proxies_link
    from modules.customError import ProxyError
    from requests import get
    try:
        proxies = proxies_link()
        response = get(url="https://api.myip.la", proxies=proxies)
        if response.status_code == 200:
            return True
        else:
            raise ProxyError
    except requests.exceptions.ProxyError:
        return False
    except ProxyError:
        return False
