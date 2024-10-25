import bot

COMMANDS = {
    "leave": {
        "name": "leave",
        "description": "Close the program",
        "action": None
    },
    "auto xp": {
        "name": "auto xp",
        "description": "Run missions indefinitely by choosing the mission with the best xp/energy ratio",
        "action": bot.auto_xp
    }
}

def exists(command):
    for k in COMMANDS.keys():
        if command == k:
            return True
    return False

def run(command):
    COMMANDS[command]["action"]()