from google.cloud import storage
from flask import Flask
from views import views
import os

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.config["JSON_SORT_KEYS"] = False


if __name__ == "__main__":
    storage_client = storage.Client()
    storage_bucket = storage_client.bucket("tenadev")
    blob = storage_bucket.blob("emote_stats.db")
    blob.download_to_filename("emote_stats.db")
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
