from dominate.tags import *
from .db import *
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
    with div(cls="container", align="center") as container:
        with table(style="table-layout: fixed; width: 250px"):
            col(style="width: 10%", span="1")
            col(style="width: 80%", span="1")
            col(style="width: 10%", span="1")
            with tr():
                for c in ("Rank", "User", "Level"):
                    td(b(c), align="center")
            i = 0
            for username, lines in top100.items():
                i += 1
                with tr():
                    td(b(i), align="center")
                    td(a(username, href=f"/users/{username}"), align="center")
                    td(calculate_level(lines)["level"], align="center")
    payload = render_template(
        "with_user_search.html",
        title="users",
        header=f"Top 100 users in DGG",
        content=container,
    )
    return payload


def users_api(user):
    if (lines := get_lines(user)) and match(r"^[\w]+$", user):
        user_stats = calculate_level(lines)
        user_stats["tng_score"] = get_tng_score(user)
        user_stats["best_friends"] = get_friends(user, amount=50)
        user_stats["bans"] = {str(k): v for k, v in get_bans(user).items()}
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
                    style=f"width: {user_level['progress']}%",
                    align="center",
                )
            p()
            h3(f"{user_level['xp']}/{user_level['xp_needed']} XP", align="center")
            h3(f"Level {user_level['level']}", align="center")
            p(f"Total lines: {lines}", align="center")
            if friends := get_friends(user, amount=25):
                hr()
                h3("Best friends", align="center")
                p()
                friend_index = tuple(friends.keys())
                top30 = None
                if len(friend_index) > 3:
                    top3 = {k: friends[k] for k in friend_index[:3]}
                    top30 = {k: friends[k] for k in friend_index[3:]}
                else:
                    top3 = {k: friends[k] for k in friend_index}
                with div(align="center"):
                    with table(cls="three-column"):
                        col(style="width: 20%", span="1")
                        col(style="width: 60%", span="1")
                        col(style="width: 20%", span="1")
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
                        with table(cls="three-column"):
                            col(style="width: 20%", span="1")
                            col(style="width: 60%", span="1")
                            col(style="width: 20%", span="1")
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
                h3(a("Emote counts", href="/emotes"), align="center")
                p()
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
            if bans := get_bans(user):
                hr()
                h3(f"Bans on record: {len(bans)}", align="center")
                p()
                ban_index = tuple(bans.keys())
                rest = None
                if len(ban_index) > 3:
                    most_recent = {k: bans[k] for k in ban_index[:3]}
                    rest = {k: bans[k] for k in ban_index[3:]}
                else:
                    most_recent = {k: bans[k] for k in ban_index}

                def expanding_ban_row(timestamp, ban_info, id):
                    if not (reason := ban_info.pop("reason")):
                        reason = ""
                    ctx_duration = ban_info["duration"]
                    if not ban_info["duration"]:
                        ctx_duration = ""
                        if ban_info["type"] in ("mute", "ban"):
                            ban_info["duration"] = "10m"
                        else:
                            ban_info["duration"] = "perma"
                    ctx_mod = ban_info["mod"]
                    if ban_info["mod"] == "RightToBearArmsLOL":
                        ban_info["mod"] = "RTBA"
                    date = timestamp.strftime("%Y-%m-%d")
                    time = timestamp.strftime("%H:%M:%S")
                    with tr() as row1:
                        td(
                            button(
                                "+",
                                cls="btn btn-default btn-sm btn-dark accordion-toggle",
                                data_toggle="collapse",
                                data_target=f"#ctx{i}",
                            ),
                            align="center",
                        )
                        td(f"{date}", align="center")
                        for info in ban_info.values():
                            td(str(info), align="center")
                    with tr() as row2:
                        with td(colspan="5", cls="hiddenRow"):
                            with div(
                                cls="accordian-body collapse",
                                id=f"ctx{i}",
                            ):
                                p()
                                ban_message = (
                                    f"[{time} UTC] {ctx_mod}: !{ban_info['type']} "
                                    f"{ctx_duration} {user} {reason}"
                                )
                                p(
                                    ban_message,
                                    align="left",
                                    style="padding-left: 20px",
                                )
                    return (row1, row2)

                with div(align="center"):
                    with table(cls="four-column"):
                        col(style="width: 10%", span="1")
                        col(style="width: 20%", span="2")
                        col(style="width: 10%", span="2")
                        with tr():
                            for c in ("Context", "Date", "Mod", "Type", "Duration"):
                                td(b(c), align="center")
                        i = 0
                        for timestamp, ban_info in most_recent.items():
                            i += 1
                            new_row = expanding_ban_row(timestamp, ban_info, i)
                            new_row[0]
                            new_row[1]
                    if rest:
                        p()
                        with div(align="center"):
                            button(
                                "Expand",
                                cls="btn btn-primary",
                                type="button",
                                data_toggle="collapse",
                                data_target="#OtherBans",
                            )
                        p()
                        with div(cls="collapse", id="OtherBans", align="center"):
                            with table(cls="four-column"):
                                col(style="width: 10%", span="1")
                                col(style="width: 20%", span="2")
                                col(style="width: 10%", span="2")
                                for timestamp, ban_info in rest.items():
                                    i += 1
                                    new_row = expanding_ban_row(timestamp, ban_info, i)
                                    new_row[0]
                                    new_row[1]
            br()

    else:
        container = p("Couldn't find that user", align="center")
    return render_template(
        "with_user_search.html",
        title="user",
        header=f"User stats for {user}",
        content=container,
    )
