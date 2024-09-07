import json
import time

from colorama import Fore, Style

import modules.globalVariables as Var

from requests import get
from modules.customError import GetPublickeyFailureError


def update_key_thread():
    print(Fore.GREEN + "[Update PublicKeys Loaded]" + Style.RESET_ALL)
    while True:
        Var.publickeys = None
        Var.publickeys = update_publickeys()
        time.sleep(Var.updatePublickeysTime)
    pass


def save_publickeys2folder(keys: dict, folder: str):

    pass


# 检查publickeys是否正确
def check_publickey_structure(json_data):
    try:
        for key in json_data:
            if key not in ["profilePropertyKeys", "playerCertificateKeys"]:
                return False
            if not isinstance(json_data[key], list):
                return False
            for item in json_data[key]:
                if not isinstance(item, dict) or "publicKey" not in item:
                    return False
        return True
    except json.JSONDecodeError:
        return False


# publickeys更新
def update_publickeys():
    # 获取publickeys
    # 如果无法从Mojang官方获取就从LittleSkin获取
    try:
        url = "https://api.minecraftservices.com/publickeys"
        response = get(url)
        if response.status_code == 200:
            if check_publickey_structure(response.json()):
                return response.json()
            else:
                raise GetPublickeyFailureError("Failed to fetch publickeys from Mojang.")
        else:
            raise GetPublickeyFailureError("Failed to fetch publickeys from Mojang.")
    except GetPublickeyFailureError as error_info:
        print(error_info)
        url = "https://littleskin.cn/api/yggdrasil/minecraftservices/publickeys"
        response = get(url=url)
        if response.status_code == 200:
            if check_publickey_structure(response.json()):
                return response.json()
            else:
                raise GetPublickeyFailureError("Failed to fetch publickeys from LittleSkin.")
        else:
            print("Failed to fetch publickeys from LittleSkin.")
