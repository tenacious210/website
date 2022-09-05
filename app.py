from google.cloud import storage
from schedule import every, repeat, run_pending
from threading import Thread
from time import sleep
from flask import Flask
from views import views
import os


@repeat(every().day.at("00:10"))
def download_latest_db():
    storage_client = storage.Client()
    storage_bucket = storage_client.bucket("tenadev")
    blob = storage_bucket.blob("dgg_stats.db")
    blob.download_to_filename("dgg_stats.db")


def run_scheduled():
    run_pending()
    sleep(60)


app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.config["JSON_SORT_KEYS"] = False


if __name__ == "__main__":
    download_latest_db()
    download_db_thread = Thread(target=run_scheduled)
    download_db_thread.start()
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
