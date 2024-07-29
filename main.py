from modules.configMgr import FindConfig, ConfigParsing
import sys
import os
from colorama import Fore, Style

print("\n")

workDir = os.getcwd()
defConfigPath = str(workDir + os.sep + "configs")
# 1=.toml 2=.json 3=.json5
# 未实现配置文件切换，当前之支持toml格式
setExtension = 1
# 实例化
find = FindConfig(defConfigPath, setExtension)

print(f"Service running in {workDir}")

# 配置文件检查
if find.check():
    configList, configName, configType = find.name()
    print(f"Find {len(set(configList))} Configuration File")
    print("The configuration file has been found. The file name is", Fore.CYAN + configName + Style.RESET_ALL)
else:
    print("The configuration file cannot be found in configs\nBye!")
    sys.exit()
print(configType)
print(defConfigPath + os.sep + configName)
logs, debuglevel, ip, port = ConfigParsing.general_read_toml(defConfigPath + os.sep + configName)
