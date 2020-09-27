from flask import Blueprint, request, jsonify


SHUTDOWN_API = Blueprint("shutdown_api", __name__)

# ------------ SETUP VARIBLES -------------------


# ------------ CALLABLE API METHODS ----------------
#DELETE THIS
@SHUTDOWN_API.route("/shutdown", methods=["GET"])
def shutdown():
    shutdown_function = request.environ.get('werkzeug.server.shutdown')
    shutdown_function()
    return "Shutting down."