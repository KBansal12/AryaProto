from flask import Flask, render_template, request, jsonify
from openchat import OpenChat  # Correct class name
import pyttsx3

app = Flask(__name__)
bot = OpenChat(model="blender.medium", device="cpu", method="top_k", top_k=20)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    response = bot.chat(inputs={"text": user_msg})  # Depends on method
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
