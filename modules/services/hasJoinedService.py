import threading
from typing import TypedDict

import requests

import modules.globalVariables as gVar
from modules.Errors import FailureToFetchProfile
from modules.services.blacklistService import BlacklistService
from modules.database.accountInfoDB import AccountInfoDB

session = requests.Session()
session.trust_env = False


class MsgType(TypedDict):
    status: bool
    data: dict


class HasJoinedService:
    def __init__(self):
        self.__username = ""
        self.__server_id = ""
        self.__proxyEnable = gVar.cfgContext['Proxy']['enable']
        self.__proxies = gVar.proxies
        self.blacklist = BlacklistService()
        self.account_db = AccountInfoDB()

    def get_profile(self, username: str, server_id: str):
        self.__username = username
        self.__server_id = server_id
        servers = gVar.cfgContext["Server"]
        # Use a for loop to iterate through the server list
        for dict_server_id, serial in servers.items():
            # If ServerType is about mojang or official, running this
            if serial['ServerType'].lower() in {"mojang", "official"}:
                try:
                    msg: MsgType = self.request_mojang(serial['NeedProxy'])
                    if msg['status']:
                        print(f"Successfully fetched player {username} in {serial['Name']} server")
                        # If debugMode is enabled, print the return value to the console
                        if gVar.debugMode:
                            print(msg['data'])

                        if self.blacklist.check_is_blacklisted(msg['data']['id'],dict_server_id):
                            return None
                        # When msg['data'] retrieves the data, input name,uuid, and the server ID
                        # from the configuration file into this function
                        # and attempt to add this account to the database.
                        self.try_to_add_account_to_db_thread(
                            msg['data']['name'],
                            msg['data']['id'],
                            dict_server_id
                        )
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
                    msg: MsgType = self.request_blessing(serial['Url'], serial['NeedProxy'])
                    # Check status in msg, if this is true check debugMode and return data in msg
                    if msg['status']:
                        print(f"Successfully fetched player {username} in {serial['Name']} server")
                        # If debugMode is enabled, print the return value to the console
                        if gVar.debugMode:
                            print(msg['data'])

                        if self.blacklist.check_is_blacklisted(msg['data']['id'], dict_server_id):
                            return None
                        self.try_to_add_account_to_db_thread(
                            msg['data']['name'],
                            msg['data']['id'],
                            dict_server_id
                        )
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
    def request_tool(self, url, proxy) -> dict:
        if proxy and self.__proxyEnable:
            response = requests.get(url, proxies=self.__proxies)
        else:
            response = requests.get(url=url)
        if not response.status_code == 200:
            return {'status': False}
        return_msg: MsgType = {'status': True, 'data': response.json()}
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


    def check_profile(self, data_dict):
        pass

    def try_to_add_account_to_db_thread(self, name, uuid, server):
        """Try to add account to accountDB thread"""
        def try_thread():
            if self.account_db.check_uuid_exists(uuid, server):
                if not self.account_db.get_name_by_uuid(uuid, server) == name:
                    self.account_db.update_account_name(uuid, name)
            else:
                self.account_db.insert_account(uuid, name, server)

        # this well be created a new thread
        try_add_thread = threading.Thread(target=try_thread)
        try_add_thread.daemon=True
        try_add_thread.start()

