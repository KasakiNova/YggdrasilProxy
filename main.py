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
    (configList, configName, Var.config_data) = config.load_config(opt_configFileName)
    print(f"Find {len(set(configList))} Configuration File")
    print("The configuration file has been found. The file is", Fore.CYAN + configName + Style.RESET_ALL)
    if Var.debuglevel == 2:
        print("General:\n", Var.config_data['General'], "\nServer:\n", Var.config_data['Server'])
    print(Fore.GREEN + "[Config Loaded]" + Style.RESET_ALL)
else:
    sys.exit("The configuration file cannot be found in configs\nBye!")

thread = threading.Thread(target=update_key_thread)
thread.daemon = True
thread.start()

config.read_server_config(0)


# 测试用
app.run(debug=True, host=Var.ip, port=Var.port)
logger = logging.getLogger("waitress")
logger.setLevel(logging.DEBUG)

#serve(TransLogger(app, setup_console_handler=True), host=Var.ip, port=Var.port, threads=4)
