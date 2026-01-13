# server.py
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'arya-secret'
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # Broadcast holo state to frontend
    @socketio.on("holo")
    def handle_holo_event(data):
        emit("holo", data, broadcast=True)

    return app, socketio


if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
