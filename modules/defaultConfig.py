# 默认配置文件
default_config = """[General]
# Enable this config
# default: true
enable=true
# Save Logs
# default: false
logs=false
# 1: info, 2: debug,
# Console and logs use this
# default: 1
debuglevel=1
# Binding IP
# default: "127.0.0.1"
ip = "127.0.0.1"
# Service listening port
# default: 30000
port=30000
# Publickeys Update time
# Default: 7200
UpdatePublickeysTime=7200

[Proxy]
# Enable Proxy
# Default: false
enable=false
# Proxy Address
# Protocol input required
# Examples: address="http://127.0.0.1:8080"
# Supported Protocols: http, https
address="127.0.0.1:8080"
# Enable Auth
# Default: false
enable_auth=false
# Proxy Auth Username
username=""
# Proxy Auth Password
password=""

[Server.0]
# Mojang Offical Server
Name="Mojang"
NeedProxy=false
Url="https://sessionserver.mojang.com"

[Server.1]
# LittleSkin Server
Name="LittleSkin"
NeedProxy=false
Url="https://littleskin.cn/api/yggdrasil"
"""

# 默认index.json
default_index = """{
    "Man!": {
        "What can i say!": "Mamba, Out!"
    }
}"""


def create_config_file(path):
    filename = str(path + "config.toml")
    with open(filename, 'w') as configfile:
        configfile.write(default_config)


# 创建index
def create_index_file(path: str):
    filename = str(path + "index.json")
    with open(filename, 'w') as configfile:
        configfile.write(default_index)
