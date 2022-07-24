from flask import Blueprint, render_template, request, jsonify
from emotes.html import *

views = Blueprint(__name__, "views")


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/emotes")
def emotes():
    if user := request.args.get("user"):
        return user_page(user)
    elif emote := request.args.get("emote"):
        return top_page(emote)
    else:
        return top5s_page()


@views.route("/api/emotes")
def api():
    if user := request.args.get("user"):
        return user_api(user)
    elif emote := request.args.get("emote"):
        return top_api(emote)
    else:
        return top5s_api()
