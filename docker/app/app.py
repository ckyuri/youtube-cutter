import os
from flask import Flask, send_from_directory, abort, render_template
from flask_restful import Api

from FullDownloadHandler import FullDownloadHandler
from CleanupHandler import CleanupHandler
from WebhookHandler import WebHookHandler

app = Flask(
    __name__,
    template_folder="frontend/dist",
    static_folder="frontend/dist/assets",
)

api = Api(app)
api.add_resource(FullDownloadHandler, "/handle_yt")
api.add_resource(CleanupHandler, "/cleanup")
api.add_resource(WebHookHandler, "/webhook")

AUDIO_PATH = "/audio"


@app.route("/")
def serve():
    return render_template("index.html")


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    """Serves processed audio files as downloadable attachments."""
    if not os.path.exists(os.path.join(AUDIO_PATH, filename)):
        abort(404)
    return send_from_directory(
        AUDIO_PATH,
        filename,
        as_attachment=True,
        mimetype="application/octet-stream",
    )
