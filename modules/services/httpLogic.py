import json
import os.path

from flask import Flask, jsonify, request

import modules.globalVariables as gVar
from modules.services.hasJoinedService import HasJoinedService

app = Flask(__name__)
has_joined_service = HasJoinedService()

# Return index.json
@app.route(rule='/', methods=['GET'])
def index():
    index_path = os.path.join(gVar.webDir, 'index.json')
    with open(index_path, 'r') as f:
        return jsonify(json.load(f))

# Return Publickeys
@app.route(rule='/minecraftservices/publickeys', methods=['GET'])
def publickeys():
    return jsonify(gVar.publickey)

@app.route(rule='/sessionserver/session/minecraft/hasJoined', methods=['GET'])
def has_joined():
    # Get URL Params
    server_id = request.args.get("serverId")
    username = request.args.get("username")
    # Send username and serverId to get user profile
    profile = has_joined_service.get_profile(username=username, server_id=server_id)
    return jsonify(profile)

