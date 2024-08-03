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
port = int()
ip = str()
prefix = str()

# 修改默认读取的配置文件，下面是可选的配置文件
# toml json json5 yaml
ConfigExtension = "toml"
# 配置文件处理实例化
config = ConfigParsing(ConfigPath, ConfigExtension)
# 输入参数的初始化
# 未实现输入参数
opt_configFileName = None

# 打印系统信息
print_system_info()

print(f"Service running in {workDir}")

# 配置文件检查
if config.check_config():
    configList, configName, config_data, logs, debuglevel, ip, port, prefix = config.load_config(opt_configFileName)
    print(f"Find {len(set(configList))} Configuration File")
    print("The configuration file has been found. The file name is", Fore.CYAN + configName + Style.RESET_ALL)
    if debuglevel == 2:
        print("General:\n", config_data['General'], "\nServer:\n", config_data['Server'])
        config.read_server_config(1)
    print(Fore.GREEN + "[Config Loaded]" + Style.RESET_ALL)
else:
    sys.exit("The configuration file cannot be found in configs\nBye!")

from modules.httpLogic import app

app.run(debug=True, port=5000, host='0.0.0.0')

