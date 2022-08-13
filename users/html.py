from dominate.tags import *
from .db import get_lines, get_top_users, get_tng_score
from emotes.db import get_emotes_user
from emotes.html import emote_to_html
from flask import render_template, jsonify
from re import match


def calculate_level(xp):
    level = 1
    xp_needed = 1000
    while xp > xp_needed:
        level += 1
        xp -= xp_needed
        xp_needed *= 1.1

    return {
        "level": level,
        "xp": round(xp),
        "xp_needed": round(xp_needed),
        "progress": xp / xp_needed * 100,
    }


def users_home():
    top100 = get_top_users()
    with div(cls="container") as container:
        with div(cls="row justify-content-center"):
            div(b("Rank"), cls="col-1 py-1", align="center")
            for c in ("User", "Level"):
                div(b(c), cls="col-2 py-1", align="center")
            div(cls="w-100")
            i = 0
            for user, amount in top100.items():
                i += 1
                div(i, cls="col-1 py-1", align="center")
                div(a(user, href=f"/users/{user}"), cls="col-2 py-1", align="center")
                div(calculate_level(amount)["level"], cls="col-2 py-1", align="center")
                div(cls="w-100")
    payload = render_template(
        "users.html",
        title="users",
        header=f"Top 100 users in DGG",
        content=container,
    )
    return payload


def users_api(user):
    if not match(r"^[\w]+$", user):
        return jsonify(None)
    return jsonify(calculate_level(get_lines(user)))


def users_page(user):
    if not match(r"^[\w]+$", user):
        user = "?"
    if lines := get_lines(user):
        user_level = calculate_level(lines)
        with div(cls="container") as container:
            hr()
            with div(cls="progress"):
                div(
                    cls="progress-bar progress-bar-striped progress-bar-animated",
                    role="progressbar",
                    style=f"width: {user_level['progress']}%",
                )
            p()
            h3(f"{user_level['xp']}/{user_level['xp_needed']} XP", align="center")
            h3(f"Level {user_level['level']}", align="center")
            p(f"Total lines: {lines}", align="center")
            hr()
            if user_emotes := get_emotes_user(user, amount=5):
                with table(align="center"):
                    with tr():
                        for emote in user_emotes.keys():
                            td(emote_to_html(emote), style="padding: 3px")
                p(a("Favorite emotes", href=f"/emotes?user={user}"), align="center")
            hr()
            if tng_score := get_tng_score(user):
                with table(align="center"):
                    with tr():
                        td(
                            emote_to_html("BINGQILIN"),
                            style="padding-right: 5px; padding-bottom: 10px",
                        )
                        td(h4(tng_score, align="center"))
                p("tng69 social credit score", align="center")

    else:
        container = p("Couldn't find that user", align="center")
    return render_template(
        "users.html",
        title="user",
        header=f"User stats for {user}",
        content=container,
    )
