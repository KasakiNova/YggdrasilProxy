import json
import os

from flask import Flask, jsonify, request

from modules.profileRequest import request_mojang_server, request_bs_server
import modules.globalVariables as Var

app = Flask(__name__)


# 访问根返回值
@app.get(rule="/")
def get_root():
    path: str = f"{Var.workDir}{os.sep}modules{os.sep}static{os.sep}index.json"
    with open(path, mode="rb") as index:
        return jsonify(json.load(index))


# publickeys代理
@app.get(rule="/minecraftservices/publickeys")
def publickeys():
    return jsonify(Var.publickeys)


# hasJoined
@app.get(rule="/sessionserver/session/minecraft/hasJoined")
def has_joined():
    server_id = request.args.get('serverId')
    username = request.args.get('username')
    try:
        user_profile = request_mojang_server(username, server_id)
        print("official")
        return jsonify(user_profile)
    except ValueError:
        user_profile = request_bs_server(username, server_id)
        print("third party")
        return jsonify(user_profile)
