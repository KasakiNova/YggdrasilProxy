import json
import os

from flask import Flask, jsonify, request

import modules.globalVariables as Var

from modules.profileRequest import request_mojang_server, request_bs_server
from modules.configMgr import read_server_config
from modules.customError import FailureToFetchProfileError

app = Flask(__name__)


# 访问根返回值
@app.get(rule="/")
def get_root():
    path: str = f"{Var.workDir}{os.sep}static{os.sep}index.json"
    with open(path, mode="rb") as index:
        return jsonify(json.load(index))


# publickeys代理
@app.get(rule="/minecraftservices/publickeys")
def publickeys():
    return jsonify(Var.publickeys)


# hasJoined
@app.get(rule="/sessionserver/session/minecraft/hasJoined")
def has_joined():
    # 获取参数
    server_id = request.args.get('serverId')
    username = request.args.get('username')
    # 使用循环获取用户信息
    for serial in range(len(Var.configData["Server"])):
        name, proxy, url, server_type = read_server_config(serial)
        # Mojang官方
        if server_type == "official":
            try:
                profile_data = request_mojang_server(username, server_id, proxy)
                if profile_data == "Error":
                    raise FailureToFetchProfileError(f"Unable to get {username} profile from {name} server")
                else:
                    print(f"Successfully fetched player {username} in {name} server")
                    return jsonify(profile_data)
            except FailureToFetchProfileError as error_info:
                serial += 1
                print(error_info)
                continue
        # BlessingSkinServer
        elif server_type == "blessing":
            try:
                profile_data = request_bs_server(url, username, server_id, proxy)
                if profile_data == "Error":
                    raise FailureToFetchProfileError(f"Unable to get {username} profile from {name} server")
                else:
                    print(f"Successfully fetched player {username} in {name} server")
                    return jsonify(profile_data)
            except FailureToFetchProfileError as error_info:
                serial += 1
                print(error_info)
                continue
        else:
            print(f"Unable to get player {username} profile from All server")
