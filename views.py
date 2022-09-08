from flask import Blueprint, render_template, request
from emotes.html import *
from users.html import *
from dominate.tags import iframe

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
    if emote := request.args.get("emote"):
        return emote_top_page(emote)
    else:
        return emote_top5s_page()


@views.route("/api/emotes")
def api():
    if user := request.args.get("user"):
        return emote_user_api(user)
    elif emote := request.args.get("emote"):
        return emote_top_api(emote)
    else:
        return top5s_api()


@views.route("/donate")
def donate():
    dono_message = (
        "This site costs about $10/month to host. If you enjoy my work and "
        "are feeling generous, a donation of any amount would be much appreciated! "
    )
    with div(align="center") as container:
        emote_to_html("dggL")
        p(dono_message, align="center", style="width:400px")
        iframe(
            id="kofiframe",
            src="https://ko-fi.com/tenadev/?hidefeed=true&widget=true&embed=true&preview=true",
            style="border:none;width:400px;height:615px;padding:4px;background:#1e1e1e;",
            title="tenadev",
        )
        p()
    return render_template(
        "with_user_search.html",
        title="donate",
        header=f"Support me",
        content=container,
    )
