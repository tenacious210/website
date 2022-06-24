import sqlite3
from datetime import datetime, timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_emotes_user(username, number_of_days=30):
    con = sqlite3.connect("emote_stats.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cmd = f"SELECT UserName FROM EmoteStats WHERE LOWER(UserName)='{username.lower()}'"
    target_day = datetime.today() - timedelta(days=number_of_days)
    if user_raw := cur.execute(cmd):
        user = user_raw.fetchall()[0][0]
        sql_date = target_day.strftime("%Y-%m-%d")
        cmd = (
            f"SELECT * FROM EmoteStats WHERE UserName='{user}' "
            f"AND Date>=DATE('{sql_date}')"
        )
        emotes_by_day = cur.execute(cmd)
        fields = [f[0] for f in emotes_by_day.description]
        user_stats_unsorted = {f: 0 for f in fields}
        for day in emotes_by_day:
            i = 0
            for f in fields:
                if f not in ("UserName", "Date"):
                    user_stats_unsorted[f] += day[i]
                i += 1
        user_stats_unsorted.pop("UserName")
        user_stats_unsorted.pop("Date")
        user_stats = {
            k: v
            for k, v in sorted(
                user_stats_unsorted.items(), key=lambda i: i[1], reverse=True
            )
        }
    else:
        user_stats = None
    con.close()
    return user_stats


def get_emote_top_posters(emote, ranks=100, number_of_days=30):
    con = sqlite3.connect("emote_stats.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    emotes = [i[1] for i in cur.execute("PRAGMA table_info(EmoteStats)")][2:]
    if emote not in emotes:
        con.close()
        return None
    target_day = datetime.today() - timedelta(days=number_of_days)
    sql_date = target_day.strftime("%Y-%m-%d")
    cmd = (
        f"SELECT UserName,{emote} FROM EmoteStats "
        f"WHERE Date>DATE('{sql_date}') AND {emote}>0"
    )
    day_stats = cur.execute(cmd)
    stats_unsorted = {}
    for username, amount in day_stats:
        if username not in stats_unsorted.keys():
            stats_unsorted[username] = 0
        stats_unsorted[username] += amount
    top_posters = {}
    for k, v in sorted(stats_unsorted.items(), key=lambda i: i[1], reverse=True):
        if len(top_posters) < ranks:
            top_posters[k] = v
        else:
            break
    con.close()
    return top_posters


def get_emote_top5s(number_of_days=30):
    con = sqlite3.connect("emote_stats.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    emotes = [i[1] for i in cur.execute("PRAGMA table_info(EmoteStats)")][2:]
    top5s_unsorted = {}
    for emote in emotes:
        top5 = get_emote_top_posters(emote, ranks=5, number_of_days=number_of_days)
        top5s_unsorted[emote] = top5
    top5s_values = {}
    for emote, top5 in top5s_unsorted.items():
        weight = 0
        for count in top5.values():
            weight += count
        top5s_values[emote] = weight
    top5s_by_value = [
        e[0] for e in reversed(sorted(top5s_values.items(), key=lambda i: i[1]))
    ]
    con.close()
    return {e: top5s_unsorted[e] for e in top5s_by_value}
