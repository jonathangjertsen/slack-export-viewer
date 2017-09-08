import os
import json
import sys

import flask
from flask_basicauth import BasicAuth

app = flask.Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

try:
    with open(os.path.join(os.path.dirname(__file__), "../secrets.json")) as f:
        secrets = json.load(f)
        app.config['BASIC_AUTH_USERNAME'] = secrets["username"]
        app.config['BASIC_AUTH_PASSWORD'] = secrets["password"]
        app.config['BASIC_AUTH_FORCE'] = True
        basic_auth = BasicAuth(app)
except FileNotFoundError:
    print("No secrets.json file found, no auth will be used.")

@app.route("/channel/<name>")
def channel_name(name):
    messages = flask._app_ctx_stack.channels[name]
    channels = list(flask._app_ctx_stack.channels.keys())
    return flask.render_template("viewer.html", messages=messages,
                                 name=name.format(name=name),
                                 channels=sorted(channels))


@app.route("/")
def index():
    channels = list(flask._app_ctx_stack.channels.keys())
    if "general" in channels:
        return channel_name("general")
    else:
        return channel_name(channels[0])
