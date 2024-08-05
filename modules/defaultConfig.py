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
# Set Publickeys Update time
UpdatePublickeysTime=7200

[Proxy]
# Enable Proxy
enable=false
# Proxy Address
# Protocol input required
# Examples: address="http://127.0.0.1:8080" or address="socks5"
# Supported Protocols: http, https, socks5
address=""
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


def create_def_config_file(path):
    filename = str(path + "config.toml")
    with open(filename, 'w') as configfile:
        configfile.write(default_config)
