import requests

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
        # Use a for loop to iterate through the server list
        for serial in servers.values():
            # If ServerType is about mojang or official, running this
            if serial['ServerType'].lower() in {"mojang", "official"}:
                try:
                    msg = self.request_mojang(serial['NeedProxy'])
                    if msg['status']:
                        print(f"Successfully fetched player {username} in {serial['Name']} server")
                        # If debugMode is enabled, print the return value to the console
                        if gVar.debugMode:
                            print(msg['data'])
                        return msg['data']
                    else:
                        # If the user data cannot be obtained from Mojang servers, an exception is raised
                        raise FailureToFetchProfile(f"Unable to get {username} profile from {serial['Name']} server")
                except FailureToFetchProfile as e:
                    print(e)
                    continue
            # this is about use blessing skin server, if
            elif serial['ServerType'].lower() in {"blessing"}:
                try:
                    msg = self.request_blessing(serial['Url'], serial['NeedProxy'])
                    # Check status in msg, if this is true check debugMode and return data in msg
                    if msg['status']:
                        print(f"Successfully fetched player {username} in {serial['Name']} server")
                        # If debugMode is enabled, print the return value to the console
                        if gVar.debugMode:
                            print(msg['data'])
                        return msg['data']
                    else:
                        # If the user data cannot be obtained from blessing auth servers, an exception is raised
                        raise FailureToFetchProfile(f"Unable to get {username} profile from {serial['Name']} server")
                except FailureToFetchProfile as e:
                    print(e)
                    continue
            else:
                # if all server cannot find user profile
                print(f"Unable to get player {username} profile from All server")

    # request_tool use to request.get, but support proxy
    def request_tool(self, url, proxy):
        if proxy and self.__proxyEnable:
            response = requests.get(url, proxies=self.__proxies)
        else:
            response = requests.get(url=url)
        if not response.status_code == 200:
            return {'status': False}
        return_msg = {'status': True, 'data': response.json()}
        return return_msg

    # Request Mojang official session server
    # insert username and serverId build full url
    def request_mojang(self, proxy: bool):
        # this is mojang official session server
        domain = "https://sessionserver.mojang.com"
        # build request hasJoined Link
        url = f"{domain}/session/minecraft/hasJoined?username={self.__username}&serverId={self.__server_id}"
        # use request_tool to request
        return self.request_tool(url, proxy)

    # Request blessing skin server Yggdrasil API session server
    # insert username and serverId build full url
    def request_blessing(self, i_url, proxy: bool):
        # just build blessing skin server Yggdrasil API link
        url = f"{i_url}/sessionserver/session/minecraft/hasJoined?username={self.__username}&serverId={self.__server_id}"
        return self.request_tool(url, proxy)


