import requests


# Mojang正版验证
def request_mojang_server(username, import_server_id):
    domain = "https://sessionserver.mojang.com"
    url = f"{domain}/session/minecraft/hasJoined?username={username}&serverId={import_server_id}"
    response = requests.get(url=url)
    return response.json()


# 使用Blessing Skin Server的Yggdrasil插件的请求
def request_bs_server(username, import_server_id):
    domain = "https://littleskin.cn/api/yggdrasil"
    url = f"{domain}/sessionserver/session/minecraft/hasJoined?username={username}&serverId={import_server_id}"

    # uuid_response = requests.get(url=url)
    # json_temp = uuid_response.json()
    # uuid = json_temp['id']

    response = requests.get(url=url)
    return response.json()
