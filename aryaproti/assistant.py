# assistant.py
import os
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import requests

# ---------- Optional OpenAI chat ----------

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
def chat_with_arya(prompt: str) -> str:
    if not OPENAI_KEY:
        return "I don't have cloud access right now, but I’m online and ready."
    try:
        import openai
        openai.api_key = OPENAI_KEY
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"I couldn't reach my language model: {e}"

# ---------- Voice Assistant ----------
class AryaAssistant:
    def __init__(self, socketio=None, base_url="http://127.0.0.1:5000"):
        self.socketio = socketio
        self.base_url = base_url
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)
        self._say("Arya is online. Try: 'open notepad', 'search AI future', 'what time is it', 'activate hologram', 'lockdown', or just talk to me.'")

    def _emit(self, event, data):
        try:
            if self.socketio: self.socketio.emit(event, data)
        except Exception:
            pass

    def _say(self, text):
        print(f"Arya: {text}")
        self._emit("log", {"who": "Arya", "text": text})
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass

    def listen_once(self) -> str:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self._emit("status", {"text": "🎤 Listening..."})
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source, phrase_time_limit=6)
        try:
            q = r.recognize_google(audio, language="en-IN").lower()
            self._emit("log", {"who":"You","text": q})
            return q
        except Exception:
            self._emit("log", {"who":"System","text":"Sorry, I didn't catch that."})
            return ""

    def handle(self, command: str) -> bool:
        if not command: 
            return True

        # --- Open apps ---
        if "open notepad" in command:
            self._say("Opening Notepad")
            os.system("notepad")
            return True

        if "open calculator" in command or "open calc" in command:
            self._say("Opening Calculator")
            os.system("calc")
            return True

        if command.startswith("open "):
            app = command.replace("open", "", 1).strip()
            self._say(f"Trying to open {app}")
            os.system(f"start {app}")
            return True

        # --- Search ---
        if command.startswith("search "):
            query = command.replace("search", "", 1).strip()
            self._say(f"Searching {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return True

        # --- Time ---
        if "what time is it" in command or command.strip() == "time" or "time now" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self._say(f"The time is {now}.")
            return True

        # --- Hologram UI toggle ---
        def _say(self, text):
                print("Arya:", text)   # still print to terminal
                socketio.emit("log", {"who": "Arya", "text": text}) 
        def _emit(self, channel, data):
                socketio.emit(channel, data)
        def handle_command(self, command):
            if "activate hologram" in command or "hologram mode" in command:
                self._say("Activating holographic interface.")
            
                self._emit("holo", {"on": True})
                try: requests.get(self.base_url + "/holo/on", timeout=1)
                except: pass
                return True

            if "deactivate hologram" in command or "hologram off" in command:
                self._say("Deactivating hologram.")
                self._emit("holo", {"on": False})
                try: requests.get(self.base_url + "/holo/off", timeout=1)
                except: pass
                return True

        # --- Emergency Lockdown (Windows) ---
        if "lockdown" in command or "emergency lockdown" in command:
            self._say("Initiating emergency lockdown.")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return True

        # --- Exit ---
        if command in ("exit", "quit", "shutdown arya") or "exit" in command:
            self._say("Goodbye. Shutting down Arya.")
            return False

        # --- Fallback: Chat ---
        answer = chat_with_arya(command)
        self._say(answer)
        return True

    def loop(self):
        running = True
        while running:
            cmd = self.listen_once()
            running = self.handle(cmd)
