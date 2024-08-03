import os
import threading
import time
import json

from flask import Flask, jsonify, request
from modules.tools import update_publickeys
from modules.profileRequest import RequestProfile

app = Flask(__name__)
reqProfile = RequestProfile

publickeys: None


# publickeys更新
def update_key_thread():
    global publickeys
    while True:
        publickeys = None
        publickeys = update_publickeys()
        time.sleep(7000)


Key_thread = threading.Thread(target=update_key_thread)
Key_thread.daemon = True
Key_thread.start()


# 访问根返回值
@app.get(rule="/")
def get_root():
    path: str = f"{os.getcwd()}{os.sep}modules{os.sep}static{os.sep}index.json"
    with open(path, mode="rb") as index:
        return jsonify(json.load(index))


# publickeys代理
@app.get(rule="/minecraftservices/publickeys")
def publickeys():
    return jsonify(publickeys)


# hasJoined判断
@app.get(rule="/sessionserver/session/minecraft/hasJoined")
def has_joined():
    server_id = request.args.get('serverId')
    username = request.args.get('username')
    try:
        user_profile = reqProfile.request_mojang_server(username, server_id)
        print("official")
        return jsonify(user_profile)
    except ValueError:
        user_profile = reqProfile.request_bs_server(username, server_id)
        print("third party")
        return jsonify(user_profile)


