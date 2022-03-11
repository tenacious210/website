from cgitb import html
from flask import Blueprint, render_template, request
import sqlite3
import requests


views = Blueprint(__name__, "views")
emote_json = requests.get("https://cdn.destiny.gg/emotes/emotes.json").json()


def add_columns(original, columns):
    start_html = '<div class="container"><div class="row justify-content-center">'
    start_html += f'<div class="col-1 py-1" align="center"><b>{columns[0]}</b></div>'
    for c in columns[1:]:
        start_html += f'<div class="col-2 py-1" align="center"><b>{c}</b></div>'
    start_html += '<div class="w-100"></div>'
    end_html = "</div></div>"
    return f"{start_html}{original}{end_html}"


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
        html = f'<a href="/emotes?emote={emote}"><img src="{img_link}"></a>'
    else:
        html = f'<a href="/emotes?emote={emote}"><div title="{emote}" class="emote {emote}"></div></a>'
    return html


@views.route("/")
def index():
    return render_template("base.html", text="Home page", title="home")


@views.route("/emotes")
def emotes():
    con = sqlite3.connect("user_emotes.db")
    cur = con.cursor()
    emotes = [i[1] for i in cur.execute("PRAGMA table_info(LastMonth)")][1:]
    if user := request.args.get("user"):
        username = cur.execute(
            f"SELECT UserName FROM LastMonth WHERE LOWER(UserName)='{user.lower()}'"
        )
        if username := username.fetchall():
            username = username[0][0]
            userstats_raw = cur.execute(
                f"SELECT * FROM LastMonth WHERE UserName = '{username}'"
            )
            results = userstats_raw.fetchall()
            fields = [d[0] for d in userstats_raw.description]
            emotestats_unsorted = {fields[i]: results[0][i] for i in range(len(fields))}
            emotestats_unsorted.pop("UserName")
            emotestats = dict(
                reversed(sorted(emotestats_unsorted.items(), key=lambda item: item[1]))
            )
            html_payload = ""
            i = 0
            for emote, amount in emotestats.items():
                i += 1
                html_payload += f'<div class="col-1 py-1" align="center">{i}</div>'
                html_payload += f'<div class="col-2 py-1" align="center">{emote_to_html(emote)}</div>'
                html_payload += f'<div class="col-2 py-1" align="center">{amount}</div><div class="w-100"></div>'
            html_payload = add_columns(html_payload, ("Rank", "Emote", "30 day total"))
        else:
            html_payload = "Couldn't find that user"
        payload = render_template(
            "emotes.html",
            title="user emote",
            header=f"Emote stats for {username}",
            content=html_payload,
        )
    elif emote := request.args.get("emote"):
        if emote in emotes:
            rank_info = cur.execute(
                f"SELECT UserName, {emote}, RANK() OVER(ORDER BY {emote} DESC) FROM LastMonth LIMIT 100"
            )
            html_payload = ""
            for info in rank_info:
                user_info = ""
                username, amount, rank = info
                user_info += f'<div class="col-2 py-1" align="center"><a href="/emotes?user={username}">{username}</a></div>'
                user_info += f'<div class="col-2 py-1" align="center">{amount}</div>'
                html_payload += f'<div class="col-1 py-1" align="center">{rank}</div>{user_info}<div class="w-100"></div>'
            html_payload = add_columns(
                html_payload, ("Rank", "Username", "30 day total")
            )
        else:
            html_payload = "Couldn't find that emote"
        payload = render_template(
            "emotes.html",
            title="emote",
            header=f"Top 100 {emote_to_html(emote)} posters of the month",
            content=html_payload,
        )
    else:
        top5s_unsorted = {}
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
        html_payload = ""
        for emote, top5 in top5s.items():
            user_links = "".join(
                [
                    f'<div class="col-2 py-1" align="center"><a href="/emotes?user={user}">{user}</a>: {amount} </div>'
                    for user, amount in top5.items()
                ]
            )
            html_payload += f'<div class="col-1 py-1" align="center">{emote_to_html(emote)}</div>{user_links}<div class="w-100"></div>'
        html_payload = add_columns(
            html_payload,
            (
                "Emote",
                "First place",
                "Second place",
                "Third place",
                "Fourth place",
                "Fifth place",
            ),
        )
        payload = render_template(
            "emotes.html",
            title="emotes",
            header="Top emote posters of the month",
            content=html_payload,
        )
    con.close()
    return payload
