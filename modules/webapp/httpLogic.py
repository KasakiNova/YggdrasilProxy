import json
import os.path

import ujson
from flask import Flask, jsonify, request, Response
from flask.json.provider import JSONProvider
from werkzeug.http import HTTP_STATUS_CODES

import modules.globalVariables as gVar
from modules.services.hasJoinedService import HasJoinedService


class UjsonProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return ujson.dumps(obj)

    def loads(self, s, **kwargs):
        return ujson.loads(s)


# Init Flask and some Services
app = Flask(__name__)
has_joined_service = HasJoinedService()

# Set json encoder and decoder to ujson
app.json_provider_class = UjsonProvider
app.json = UjsonProvider(app)

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


# When a user attempts to log in, call 'has_joined_service.get_profile' to retrieve data and return it.
@app.route(rule='/sessionserver/session/minecraft/hasJoined', methods=['GET'])
def has_joined():
    # Get URL Params
    server_id = request.args.get("serverId")
    username = request.args.get("username")
    # Send username and serverId to get user profile
    profile = has_joined_service.get_profile(username=username, server_id=server_id)
    return Response(status=204) if profile is None else (jsonify(profile), 200)

