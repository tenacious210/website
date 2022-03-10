from flask import Blueprint, render_template, request
from flask.json import jsonify
import sqlite3
import requests


views = Blueprint(__name__, "views")


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/emotes")
def emotes():
    emote_json = requests.get("https://cdn.destiny.gg/emotes/emotes.json").json()
    con = sqlite3.connect("user_emotes.db")
    cur = con.cursor()
    if user := request.args.get("user"):
        userstats = cur.execute(f"SELECT * FROM LastMonth WHERE UserName='{user}';")
        if results := userstats.fetchall():
            fields = [d[0] for d in userstats.description]
            message = {fields[i]: results[0][i] for i in range(len(fields))}
        else:
            message = "Couldn't find that user"
        payload = render_template(
            "user.html", title="user emote", user=f"{user}", content=f"{message}"
        )
    elif emote := request.args.get("emote"):
        payload = render_template(
            "emote.html", title="emote", emote=f"{emote}", content=None
        )
    else:
        top5s_unsorted = {}
        emotes = [i[1] for i in cur.execute("PRAGMA table_info(LastMonth)")][1:]
        for emote in emotes:
            top5 = cur.execute(
                f"SELECT UserName, {emote} FROM LastMonth WHERE {emote} > 0 ORDER BY {emote} DESC LIMIT 5"
            )
            top5s_unsorted[emote] = dict(top5.fetchall())
        top5s_values = {}
        for emote, top5 in top5s_unsorted.items():
            weight = 0
            for count in top5.values():
                weight += count
            top5s_values[emote] = weight
        top5s_by_value = [
            e[0] for e in reversed(sorted(top5s_values.items(), key=lambda i: i[1]))
        ]
        top5s = {e: top5s_unsorted[e] for e in top5s_by_value}
        html_payload = '<div class="container"><div class="row">'
        html_payload += '<div class="col-1 py-1" align="center"><b>Emote</b></div>'
        for p in (
            "First place",
            "Second place",
            "Third place",
            "Fourth place",
            "Fifth place",
        ):
            html_payload += f'<div class="col-2 py-1" align="center"><b>{p}</b></div>'
        html_payload += '<div class="w-100"></div>'
        for emote, top5 in top5s.items():
            user_links = "".join(
                [
                    f'<div class="col-2 py-1" align="center"><a href="/emotes?user={user}">{user}</a>: {amount} </div>'
                    for user, amount in top5.items()
                ]
            )
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
                html_payload += f'<div class="col-1 py-1" align="center"><a href="/emotes?emote={emote}"><img src="{img_link}"></a></div>{user_links}<div class="w-100"></div>'
            else:
                html_payload += f'<div class="col-1 py-1" align="center"><a href="/emotes?emote={emote}"><div title="{emote}" class="emote {emote}"></div></a></div>{user_links}<div class="w-100"></div>'
        html_payload += "</div></div>"
        payload = render_template("emotes.html", title="emotes", content=html_payload)
    con.close()
    return payload
