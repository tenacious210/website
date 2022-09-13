from datetime import datetime
import sqlite3
import json
import re
from os import getenv

db_name = getenv("DGG_STATS_DB")


def get_top_users():
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    top100_raw = cur.execute(
        "SELECT UserName, Amount FROM Lines ORDER BY Amount DESC LIMIT 101"
    )
    top100 = {u: a for u, a in top100_raw}
    if "_anon$" in top100.keys():
        top100.pop("_anon$")
    con.close()
    return top100


def get_lines(user: str):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    params = {"user": user.lower()}
    cmd = "SELECT Amount FROM Lines WHERE LOWER(UserName) = :user"
    lines = cur.execute(cmd, params).fetchall()
    con.close()
    return int(lines[0][0]) if lines else 0


def get_tng_score(user: str):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    params = {"user": user.lower()}
    cmd = "SELECT Score FROM TngScore WHERE LOWER(UserName) = :user"
    tng_score = cur.execute(cmd, params).fetchall()
    con.close()
    return int(tng_score[0][0]) if tng_score else 0


def get_friends(user: str, amount=None):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    params = {"user": user.lower()}
    cmd = "SELECT Mentions FROM UserMentions WHERE LOWER(UserName) = :user"
    mentions_raw = cur.execute(cmd, params).fetchall()
    mentions = {}
    if mentions_raw:
        mentions_unsorted = json.loads(mentions_raw[0][0])
        if not amount:
            amount = len(mentions_unsorted)
        for k, v in sorted(mentions_unsorted.items(), key=lambda i: i[1], reverse=True):
            if len(mentions) < amount:
                if k not in ("Ban", "Subscriber", "_anon$"):
                    mentions[k] = v
            else:
                break
    con.close()
    return mentions


def get_bans(user: str, amount=None):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    params = {"user": user.lower()}
    cmd = "SELECT Bans FROM UserBans WHERE LOWER(UserName) = :user"
    bans_raw = cur.execute(cmd, params).fetchall()
    bans = {}
    if bans_raw:
        bans_raw = json.loads(bans_raw[0][0])
        bans_by_date_unsorted = {}
        for ban in bans_raw:
            date_strings = re.split(r"-| |:", ban.pop("timestamp"))
            date_strings.remove("UTC")
            if len(date_strings) > 6:
                continue
            date_strings = [int(i) for i in date_strings]
            bans_by_date_unsorted[datetime(*date_strings)] = ban
        if not amount:
            amount = len(bans_by_date_unsorted)
        for d in sorted(bans_by_date_unsorted.keys(), reverse=True):
            if len(bans) < amount:
                bans[d] = bans_by_date_unsorted[d]
            else:
                break
    con.close()
    return bans


if __name__ == "__main__":
    print(get_bans("Destiny", amount=3))
