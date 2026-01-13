# run.py
import threading
import time
import webbrowser

from server import create_app
from face_auth import authenticate_user
from assistant import AryaAssistant

def main():
    print("🔒 Starting Face Authentication…")
    if not authenticate_user():
        print("❌ Access denied.")
        return
    print("✅ Face verified. Launching Arya…")

    app, socketio = create_app()
    

    # Simple endpoints for hologram toggle (assistant pings them too)
    @app.route("/holo/on")
    def holo_on():
        socketio.emit("holo", {"on": True})
        return "ok"

    @app.route("/holo/off")
    def holo_off():
        socketio.emit("holo", {"on": False})
        return "ok"

    # Start web server in a background thread
    def run_server():
        socketio.run(app, host="127.0.0.1", port=5000)

    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # Open dashboard
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

    # Start voice assistant
    assistant = AryaAssistant(socketio=socketio, base_url="http://127.0.0.1:5000")
    assistant.loop()

if __name__ == "__main__":
    main()
