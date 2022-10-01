from dominate.tags import *
from .db import *
from flask import render_template, request, jsonify
import requests
from requests import JSONDecodeError
from re import match

try:
    emote_json = requests.get("https://cdn.destiny.gg/emotes/emotes.json").json()
except JSONDecodeError:
    emote_json = {}


def emote_to_html(emote):
    if emote in (
        "HACKERMAN",
        "YEEHAW",
        "PARDNER",
        "BibleThump",
        "ATAB",
        "PepeHands",
        "Slumlord",
        "LOVE",
        "Blubstiny",
        "GRUGingOverIt",
        "ATAB",
    ):
        for e in emote_json:
            if e["prefix"] == emote:
                img_link = e["image"][0]["url"]
        html = a(img(src=img_link), href=f"/emotes/{emote}")
    else:
        html = a(div(title=emote, cls=f"emote {emote}"), href=f"/emotes/{emote}")
    return html


def emote_top5s_api():
    if amount := request.args.get("amount"):
        try:
            amount = int(amount)
        except ValueError:
            amount = None
    return jsonify(get_emote_top5s(amount=amount))


def emote_top100_api(emote):
    if amount := request.args.get("amount"):
        try:
            amount = int(amount)
        except ValueError:
            amount = 100
        payload = jsonify(get_emote_top_posters(emote, amount=amount))
    else:
        payload = jsonify(get_emote_top_posters(emote))
    return payload


def emote_top_page(emote):
    if top100 := get_emote_top_posters(emote):
        with div(cls="container") as container:
            with table(cls="three-column", align="center"):
                col(style="width: 20%", span="1")
                col(style="width: 60%", span="1")
                col(style="width: 20%", span="1")
                with tr():
                    for c in ("Rank", "Name", "Amount"):
                        td(b(c), align="center")
                i = 0
                for username, amount in top100.items():
                    i += 1
                    with tr():
                        td(i, align="center")
                        td(
                            a(username, href=f"/users/{username}"),
                            align="center",
                        )
                        td(amount, align="center")
    else:
        container = p("Couldn't find that emote", align="center")
    payload = render_template(
        "with_user_search.html",
        title="emote",
        header=f"Top 100 {emote_to_html(emote)} posters of the month",
        content=container,
    )
    return payload


def emote_top5s_page():
    with div(cls="container") as container:
        with table(style="width: 100%", align="center"):
            col(style="width: 5%", span="1")
            col(style="width: 19%", span="5")
            with tr():
                for c in ("Emote", "First", "Second", "Third", "Fourth", "Fifth"):
                    td(b(c), align="center", style="padding-bottom: 5px")
            for emote, top5 in get_emote_top5s().items():
                with tr():
                    td(
                        emote_to_html(emote),
                        align="center",
                        style="padding-bottom: 5px",
                    )
                    for username, amount in top5.items():
                        with td(align="center", style="padding-bottom: 5px") as poster:
                            a(username, href=f"/users/{username}")
                        poster.add(f": {amount}")
    payload = render_template(
        "with_user_search.html",
        title="emotes",
        header="Top emote posters of the month",
        content=container,
    )
    return payload
