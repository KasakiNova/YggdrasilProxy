import logging
import sys
import threading

from colorama import Fore, Style
from paste.translogger import TransLogger
from waitress import serve

import modules.globalVariables as Var

from modules.publickeysGet import update_key_thread
from modules.configMgr import ConfigParsing
from modules.httpLogic import app
from modules.tools import print_system_info

# 配置文件处理实例化
config = ConfigParsing(Var.ConfigPath, Var.ConfigExtension)
# 输入参数的初始化
# 未实现输入参数
opt_configFileName = None

# 打印系统信息
print_system_info()

print(f"Service running in {Var.workDir}")

# 配置文件检查
if config.check_config():
    (configList, configName, Var.configData) = config.load_config(opt_configFileName)
    print(f"Find {len(set(configList))} Configuration File")
    print("The configuration file has been found. The file is", Fore.CYAN + configName + Style.RESET_ALL)
    if Var.debuglevel == 2:
        print("General:\n", Var.configData['General'], "\nServer:\n", Var.configData['Server'])
    print(Fore.GREEN + "[Config Loaded]" + Style.RESET_ALL)
else:
    sys.exit("The configuration file cannot be found in configs\nBye!")

thread = threading.Thread(target=update_key_thread)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    logger = logging.getLogger("waitress")
    logger.setLevel(logging.INFO)
    try:
        serve(TransLogger(app, setup_console_handler=False), host=Var.ip, port=Var.port, threads=4)
    except KeyboardInterrupt:
        print("\nStopped by user")
