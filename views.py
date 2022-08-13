from flask import Blueprint, render_template, request
from emotes.html import *
from users.html import *

views = Blueprint(__name__, "views")


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/users")
def users_home_page():
    return users_home()


@views.route("/users/<name>")
def users(name):
    return users_page(name)


@views.route("/api/users/<user>")
def users_api1(user):
    return users_api(user)


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
