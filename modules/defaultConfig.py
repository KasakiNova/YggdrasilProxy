# 默认配置文件
default_config = """[General]
# Enable this config
# default: true
enable=true
# Save Logs
# default: false
save-log=false
# false: info, true: debug,
# default: false
debug=true
# Binding IP
# default: "127.0.0.1"
ip = "127.0.0.1"
# Service listening port
# default: 30000
port=30000
# Publickeys Update time
# Default: 7200
# 0 is no check for updates
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
# Mojang Official Server
Name="Mojang"
ServerType="Official"
NeedProxy=false
Url="https://sessionserver.mojang.com"

[Server.1]
# LittleSkin Server
Name="LittleSkin"
ServerType="Blessing"
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
