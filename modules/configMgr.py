import sys
import tomllib
import os
import re
import socket
from colorama import Fore, Style


# 判断配置文件类型
class FindConfig:
    def __init__(self, import_path: str, import_extension: int):
        self.configDir = import_path
        self.configDirList = None
        self.configFile = list()
        self.configFileList = set()
        self.setExtension = import_extension
        self.endswith = ('toml', 'json', 'json5')
        # 检查文件夹是否存在,不存在则创建
        if not os.path.exists(self.configDir):
            os.mkdir(self.configDir)

    def check(self) -> bool:
        # 检查文件夹内是否存在配置文件
        if len(os.listdir(self.configDir)) == 0:
            return False
        else:
            self.configDirList = os.listdir(self.configDir)
            pass

        # 检查文件扩展名
        for filename in self.configDirList:
            if filename.endswith(self.endswith):
                self.configFileList.add(filename)
        if len(self.configFileList) == 0:
            return False
        return True

    def name(self):
        # 指定配置文件优先级
        ext = ""
        if self.setExtension == 1:
            ext = ".toml"
        elif self.setExtension == 2:
            ext = ".json"
        elif self.setExtension == 3:
            ext = ".json5"
        # 多配置文件选择，未实现
        self.configFile.append([i for i in self.configFileList if re.search(ext, i)])
        def_output = "".join(self.configFile[0])
        return self.configFileList, def_output, self.endswith[self.setExtension - 1]


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


# 配置文件解析
class ConfigParsing:
    # toml配置文件读取
    def general_read_toml(self: str):
        # 加载配置文件
        with open(str(self), mode="r+b") as file:
            config_data = tomllib.load(file)
        # 输出配置并检查
        print(config_data)
        config_check(config_data)
        # 解析配置
        def_logs: bool = config_data["General"]["logs"]
        def_debuglevel: int = config_data["General"]["debuglevel"]
        def_ip: str = config_data["General"]["ip"]
        def_port: int = config_data["General"]["port"]

        print(Fore.GREEN + "[Config Loaded]" + Style.RESET_ALL)
        return def_logs, def_debuglevel, def_ip, def_port
