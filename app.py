from google.cloud import storage
from datetime import datetime
from flask import Flask
from views import views
import os


def download_latest_db():
    db_name = os.getenv("DGG_STATS_DB")
    storage_client = storage.Client()
    storage_bucket = storage_client.bucket("tenadev")
    blob = storage_bucket.blob(f"website/{db_name}")
    blob.download_to_filename(db_name)
    print(f"Downloaded latest database at {datetime.now()}")


if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(views, url_prefix="/")
    app.config["JSON_SORT_KEYS"] = False
    download_latest_db()
    app.run(debug=False, port=os.environ.get("PORT", "8080"), host="0.0.0.0")
    # app.run(debug=True)
