import sqlite3


def get_lines(user: str):
    con = sqlite3.connect("dgg_stats.db")
    cur = con.cursor()
    params = {"user": user.lower()}
    lines = cur.execute(
        "SELECT Amount FROM Lines WHERE LOWER(UserName) = :user", params
    ).fetchall()
    con.close()
    return int(lines[0][0]) if lines else None


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
