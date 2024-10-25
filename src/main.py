import commands
import bot

user_input = input("Enter a command")
while user_input != commands.COMMANDS["leave"]["name"]:
    if commands.exists(user_input):
        commands.run(user_input)
    else:
        print(f"The command '{user_input}' does not exist please enter a valid command")
    user_input = input("Enter a command")

print("Closing the program")