import requests

from modules.tools import proxies_link
import modules.globalVariables as Var


def request_tool(url, proxy):
    if proxy and Var.proxyEnable:
        proxies = proxies_link()
        response = requests.get(url=url, proxies=proxies)
    else:
        response = requests.get(url=url)
    if not response.status_code == 200:
        return "Error"
    return response.json()


# Mojang正版验证
def request_mojang_server(username, server_id, proxy):
    domain = "https://sessionserver.mojang.com"
    url = f"{domain}/session/minecraft/hasJoined?username={username}&serverId={server_id}"
    return request_tool(url, proxy)


# 使用Blessing Skin Server的Yggdrasil插件的请求
def request_bs_server(import_url, username, server_id, proxy):
    url = f"{import_url}/sessionserver/session/minecraft/hasJoined?username={username}&serverId={server_id}"
    return request_tool(url, proxy)
