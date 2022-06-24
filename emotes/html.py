from dominate.tags import *
from .db import *
from flask import render_template
import requests

emote_json = requests.get("https://cdn.destiny.gg/emotes/emotes.json").json()


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
    ):
        for e in emote_json:
            if e["prefix"] == emote:
                img_link = e["image"][0]["url"]
        html = a(img(src=img_link), href=f"/emotes?emote={emote}")
    else:
        html = a(div(title=emote, cls=f"emote {emote}"), href=f"/emotes?emote={emote}")
    return html


def emotes_user(user):
    if top_emotes := get_emotes_user(user):
        with div(cls="container") as container:
            with div(cls="row justify-content-center"):
                div(b("Rank"), cls="col-1 py-1", align="center")
                for c in ("Emote", "30 day total"):
                    div(b(c), cls="col-2 py-1", align="center")
                div(cls="w-100")
                i = 0
                for emote, amount in top_emotes.items():
                    i += 1
                    div(i, cls="col-1 py-1", align="center")
                    div(emote_to_html(emote), cls="col-2 py-1", align="center")
                    div(amount, cls="col-2 py-1", align="center")
                    div(cls="w-100")
    else:
        container = "Couldn't find that user"
    payload = render_template(
        "emotes.html",
        title="user emote",
        header=f"Emote stats for {user}",
        content=container,
    )
    return payload


def emotes_top100(emote):
    if top100 := get_emote_top_posters(emote):
        with div(cls="container") as container:
            with div(cls="row justify-content-center"):
                div(b("Rank"), cls="col-1 py-1", align="center")
                for c in ("Username", "30 day total"):
                    div(b(c), cls="col-2 py-1", align="center")
                div(cls="w-100")
                i = 0
                for user, amount in top100.items():
                    i += 1
                    div(i, cls="col-1 py-1", align="center")
                    div(
                        a(user, href=f"/emotes?user={user}"),
                        cls="col-2 py-1",
                        align="center",
                    )
                    div(amount, cls="col-2 py-1", align="center")
                    div(cls="w-100")
    else:
        container = "Couldn't find that emote"
    payload = render_template(
        "emotes.html",
        title="emote",
        header=f"Top 100 {emote_to_html(emote)} posters of the month",
        content=container,
    )
    return payload


def emotes_top5s(number_of_days=30):
    with div(cls="container") as container:
        with div(cls="row justify-content-center"):
            div(b("Emote"), cls="col-1 py-1", align="center")
            for c in ("First", "Second", "Third", "Fourth", "Fifth"):
                div(b(c), cls="col-2 py-1", align="center")
            div(cls="w-100")
            for emote, top5 in get_emote_top5s(number_of_days=number_of_days).items():
                div(emote_to_html(emote), cls="col-1 py-1", align="center")
                for user, amount in top5.items():
                    with div(cls="col-2 py-1", align="center") as user_num:
                        a(user, href=f"/emotes?user={user}")
                    user_num.add(f": {amount}")
                div(cls="w-100")
    payload = render_template(
        "emotes.html",
        title="emotes",
        header="Top emote posters of the month",
        content=container,
    )
    return payload
