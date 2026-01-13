from flask import Flask, render_template, request, jsonify
from assistant import chat_with_arya

app = Flask(__name__)
socketio = SocketIO(app)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = chat_with_arya(user_input)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)

