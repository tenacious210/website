from flask import Blueprint, render_template, request
from emotes.html import *
from users.html import *
from dominate.tags import iframe

views = Blueprint(__name__, "views")


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/users")
def users_home_response():
    return users_home()


@views.route("/users/<name>")
def users_response(name):
    return users_page(name)


@views.route("/api/users")
def users_levels_api_response():
    return all_users_api()


@views.route("/api/users/<user>")
def users_api_response(user):
    return one_user_api(user)


@views.route("/emotes")
def emotes_home_response():
    return emote_top5s_page()


@views.route("/emotes/<emote>")
def emotes_response(emote):
    return emote_top_page(emote)


@views.route("/api/emotes")
def emotes_api_response():
    return emote_top5s_api()


@views.route("/api/emotes/<emote>")
def emotes_top_api_response(emote):
    return emote_top100_api(emote)


@views.route("/donate")
def donate():
    dono_message = (
        "My projects cost about $10/month to host. If you enjoy my work and "
        "are feeling generous, a donation of any amount would be much appreciated! "
    )
    with div(align="center") as container:
        emote_to_html("dggL")
        p(dono_message, align="center", style="width:400px")
        iframe(
            id="github sponsors",
            src="https://github.com/sponsors/tenacious210/card",
            style="border:none;width:450px;height:150px;padding:4px",
        )
        p()
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


@views.route("/voiture")
def voiture():
    with div(align="center") as container:
        p()
        iframe(
            width="560",
            height="315",
            src="https://www.youtube.com/embed/tZ_gn0E87Qo",
            frameborder="0",
        )
    return render_template(
        "with_user_search.html",
        title="voiture",
        header=emote_to_html("LULW"),
        content=container,
    )


@views.route("/cantclosevim")
def cantclosevim():
    with div(align="center") as container:
        p()
        iframe(
            width="384",
            height="683",
            src="https://www.youtube.com/embed/TDestzutf1s",
            frameborder="0",
        )
    return render_template(
        "with_user_search.html",
        title="cantclosevim",
        header=emote_to_html("LULW"),
        content=container,
    )
