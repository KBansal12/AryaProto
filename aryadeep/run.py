import threading
import time
import webbrowser
from server import create_app
# from face_auth import authenticate_user  # Commented out for testing
from assistant import AryaAssistant
import sys

def main():
    print("🔒 Starting Face Authentication…")
    # Temporarily disable face auth for testing
    # if not authenticate_user():
    #     print("❌ Access denied.")
    #     return
    print("✅ Face verified. Launching Arya…")

    app, socketio = create_app()
    
    # Simple endpoints for hologram toggle (assistant pings them too)
    @app.route("/holo/on")
    def holo_on():
        socketio.emit("holo", {"on": True}, namespace='/')
        return "ok"

    @app.route("/holo/off")
    def holo_off():
        socketio.emit("holo", {"on": False}, namespace='/')
        return "ok"

    # Start web server in a background thread
    def run_server():
        print("Starting server on port 5000...")
        socketio.run(app, host="127.0.0.1", port=5000, debug=False, use_reloader=False)

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = False  # Changed to False to keep thread alive
    server_thread.start()

    # Wait a moment for server to start
    time.sleep(3)
    
    # Open dashboard
    try:
        webbrowser.open("http://127.0.0.1:5000")
    except Exception as e:
        print(f"Could not open browser: {e}")

    # Start voice assistant
    try:
        assistant = AryaAssistant(socketio=socketio, base_url="http://127.0.0.1:5000")
        print("Assistant created. Starting loop...")
        assistant.loop()
    except Exception as e:
        print(f"Error in assistant: {e}")
        import traceback
        traceback.print_exc()

    # Keep the main thread alive
    print("Main thread waiting...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()