import json
import os
import threading
from json import JSONDecodeError
from time import sleep

import requests
from print_color import print

import modules.globalVariables as gVar
from modules.Errors import ErrorInGettingPublickeysFromMojang, ErrorInGettingPublickeysFromLittleSkin

session = requests.Session()
session.trust_env = False

class PublicKeys:
    def __init__(self):
        self.__keys = {}
        self.__staticDir = gVar.webDir
        self.__keyFile = os.path.join(self.__staticDir, 'publickeys.json')
        self.__check_time = gVar.cfgContext["General"]["CheckKeysTime"]
        self.__proxy_enable = gVar.cfgContext["Proxy"]["enable"]
        self.__proxies = gVar.proxies
        # If publickeys.json does not exist, so create it
        try:
            if not os.path.isfile(self.__keyFile):
                with open(self.__keyFile, 'w'):
                    pass
                pass
            else:
                with open(self.__keyFile, 'r') as keyFile:
                    self.__keys = json.loads(keyFile.read())
                    pass
                gVar.publickey = self.__keys
        except JSONDecodeError:
            pass
        except FileNotFoundError:
            pass


    def start_thread(self):
        """Try to start auto check publickeys"""
        if os.path.getsize(self.__keyFile) == 0:
            self.get_key()
            gVar.publickey = self.__keys
            self.write_json_to_file()
        else:
            if not self.check_key():
                self.get_key()
                gVar.publickey = self.__keys
                self.write_json_to_file()
        # check_time is 0 just running one time
        if not self.__check_time == 0:
            thread = threading.Thread(target=self.thread)
            thread.daemon = True
            thread.start()
            print("Update PublicKeys Services Loaded", tag='Success', tag_color='green', color='white')
        else:
            print("PublicKeys Loaded", tag='Success', tag_color='green', color='white')


    def thread(self):
        """Use while to Cycle Check"""
        self.get_key()
        sleep(5)
        while True:
            self.get_key()
            if self.__keys != gVar.publickey:
                gVar.publickey = self.__keys
                self.write_json_to_file()
            sleep(self.__check_time)


    def write_json_to_file(self):
        """Write publickeys to file"""
        with open(self.__keyFile, 'w') as file:
            file.write(json.dumps(self.__keys, indent=4, ensure_ascii=False))


    # Get the public key from the mojang server or LittleSkin
    # If you cannot get the public key from the mojang server, get it from the LittleSkin server
    def get_key(self) -> None:
        mojang_server = "https://api.minecraftservices.com/publickeys"
        little_skin = "https://littleskin.cn/api/yggdrasil/minecraftservices/publickeys"
        try:
            response = self.request(mojang_server)
            if response.status_code == 200:
                self.__keys = response.json()
                if self.check_key():
                    gVar.publickey = self.__keys
                else:
                    raise ErrorInGettingPublickeysFromMojang("Unable to get publickeys from mojang server")
            else:
                raise ErrorInGettingPublickeysFromMojang("Unable to get publickeys from mojang server")
        except ErrorInGettingPublickeysFromMojang as e:
            print(str(e), color='red')
            response = self.request(little_skin)
            if response.status_code == 200:
                self.__keys = response.json()
                if self.check_key():
                    gVar.publickey = self.__keys
                else:
                    raise ErrorInGettingPublickeysFromLittleSkin("Unable to get publickeys from LittleSkin server")
            else:
                raise ErrorInGettingPublickeysFromLittleSkin("Unable to get publickeys from LittleSkin server")
        except ErrorInGettingPublickeysFromLittleSkin as e:
            print(e)
        pass


    # Check whether the obtained publickeys is correct
    def check_key(self) -> bool:
        try:
            for key in self.__keys:
                if key not in ["profilePropertyKeys", "playerCertificateKeys"]:
                    return False
                if not isinstance(self.__keys[key], list):
                    return False
                for item in self.__keys[key]:
                    if not isinstance(item, dict) or "publicKey" not in item:
                        return False
            return True
        except json.JSONDecodeError:
            return False


    def request(self, url):
            try:
                if self.__proxy_enable:
                    print()
                    return requests.get(url, self.__proxies)
                else:
                    return requests.get(url)
            except requests.exceptions.RequestException:
                pass
