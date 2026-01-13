import os
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import requests
import json
import time
import subprocess
import pyautogui
import wikipedia
import wolframalpha
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import calendar
import pyperclip
import psutil
import screeninfo
import keyboard
import openai
from state_manager import state_manager
import os
# ---------- Configuration ----------

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WOLFRAM_ALPHA_APP_ID = "YOUR_WOLFRAM_ALPHA_APP_ID"  # Get from https://products.wolframalpha.com/api/

# Email configuration (for sending reports/emails)
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email": "khushboobansal792@gmail.com",
    "password": "your_app_password"  # Use app-specific password
}

# ---------- Enhanced OpenAI chat ----------
def chat_with_arya(prompt: str) -> str:
    if not OPENAI_KEY:
        return "I don't have cloud access right now, but I'm online and ready."
    try:
        openai.api_key =OPENAI_KEY
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"I couldn't reach my language model: {e}"

# ---------- Business Automation Functions ----------
class BusinessAutomation:
    def __init__(self, socketio=None):
        self.socketio = socketio
        self.notes_file = "arya_notes.txt"
        self.tasks_file = "arya_tasks.json"
        self.meetings_file = "arya_meetings.json"
        self._load_data()
    
    def _emit(self, event, data):
        try:
            if self.socketio:
                self.socketio.emit(event, data, namespace='/')
        except Exception as e:
            print(f"Emit error: {e}")
    
    def _load_data(self):
        # Load tasks
        try:
            with open(self.tasks_file, 'r') as f:
                self.tasks = json.load(f)
        except:
            self.tasks = []
        
        # Load meetings
        try:
            with open(self.meetings_file, 'r') as f:
                self.meetings = json.load(f)
        except:
            self.meetings = []
    
    def _save_data(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f)
        with open(self.meetings_file, 'w') as f:
            json.dump(self.meetings, f)
    
    def take_note(self, note_text):
        """Save a note to file"""
        try:
            with open(self.notes_file, 'a') as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {note_text}\n")
            return f"Note saved: {note_text}"
        except Exception as e:
            return f"Failed to save note: {e}"
    
    def add_task(self, task_description, priority="medium"):
        """Add a new task to the task list"""
        task = {
            "id": len(self.tasks) + 1,
            "description": task_description,
            "priority": priority,
            "completed": False,
            "created": datetime.datetime.now().isoformat()
        }
        self.tasks.append(task)
        self._save_data()
        return f"Task added: {task_description} (Priority: {priority})"
    
    def list_tasks(self):
        """List all tasks"""
        if not self.tasks:
            return "You have no tasks."
        
        response = "Your tasks:\n"
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task["completed"] else "○"
            response += f"{i}. [{status}] {task['description']} (Priority: {task['priority']})\n"
        
        return response
    
    def complete_task(self, task_number):
        """Mark a task as completed"""
        try:
            task_index = int(task_number) - 1
            if 0 <= task_index < len(self.tasks):
                self.tasks[task_index]["completed"] = True
                self._save_data()
                return f"Task marked as completed: {self.tasks[task_index]['description']}"
            else:
                return "Invalid task number."
        except:
            return "Please specify a valid task number."
    
    def schedule_meeting(self, title, date_str, time_str, participants=None):
        """Schedule a new meeting"""
        try:
            # Parse date and time
            meeting_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            
            meeting = {
                "id": len(self.meetings) + 1,
                "title": title,
                "datetime": meeting_datetime.isoformat(),
                "participants": participants or [],
                "created": datetime.datetime.now().isoformat()
            }
            
            self.meetings.append(meeting)
            self._save_data()
            
            # Create calendar event (Windows)
            try:
                # This creates an Outlook calendar event on Windows
                os.system(f'powershell "Add-Appointment -Subject \'{title}\' -Start \'{meeting_datetime}\' -Duration 60"')
            except:
                pass
            
            return f"Meeting scheduled: {title} on {date_str} at {time_str}"
        except Exception as e:
            return f"Failed to schedule meeting: {e}"
    
    def list_meetings(self):
        """List all upcoming meetings"""
        if not self.meetings:
            return "You have no scheduled meetings."
        
        # Sort meetings by datetime
        sorted_meetings = sorted(self.meetings, key=lambda x: x["datetime"])
        
        response = "Your upcoming meetings:\n"
        for i, meeting in enumerate(sorted_meetings, 1):
            meeting_time = datetime.datetime.fromisoformat(meeting["datetime"])
            response += f"{i}. {meeting['title']} - {meeting_time.strftime('%Y-%m-%d %H:%M')}\n"
        
        return response
    
    def send_email(self, recipient, subject, body):
        """Send an email using SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG["email"]
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
            server.starttls()
            server.login(EMAIL_CONFIG["email"], EMAIL_CONFIG["password"])
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG["email"], recipient, text)
            server.quit()
            
            return f"Email sent to {recipient} with subject: {subject}"
        except Exception as e:
            return f"Failed to send email: {e}"
    
    def create_presentation(self, topic):
        """Create a PowerPoint presentation with the given topic"""
        try:
            # This would use python-pptx in a real implementation
            # For demo purposes, we'll just open PowerPoint
            os.system("start powerpnt")
            time.sleep(3)  # Wait for PowerPoint to open
            
            # Create a new presentation (simulated)
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1)
            
            # Add title slide
            pyautogui.click(500, 300)  # Click on title placeholder
            pyautogui.write(topic, interval=0.1)
            
            return f"Created a presentation about {topic}"
        except Exception as e:
            return f"Failed to create presentation: {e}"
    
    def system_report(self):
        """Generate a system status report"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # Battery status (if available)
            try:
                battery = psutil.sensors_battery()
                battery_percent = battery.percent if battery else "N/A"
                plugged = battery.power_plugged if battery else "N/A"
            except:
                battery_percent = "N/A"
                plugged = "N/A"
            
            report = f"""
System Report:
- CPU Usage: {cpu_usage}%
- Memory Usage: {memory_usage}%
- Disk Usage: {disk_usage}%
- Battery: {battery_percent}% ({'Charging' if plugged else 'On battery' if battery_percent != 'N/A' else 'N/A'})
"""
            return report
        except Exception as e:
            return f"Failed to generate system report: {e}"
    
    def research_topic(self, topic):
        """Research a topic using Wikipedia and web search"""
        try:
            # Try Wikipedia first
            try:
                wiki_summary = wikipedia.summary(topic, sentences=2)
                response = f"According to Wikipedia: {wiki_summary}\n\n"
            except:
                response = f"Information about {topic} from Wikipedia wasn't available.\n\n"
            
            # Open web search
            webbrowser.open(f"https://www.google.com/search?q={topic}")
            
            return response + f"I've opened a web search for {topic}."
        except Exception as e:
            return f"Failed to research topic: {e}"
    
    def calculate(self, expression):
        """Calculate mathematical expressions using Wolfram Alpha"""
        try:
            client = wolframalpha.Client(WOLFRAM_ALPHA_APP_ID)
            res = client.query(expression)
            answer = next(res.results).text
            return f"The answer is: {answer}"
        except:
            # Fallback to eval for simple expressions (with safety checks)
            try:
                # Remove any potentially dangerous characters
                safe_expression = ''.join(c for c in expression if c in '0123456789+-*/(). ')
                result = eval(safe_expression)
                return f"The answer is: {result}"
            except:
                return "I couldn't calculate that expression."
