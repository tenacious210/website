import sqlite3
import json


def get_top_users():
    con = sqlite3.connect("dgg_stats.db")
    cur = con.cursor()
    top100_raw = cur.execute(
        "SELECT UserName, Amount FROM Lines ORDER BY Amount DESC LIMIT 101"
    )
    top100 = {u: a for u, a in top100_raw}
    top100.pop("_anon$")
    con.close()
    return top100


def get_lines(user: str):
    con = sqlite3.connect("dgg_stats.db")
    cur = con.cursor()
    params = {"user": user.lower()}
    lines = cur.execute(
        "SELECT Amount FROM Lines WHERE LOWER(UserName) = :user", params
    ).fetchall()
    con.close()
    return int(lines[0][0]) if lines else 0


def get_tng_score(user: str):
    con = sqlite3.connect("dgg_stats.db")
    cur = con.cursor()
    params = {"user": user.lower()}
    cmd = "SELECT Score FROM TngScore WHERE LOWER(UserName) = :user"
    tng_score = cur.execute(cmd, params).fetchall()
    con.close()
    return int(tng_score[0][0]) if tng_score else 0


def get_friends(user: str, amount):
    con = sqlite3.connect("dgg_stats.db")
    cur = con.cursor()
    params = {"user": user.lower()}
    cmd = "SELECT Mentions FROM UserMentions WHERE LOWER(UserName) = :user"
    mentions_raw = cur.execute(cmd, params).fetchall()
    mentions = {}
    if mentions_raw:
        mentions_unsorted = json.loads(mentions_raw[0][0])
        for k, v in sorted(mentions_unsorted.items(), key=lambda i: i[1], reverse=True):
            if len(mentions) < amount:
                if k not in ("Ban", "Subscriber", "_anon$"):
                    mentions[k] = v
            else:
                break
    con.close()
    return mentions
