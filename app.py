import os
from flask import Flask, send_from_directory, abort
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from FullDownloadHandler import FullDownloadHandler
from CleanupHandler import CleanupHandler
from WebhookHandler import WebHookHandler

app = Flask(__name__)

# Origin of your deployed frontend, e.g. https://7a7vm7kqewd7iojnfnnun8h0.kyuri.moe
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
CORS(app, origins=[FRONTEND_ORIGIN], supports_credentials=True)

# JWT secret now comes from an env var instead of AWS SSM (which required the
# original developer's own AWS account). Set JWT_SECRET_KEY in your deployment.
app.config["JWT_SECRET_KEY"] = os.environ["JWT_SECRET_KEY"]

jwt = JWTManager(app)

api = Api(app)
api.add_resource(FullDownloadHandler, "/handle_yt")
api.add_resource(CleanupHandler, "/cleanup")
api.add_resource(WebHookHandler, "/webhook")

AUDIO_PATH = "/audio"


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    """
    Replaces the nginx /audio/ location block: serves processed audio files
    as downloadable attachments. HOST_ENDPOINT (used by FullDownloadHandler
    to build the returned download URL) should point at this same app.
    """
    if not os.path.exists(os.path.join(AUDIO_PATH, filename)):
        abort(404)
    return send_from_directory(
        AUDIO_PATH,
        filename,
        as_attachment=True,
        mimetype="application/octet-stream",
    )
