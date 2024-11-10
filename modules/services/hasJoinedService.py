from http.client import responses

import requests
from requests import Response

import modules.globalVariables as gVar
from modules.Errors import FailureToFetchProfile


class HasJoinedService:
    def __init__(self):
        self.__username = ""
        self.__server_id = ""
        self.__proxyEnable = gVar.cfgContext['Proxy']['enable']
        self.__proxies = gVar.proxies

    def get_profile(self, username: str, server_id: str):
        self.__username = username
        self.__server_id = server_id
        servers = gVar.cfgContext["Server"]
        for serial in servers.values():
            if serial['ServerType'].lower() in {"mojang", "official"}:
                try:
                    msg = self.request_mojang(serial['NeedProxy'])
                    if msg['status']:
                        print(f"Successfully fetched player {username} in {serial['Name']} server")
                        return msg['data']
                    else:
                        raise FailureToFetchProfile(f"Unable to get {username} profile from {serial['Name']} server")
                except FailureToFetchProfile as e:
                    print(e)
                    continue
            elif serial['ServerType'].lower() in {"blessing"}:
                try:
                    msg = self.request_blessing(serial['Url'], serial['NeedProxy'])
                    if msg['status']:
                        print(f"Successfully fetched player {username} in {serial['Name']} server")
                        return msg['data']
                    else:
                        raise FailureToFetchProfile(f"Unable to get {username} profile from {serial['Name']} server")
                except FailureToFetchProfile as e:
                    print(e)
                    continue
            else:
                print(f"Unable to get player {username} profile from All server")

    def request_tool(self, url, proxy):
        if proxy and self.__proxyEnable:
            response = requests.get(url, proxies=self.__proxies)
        else:
            response = requests.get(url=url)
        if not response.status_code == 200:
            return {'status': False}
        return_msg = {'status': True, 'data': response.json()}
        return return_msg

    def request_mojang(self, proxy: bool):
        domain = "https://sessionserver.mojang.com"
        url = (
            f"{domain}/session/minecraft/hasJoined?username={self.__username}&serverId={self.__server_id}"
        )
        return self.request_tool(url, proxy)

    def request_blessing(self, i_url, proxy: bool):
        url = f"{i_url}/sessionserver/session/minecraft/hasJoined?username={self.__username}&serverId={self.__server_id}"
        return self.request_tool(url, proxy)


