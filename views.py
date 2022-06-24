from flask import Blueprint, render_template, request, jsonify
from emotes.html import emotes_user, emotes_top5s, emotes_top100
from emotes.db import get_emote_top5s, get_emote_top_posters, get_emotes_user

views = Blueprint(__name__, "views")
top5s_page_cached = None
top5s_cached = None


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/emotes")
def emotes():
    if user := request.args.get("user"):
        payload = emotes_user(user)
    elif emote := request.args.get("emote"):
        payload = emotes_top100(emote)
    else:
        global top5s_page_cached
        if not top5s_page_cached:
            top5s_page_cached = emotes_top5s()
        payload = top5s_page_cached
    return payload


@views.route("/api/emotes")
def api():
    if user := request.args.get("user"):
        payload = jsonify(get_emotes_user(user))
    elif emote := request.args.get("emote"):
        if amount := request.args.get("amount"):
            try:
                amount = int(amount)
            except ValueError:
                amount = 100
            payload = jsonify(get_emote_top_posters(emote, ranks=int(amount)))
        else:
            payload = jsonify(get_emote_top_posters(emote))
    else:
        global top5s_cached
        if not top5s_cached:
            top5s_cached = get_emote_top5s()
        payload = top5s_cached
    return payload
