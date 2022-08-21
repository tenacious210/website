from dominate.tags import *
from .db import get_lines, get_top_users, get_tng_score, get_friends
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
    if (lines := get_lines(user)) and match(r"^[\w]+$", user):
        user_stats = calculate_level(lines)
        user_stats["tng_score"] = get_tng_score(user)
        user_stats["best_friends"] = get_friends(user, amount=3)
        return jsonify(user_stats)
    else:
        return jsonify(None)


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
            if friends := get_friends(user, amount=25):
                hr()
                p(b("Best friends"), align="center")
                friend_index = tuple(friends.keys())
                top30 = None
                if len(friend_index) > 3:
                    top3 = {k: friends[k] for k in friend_index[:3]}
                    top30 = {k: friends[k] for k in friend_index[3:]}
                else:
                    top3 = {k: friends[k] for k in friend_index}
                with div(align="center"):
                    with table(style="table-layout: fixed; width: 300px"):
                        col(style="width: 10%", span="1")
                        col(style="width: 80%", span="1")
                        col(style="width: 10%", span="1")
                        with tr():
                            for c in ("Rank", "Name", "Mentions"):
                                td(b(c), align="center")
                        i = 0
                        for username, amount in top3.items():
                            with tr():
                                i += 1
                                td(i, align="center")
                                td(
                                    a(username, href=f"/users/{username}"),
                                    align="center",
                                )
                                td(amount, align="center")
                if top30:
                    p()
                    with div(align="center"):
                        button(
                            "Expand",
                            cls="btn btn-primary",
                            type="button",
                            data_toggle="collapse",
                            data_target="#OtherFriends",
                        )
                    p()
                    with div(cls="collapse", id="OtherFriends", align="center"):
                        with table(style="table-layout: fixed; width: 300px"):
                            col(style="width: 10%", span="1")
                            col(style="width: 80%", span="1")
                            col(style="width: 10%", span="1")
                            for username, amount in top30.items():
                                with tr():
                                    i += 1
                                    td(i, align="center")
                                    td(
                                        a(username, href=f"/users/{username}"),
                                        align="center",
                                    )
                                    td(amount, align="center")
            if user_emotes := get_emotes_user(user):
                user_emotes = list(user_emotes.items())
                hr()
                p(b(a("Emote counts", href="/emotes")), align="center")
                emotes_by_7 = [{}]
                while len(user_emotes) > 0:
                    if len(emotes_by_7[-1]) == 7:
                        emotes_by_7.append({})
                    emote, amount = user_emotes.pop(0)
                    emotes_by_7[-1][emote] = amount
                with table(align="center"):
                    with tr():
                        for emote, amount in emotes_by_7[0].items():
                            with td(style="padding: 3px"):
                                emote_to_html(emote)
                                p(amount, align="center")
                if len(emotes_by_7) > 1:
                    with div(align="center"):
                        button(
                            "Expand",
                            cls="btn btn-primary",
                            type="button",
                            data_toggle="collapse",
                            data_target="#OtherEmotes",
                        )
                    br()
                    with div(cls="collapse", id="OtherEmotes"):
                        for emote_dict in emotes_by_7[1:]:
                            with table(align="center"):
                                with tr():
                                    for emote, amount in emote_dict.items():
                                        with td(style="padding: 3px"):
                                            emote_to_html(emote)
                                            p(amount, align="center")
            if tng_score := get_tng_score(user):
                hr()
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
