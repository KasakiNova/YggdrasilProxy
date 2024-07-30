import json
import os
import sys

import json5
import yaml
from colorama import Fore, Style

from modules.tools import config_check

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


# 判断配置文件类型
class ConfigParsing:
    def __init__(self, import_path: str, import_config_extension: str):
        self.configDir = import_path
        self.configFile = str()
        self.configFileList = set()
        self.selectExtension = import_config_extension
        self.endswith = ('toml', 'json', 'json5', 'yaml')
        # 检查文件夹是否存在,不存在则创建
        if not os.path.exists(self.configDir):
            os.mkdir(self.configDir)

    def check(self) -> bool:
        # 检查文件夹内是否存在配置文件
        if len(os.listdir(self.configDir)) == 0:
            return False
        else:
            config_list = set(os.listdir(self.configDir))
            pass

        # 检查文件扩展名
        for filename in config_list:
            if filename.endswith(self.endswith):
                config_list.add(filename)
        if len(config_list) == 0:
            return False
        # 对配置文件列表进行排序
        # 0为toml，1为json，2为json5，3为yaml
        suffix_order = {'.toml': 0, '.json': 1, 'json5': 2, 'yaml': 3}

        def reordering(file):
            _, ext = file.split('.')
            return suffix_order.get('.' + ext, float('inf'))

        self.configFileList = sorted(config_list, key=reordering)
        return True

    # 加载配置文件
    def load_general_config(self, import_config_file):
        # 打开配置文件函数
        def open_config(file_name) -> dict:
            _, ext = os.path.splitext(file_name)
            # 打开toml格式配置文件
            if ext.lower() == '.toml':
                with open(file_name, mode='rb') as fff:
                    config_details = tomllib.load(fff)
                    print(config_details)
                    return config_details
            # 打开json格式配置文件
            elif ext.lower() == '.json':
                with open(file_name, mode='rb') as fff:
                    config_details = json.load(fff)
                    config_check(config_details)
                    return config_details
            # 打开json5格式配置文件
            elif ext.lower() == '.json5':
                with open(file_name, mode='rb') as fff:
                    config_details = json5.load(fff)
                    config_check(config_details)
                    return config_details
            # 打开yaml格式配置文件
            elif ext.lower() == '.yaml':
                with (open(file_name, mode='rb') as fff):
                    config_details = yaml.load(fff, Loader=yaml.FullLoader)
                    config_check(config_details)
                    return config_details
            # 全都打不开执行这行退出程序，在这还整个退出搞得上面的检查是个小丑似的
            else:
                sys.exit(Fore.RED + "[Unsupported configuration file format]" + Style.RESET_ALL)
            pass

        # 判断并获取默认配置文件的后缀与文件名
        if self.selectExtension == 'toml':
            default_config_file = [file for file in self.configFileList if file.endswith('.toml')]
        elif self.selectExtension == 'json':
            default_config_file = [file for file in self.configFileList if file.endswith('.json')]
        elif self.selectExtension == 'json5':
            default_config_file = [file for file in self.configFileList if file.endswith('.json5')]
        elif self.selectExtension == 'yaml':
            default_config_file = [file for file in self.configFileList if file.endswith('.yaml')]
        else:
            sys.exit(Fore.RED + "[Wrong choice of default suffix parameter]" + Style.RESET_ALL)

        # 检查输入参数是否为空，空则将默认配置文件覆盖进来
        if import_config_file is None:
            self.configFile = self.configDir + os.sep + default_config_file[0]
            print(self.configFile)
        else:
            self.configFile = import_config_file
            print(self.configFile)

        # 初始化临时保存配置变量
        def_logs = bool()
        def_debuglevel = int()
        def_ip = str()
        def_port = int()

        # 尝试打开配置文件
        try:
            config_data = open_config(self.configFile)
            def_logs: bool = config_data["General"]["logs"]
            def_debuglevel: int = config_data["General"]["debuglevel"]
            def_ip: str = config_data["General"]["ip"]
            def_port: int = config_data["General"]["port"]
            print(Fore.GREEN + "[Config Loaded]" + Style.RESET_ALL)
        # 无法打开则切换配置文件进行打开
        except FileNotFoundError:
            print(f"Can not open {self.configFile},try next")
            self.configFileList.remove(default_config_file)
            for alt_file_name in self.configFileList:
                try:
                    config_data = open_config(self.configDir + os.sep + alt_file_name)
                    def_logs: bool = config_data["General"]["logs"]
                    def_debuglevel: int = config_data["General"]["debuglevel"]
                    def_ip: str = config_data["General"]["ip"]
                    def_port: int = config_data["General"]["port"]
                    print(Fore.GREEN + "[Config Loaded]" + Style.RESET_ALL)
                    self.configFile = self.configDir + os.sep + alt_file_name
                    break
                # 这更是个小丑
                except FileNotFoundError:
                    print(f"Can not open {alt_file_name},try next")
        return self.configFileList, self.configFile, def_logs, def_debuglevel, def_ip, def_port
