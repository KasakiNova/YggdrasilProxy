import threading
from typing import TypedDict

import requests

import modules.globalVariables as gVar
from modules.Errors import FailureToFetchProfile, PlayerIsBaned
from modules.database.accountInfoDB import AccountInfoDB
from modules.services.blacklistService import BlacklistService


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
                    if msg['status'] is False:
                        raise FailureToFetchProfile(
                            f"Unable to get {username} profile from {serial['Name']} server")
                    player_baned = self.check_profile(msg, dict_server_id)
                    if player_baned:
                        print(f"Successfully fetched player {self.__username} in {serial['Name']} server")
                        return msg['data']
                    else:
                        if player_baned:
                            # If the user data cannot be obtained from Mojang servers, an exception is raised
                            raise FailureToFetchProfile(
                                f"Unable to get {username} profile from {serial['Name']} server")
                        else:
                            raise PlayerIsBaned(
                                f"Player {username} has baned"
                            )
                except FailureToFetchProfile as e:
                    print(e)
                    continue
                except PlayerIsBaned as e:
                    print(e)
                    return None
            # this is about use blessing skin server, if
            elif serial['ServerType'].lower() in {"blessing"}:
                try:
                    msg: MsgType = self.request_blessing(serial['Url'], serial['NeedProxy'])
                    if msg['status'] is False:
                        raise FailureToFetchProfile(
                            f"Unable to get {username} profile from {serial['Name']} server")
                    player_baned = self.check_profile(msg, dict_server_id)
                    # Check status in msg, if this is true check debugMode and return data in msg
                    if player_baned:
                        print(f"Successfully fetched player {self.__username} in {serial['Name']} server")
                        return msg['data']
                    else:
                        if not player_baned:
                            raise PlayerIsBaned(
                                f"Player {username} has baned"
                            )
                        else:
                            # If the user data cannot be obtained from Mojang servers, an exception is raised
                            raise FailureToFetchProfile(
                                f"Unable to get {username} profile from {serial['Name']} server")
                except FailureToFetchProfile as e:
                    print(e)
                    continue
                except PlayerIsBaned as e:
                    print(e)
                    return None
        # if all server cannot find player profile
        print(f"Unable to get player {username} profile from All server")
        return None


    # Enter the self.request_* dictionary and the server id in the configuration file
    # to try to determine whether the account is banned.
    # If it is not banned, try to add it to the database
    def check_profile(self, msg: MsgType, server_id) -> bool:
        if msg['status']:
            # If debugMode is enabled, print the return value to the console
            if gVar.debugMode:
                print(msg['data'])
            if self.account_db.check_uuid_exists(msg['data']['id'], server_id):
                return True
            # When the player is banned in the list, it returns false directly
            if self.blacklist.check_is_blacklisted(msg['data']['id'], server_id):
                return False
            # When msg['data'] retrieves the data, input name,uuid, and the server ID
            # from the configuration file into this function
            # and attempt to add this account to the database.
            self.try_to_add_account_to_db_thread(
                msg['data']['name'],
                msg['data']['id'],
                server_id
            )
            return True
        else:
            return False


    # request_tool use to requests.get, but support proxy
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


    #Create a new thread to try to add the account to the database.
    # If it already exists, do nothing.
    # If it already exists but the player name has changed, update the name
    def try_to_add_account_to_db_thread(self, name, uuid, server):
        """Try to add account to accountDB thread"""
        def try_thread():
            if self.account_db.check_uuid_exists(uuid, server):
                if not self.account_db.get_name_by_uuid(uuid, server) == name.lower():
                    self.account_db.update_account_name(uuid, name.lower())
            else:
                self.account_db.insert_account(uuid, name.lower(), server)
        # this well be created a new thread
        try_add_thread = threading.Thread(target=try_thread)
        try_add_thread.daemon=True
        try_add_thread.start()

