import requests


# Mojang正版验证
def request_mojang_server(username, server_id):
    domain = "https://sessionserver.mojang.com"
    url = f"{domain}/session/minecraft/hasJoined?username={username}&serverId={server_id}"
    response = requests.get(url=url)
    if not response.status_code == 200:
        return "Error"
    return response.json()


# 使用Blessing Skin Server的Yggdrasil插件的请求
def request_bs_server(import_url, username, server_id):
    url = f"{import_url}/sessionserver/session/minecraft/hasJoined?username={username}&serverId={server_id}"
    response = requests.get(url=url)
    if not response.status_code == 200:
        return "Error"
    return response.json()
