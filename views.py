from flask import Blueprint, render_template, request, jsonify
from emotes.html import user_page, top5s_page, top100_page, user_api, top_api
from emotes.db import get_emote_top5s

views = Blueprint(__name__, "views")
top5s_page_cached = None
top5s_cached = None


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/emotes")
def emotes():
    if user := request.args.get("user"):
        payload = user_page(user)
    elif emote := request.args.get("emote"):
        payload = top100_page(emote)
    else:
        global top5s_page_cached
        if not top5s_page_cached:
            top5s_page_cached = top5s_page()
        payload = top5s_page_cached
    return payload


@views.route("/api/emotes")
def api():
    if user := request.args.get("user"):
        return user_api(user)
    elif emote := request.args.get("emote"):
        return top_api(emote)
    else:
        global top5s_cached
        if not top5s_cached:
            top5s_cached = get_emote_top5s()
        payload = jsonify(top5s_cached)
    return payload