# Add this to your assistant.py or create a new file interruption_listener.py

import threading
from speech_recognition import Recognizer, Microphone
from state_manager import state_manager

class InterruptionListener:
    def __init__(self, assistant):
        self.assistant = assistant
        self.recognizer = Recognizer()
        self.is_listening = False
        self.listening_thread = None
        
    def start_listening(self):
        self.is_listening = True
        self.listening_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listening_thread.start()
        
    def stop_listening(self):
        self.is_listening = False
        if self.listening_thread:
            self.listening_thread.join(timeout=1)
            
    def _listen_loop(self):
        interruption_commands = ["stop", "cancel", "never mind", "abort", "enough"]
        
        with Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while self.is_listening:
                try:
                    # Listen for interruption commands with a short timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    # Check if any interruption command was said
                    if any(cmd in text for cmd in interruption_commands):
                        if state_manager.request_interrupt():
                            self.assistant._emit("log", {"who": "System", "text": "Interruption detected! Cancelling operation."})
                            self.assistant._emit("status", {"text": "Operation cancelled"})
                            
                except Exception:
                    # Timeout or other error, just continue listening
                    pass
# ---------- Enhanced Voice Assistant ----------
class AryaAssistant:
    def __init__(self, socketio=None, base_url="http://127.0.0.1:5000"):
        self.socketio = socketio
        self.base_url = base_url
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[1].id)  # Female voice
        self.automation = BusinessAutomation(socketio)
        self._say("Arya Business Assistant is online. I'm ready to help with your entrepreneurial tasks.")

    def _emit(self, event, data):
        try:
            if self.socketio:
                self.socketio.emit(event, data, namespace='/')
        except Exception as e:
            print(f"Emit error: {e}")
    def _say(self, text, interruptable=True):
        if interruptable and state_manager.should_interrupt():
            print("Interrupted during speech")
            return False
    def _say(self, text):
        print(f"Arya: {text}")
        self._emit("log", {"who": "Arya", "text": text})
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")

    def listen_once(self, timeout=6) -> str:
        if state_manager.should_interrupt():
            return ""
            
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self._emit("status", {"text": "🎤 Listening..."})
            r.adjust_for_ambient_noise(source, duration=0.4)
            try:
                audio = r.listen(source, phrase_time_limit=timeout, timeout=timeout)
            except sr.WaitTimeoutError:
                return ""
                
        try:
            q = r.recognize_google(audio, language="en-IN").lower()
            self._emit("log", {"who": "You", "text": q})
            if any(cmd in q for cmd in ["stop", "cancel", "never mind", "abort"]):
                if state_manager.request_interrupt():
                    self._emit("log", {"who": "System", "text": "Operation cancelled"})
                    self._emit("status", {"text": "Operation cancelled"})
                return ""
                
            return q
        except Exception as e:
            self._emit("log", {"who": "System", "text": "Sorry, I didn't catch that."})
            print(f"Recognition error: {e}")
            return ""
    def handle_long_running_operation(self, operation_name, operation_func, *args, **kwargs):
        """Helper method for operations that can be interrupted"""
        state_manager.set_current_operation(operation_name)
        try:
            result = operation_func(*args, **kwargs)
            if state_manager.should_interrupt():
                self._emit("log", {"who": "System", "text": f"{operation_name} was cancelled"})
                return None
            return result
        finally:
            state_manager.clear_current_operation()
    def research_with_interruption(self, topic):
        def research_operation():
            self._say(f"Researching {topic}, please wait...")
            
            # Simulate research time
            for i in range(5):
                if state_manager.should_interrupt():
                    return None
                time.sleep(1)
                self._emit("status", {"text": f"Researching... {i+1}/5"})
            
            # Try Wikipedia
            try:
                import wikipedia
                wiki_summary = wikipedia.summary(topic, sentences=2)
                result = f"According to Wikipedia: {wiki_summary}"
            except:
                result = f"Research completed on {topic}"
            
            # Open web search
            if not state_manager.should_interrupt():
                webbrowser.open(f"https://www.google.com/search?q={topic}")
            
            return result
        
        return self.handle_long_running_operation(f"Research: {topic}", research_operation)

    def handle(self, command: str) -> bool:
        if not command: 
            return True
            
        # Check for interruption commands first
        if any(cmd in command for cmd in ["stop", "cancel", "never mind", "abort"]):
            if state_manager.request_interrupt():
                self._emit("log", {"who": "System", "text": "Operation cancelled"})
                self._emit("status", {"text": "Operation cancelled"})
            return True

        # --- Notes and Tasks ---
        if command.startswith("note ") or command.startswith("take note "):
            note_text = command.replace("note", "", 1).replace("take", "", 1).strip()
            response = self.automation.take_note(note_text)
            self._say(response)
            return True

        if command.startswith("add task "):
            task_text = command.replace("add task", "", 1).strip()
            # Check for priority
            priority = "medium"
            if " high priority" in task_text:
                priority = "high"
                task_text = task_text.replace(" high priority", "")
            elif " low priority" in task_text:
                priority = "low"
                task_text = task_text.replace(" low priority", "")
                
            response = self.automation.add_task(task_text, priority)
            self._say(response)
            return True

        if "list tasks" in command or "show tasks" in command:
            response = self.automation.list_tasks()
            self._say(response)
            return True

        if command.startswith("complete task "):
            task_num = command.replace("complete task", "", 1).strip()
            response = self.automation.complete_task(task_num)
            self._say(response)
            return True

        # --- Meetings and Scheduling ---
        if command.startswith("schedule meeting "):
            # This would parse date/time in a real implementation
            meeting_info = command.replace("schedule meeting", "", 1).strip()
            # Simple implementation - just use current time + 1 hour
            now = datetime.datetime.now()
            meeting_time = (now + datetime.timedelta(hours=1)).strftime("%H:%M")
            meeting_date = now.strftime("%Y-%m-%d")
            response = self.automation.schedule_meeting(meeting_info, meeting_date, meeting_time)
            self._say(response)
            return True

        if "list meetings" in command or "show meetings" in command:
            response = self.automation.list_meetings()
            self._say(response)
            return True

        # --- Email ---
        if command.startswith("send email to "):
            # Simplified email sending
            # In a real implementation, you'd parse recipient, subject, and body
            email_parts = command.replace("send email to", "", 1).strip().split(" about ")
            if len(email_parts) >= 2:
                recipient = email_parts[0].strip()
                subject = email_parts[1].strip()
                body = f"Email sent by Arya Assistant on {datetime.datetime.now().strftime('%Y-%m-%d')}"
                response = self.automation.send_email(recipient, subject, body)
                self._say(response)
            else:
                self._say("Please specify both recipient and subject for the email.")
            return True

        # --- Presentations ---
        if command.startswith("create presentation about "):
            topic = command.replace("create presentation about", "", 1).strip()
            response = self.automation.create_presentation(topic)
            self._say(response)
            return True

        # --- System and Reports ---
        if "system report" in command or "system status" in command:
            response = self.automation.system_report()
            self._say(response)
            return True

        # --- Research ---
        if command.startswith("research "):
            topic = command.replace("research", "", 1).strip()
            response = self.automation.research_topic(topic)
            self._say(response)
            return True

        # --- Calculations ---
        if command.startswith("calculate "):
            expression = command.replace("calculate", "", 1).strip()
            response = self.automation.calculate(expression)
            self._say(response)
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
        if "activate hologram" in command or "hologram mode" in command:
            self._say("Activating holographic interface.")
            self._emit("holo", {"on": True})
            try: 
                requests.get(self.base_url + "/holo/on", timeout=1)
            except Exception as e:
                print(f"Hologram request error: {e}")
            return True

        if "deactivate hologram" in command or "hologram off" in command:
            self._say("Deactivating hologram.")
            self._emit("holo", {"on": False})
            try: 
                requests.get(self.base_url + "/holo/off", timeout=1)
            except Exception as e:
                print(f"Hologram request error: {e}")
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