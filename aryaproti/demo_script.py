import time
from assistant import AryaAssistant

def entrepreneurs_day_demo():
    assistant = AryaAssistant()
    
    # Welcome message
    assistant._say("Welcome to Arya Business Assistant demonstration for Entrepreneurs Day!")
    time.sleep(2)
    
    # Showcase features with pre-programmed commands
    demo_commands = [
        "Take note Arya is the best business assistant for entrepreneurs",
        "Add task Prepare for investor meeting high priority",
        "Add task Research market trends",
        "List tasks",
        "Schedule meeting Team sync tomorrow at 10 AM",
        "Research artificial intelligence in business",
        "Calculate fifteen times forty two plus eighteen",
        "What time is it",
        "Create presentation about our startup vision",
        "System report"
    ]
    
    for cmd in demo_commands:
        assistant._say(f"Demo command: {cmd}")
        assistant.handle(cmd)
        time.sleep(2)
    
    assistant._say("This concludes the Arya Business Assistant demonstration. Thank you!")

if __name__ == "__main__":
    entrepreneurs_day_demo()