from flask import Flask
from views import views
import os

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "8080")
    app.run(debug=False, port=server_port, host="0.0.0.0")
