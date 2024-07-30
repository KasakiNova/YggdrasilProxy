import os
import sys

from colorama import Fore, Style

from modules.configMgr import ConfigParsing
from modules.tools import print_system_info

# 全局变量初始化
workDir = os.getcwd()
ConfigPath = str(workDir + os.sep + "configs")
logs = bool()
debuglevel = int()
ip = str()
port = int()
# 修改默认读取的配置文件，下面是可选的配置文件
# toml json json5 yaml
ConfigExtension = "toml"
# 实例化
config = ConfigParsing(ConfigPath, ConfigExtension)
# 输入参数的初始化
# 未实现输入参数
opt_configFileName = None

# 打印系统信息
print_system_info()

print(f"Service running in {workDir}")

# 配置文件检查
if config.check():
    configList, configName, logs, debuglevel, ip, port = config.load_general_config(opt_configFileName)
    print(f"Find {len(set(configList))} Configuration File")
    print("The configuration file has been found. The file name is", Fore.CYAN + configName + Style.RESET_ALL)
else:
    sys.exit("The configuration file cannot be found in configs\nBye!")
