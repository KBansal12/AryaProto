from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'arya-secret'
    CORS(app)  # Enable CORS for all routes
    
    # Configure SocketIO with better error handling
    socketio = SocketIO(
        app, 
        cors_allowed_origins="*", 
        async_mode="threading",
        logger=True,
        engineio_logger=True
    )

    @app.route("/")
    def index():
        try:
            logger.info("Serving index.html")
            return render_template("index.html")
        except Exception as e:
            logger.error(f"Error rendering index: {e}")
            return "Error loading page", 500

    @app.route("/health")
    def health():
        logger.debug("Health check requested")
        return jsonify({"status": "ok", "message": "Arya server is running"})

    # Handle socket connections
    @socketio.on("connect", namespace='/')
    def handle_connect():
        logger.info("Client connected")
        emit("status", {"text": "✅ Dashboard Ready — Waiting for voice commands…"})
        emit("log", {"who": "System", "text": "Client connected"})

    @socketio.on("disconnect", namespace='/')
    def handle_disconnect():
        logger.info("Client disconnected")

    # Handle custom events from clients
    @socketio.on("client_event", namespace='/')
    def handle_client_event(data):
        logger.info(f"Received client event: {data}")
        emit("log", {"who": "Client", "text": f"Sent: {data}"}, broadcast=True)

    # Broadcast holo state to frontend
    @socketio.on("holo", namespace='/')
    def handle_holo_event(data):
        try:
            logger.info(f"Holo event received: {data}")
            emit("holo", data, broadcast=True, namespace='/')
        except Exception as e:
            logger.error(f"Error handling holo event: {e}")

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    logger.info("Starting Arya server on port 5000")
    try:
        socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")