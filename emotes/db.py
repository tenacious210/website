import sqlite3
import requests
from datetime import datetime, timedelta
from requests import JSONDecodeError
import json
from os import getenv

db_name = getenv("DGG_STATS_DB")

try:
    emote_json = requests.get("https://cdn.destiny.gg/emotes/emotes.json").json()
except JSONDecodeError:
    emote_json = {}

if emote_json:
    emotes = [e["prefix"] for e in emote_json]
else:
    emotes = []


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_emotes_user(username, number_of_days=30, amount=None):
    con = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cmd = "SELECT UserName FROM EmoteStats WHERE LOWER(UserName)=:user"
    params = {"user": username.lower()}
    target_day = datetime.today() - timedelta(days=number_of_days)
    if user_raw := cur.execute(cmd, params).fetchall():
        user = user_raw[0][0]
        sql_date = target_day.strftime("%Y-%m-%d")
        cmd = "SELECT * FROM EmoteStats WHERE UserName=:user AND Date>=DATE(:sql_date)"
        params = {"user": user, "sql_date": sql_date}
        emotes_by_day = cur.execute(cmd, params)
        fields = [f[0] for f in emotes_by_day.description]
        user_stats_unsorted = {f: 0 for f in fields}
        for day in emotes_by_day:
            i = 0
            for f in fields:
                if isinstance(day[i], int) and f in emotes:
                    user_stats_unsorted[f] += day[i]
                i += 1
        if not amount:
            amount = len(user_stats_unsorted)
        user_stats = {}
        for k, v in sorted(
            user_stats_unsorted.items(), key=lambda i: i[1], reverse=True
        ):
            if len(user_stats) < amount and v > 0:
                user_stats[k] = v
            else:
                break
    else:
        user_stats = None
    con.close()
    return user_stats


def get_emote_top_posters(emote, number_of_days=30, amount=100):
    con = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    if emote not in emotes:
        con.close()
        return None
    target_day = datetime.today() - timedelta(days=number_of_days)
    sql_date = target_day.strftime("%Y-%m-%d")
    cmd = (
        f"SELECT UserName,SUM({emote}) FROM EmoteStats "
        f"WHERE Date >= DATE('{sql_date}') AND {emote} > 0 "
        f"GROUP BY UserName ORDER BY SUM({emote}) DESC "
        f"LIMIT {amount}"
    )
    day_stats = cur.execute(cmd).fetchall()
    con.close()
    return {u: a for u, a in day_stats}


def get_emote_top5s(amount=None):
    con = sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    top5s_unsorted = {
        e: json.loads(t5)
        for e, t5 in cur.execute("SELECT * FROM TopPosters").fetchall()
    }
    top5s_values = {}
    for emote, top5 in top5s_unsorted.items():
        weight = 0
        for count in top5.values():
            weight += count
        top5s_values[emote] = weight
    top5s_by_value = [
        e[0] for e in reversed(sorted(top5s_values.items(), key=lambda i: i[1]))
    ]
    if amount:
        top5s = {}
        for e in top5s_by_value:
            top5s[e] = top5s_unsorted[e]
            if len(top5s) == amount:
                break
    else:
        top5s = {e: top5s_unsorted[e] for e in top5s_by_value}
    return top5s
