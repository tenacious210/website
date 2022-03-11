from datetime import timedelta, date
import requests
import sqlite3
import re

debug = False


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def update_emote_stats():
    emote_json = requests.get("https://cdn.destiny.gg/emotes/emotes.json").json()
    emotes = [e["prefix"] for e in emote_json]
    user_emotes = {}
    today = date.today()
    tomorrow = today + timedelta(days=1)
    thirty_days_ago = today - timedelta(days=30 if not debug else 2)
    for days in daterange(thirty_days_ago, tomorrow):
        year, month_num, month_name, day = days.strftime("%Y %m %B %d").split()
        rustle_url = f"https://dgg.overrustlelogs.net/Destinygg%20chatlog/{month_name}%20{year}/{year}-{month_num}-{day}.txt"
        print(f"Connecting to {rustle_url}")
        logs = requests.get(rustle_url).text.split("\n")
        for log in logs:
            if user_search := re.search(r"\[.*\] (\w*): ", log):
                user = user_search.group(1)
                if user not in user_emotes.keys():
                    user_emotes[user] = {emote: 0 for emote in emotes}
                for emote in emotes:
                    user_emotes[user][emote] += len(re.findall(rf"\b{emote}\b", log))
    emote_db_con = sqlite3.connect("user_emotes.db" if not debug else "test.db")
    # Will create the .db file if it doesn't exist
    emote_db_cur = emote_db_con.cursor()
    emote_db_cur.execute(
        "CREATE TABLE IF NOT EXISTS LastMonth (UserName STRING PRIMARY KEY NOT NULL UNIQUE)"
    )
    emote_db_cur.execute("DELETE FROM LastMonth")
    columns = [i[1] for i in emote_db_cur.execute("PRAGMA table_info(LastMonth)")]
    for emote in emotes:
        if emote not in columns:
            emote_db_cur.execute(f"ALTER TABLE LastMonth ADD {emote} INT")
    db_keys = f"`UserName`{''.join([f',`{emote_name}`' for emote_name in emotes])}"
    for username, emote_dict in user_emotes.items():
        db_values = f"'{username}'" + "".join(
            [f",'{emote_count}'" for emote_count in emote_dict.values()]
        )
        emote_db_cur.execute(f"INSERT INTO LastMonth ({db_keys}) VALUES ({db_values})")
    emote_db_con.commit()
    emote_db_con.close()
    print("Database updated successfully.")


if __name__ == "__main__":
    update_emote_stats()
