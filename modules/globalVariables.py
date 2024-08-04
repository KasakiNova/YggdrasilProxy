import os

# 修改默认读取的配置文件，下面是可选的配置文件
# toml json json5 yaml
ConfigExtension = "toml"

# 全局变量初始化
workDir = os.getcwd()
ConfigPath = str(workDir + os.sep + "configs")
logs = bool()
debuglevel = int()
port = int()
ip = str()
configData = dict()
publickeys = None
updatePublickeysTime = int()
