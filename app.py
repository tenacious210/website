from emote_grabber import update_emote_stats
from flask import Flask
from views import views
from time import sleep
import threading
import schedule
import os

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

schedule.every().day.at("12:00").do(update_emote_stats)


def update_stats():
    while True:
        schedule.run_pending()
        sleep(50)


if __name__ == "__main__":
    update_stats_thread = threading.Thread(target=update_stats, daemon=True)
    update_stats_thread.start()
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
