from emote_grabber import update_emote_stats
from datetime import date, timedelta
from flask import Flask
from views import views
from time import sleep
import threading
import os

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


def update_stats():
    while True:
        try:
            with open("lastupdate.txt", "r") as lutxt:
                lutxt_content = lutxt.read()
        except FileNotFoundError:
            with open("lastupdate.txt", "w") as lutxt:
                lutxt_content = ""
        date_str = lutxt_content if lutxt_content.count("-") == 2 else "2020-01-01"
        year, month, day = [int(n) for n in date_str.split("-")]
        lastupdate = date(year, month, day)
        today = date.today()
        if today - lastupdate != timedelta(0):
            update_emote_stats()
            with open("lastupdate.txt", "w") as lutxt:
                lutxt.write(str(today))
        sleep(600)


if __name__ == "__main__":
    update_stats_thread = threading.Thread(target=update_stats)
    update_stats_thread.start()
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
