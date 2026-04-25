import os

from webex_bot.commands.echo import EchoCommand
from webex_bot.webex_bot import WebexBot

# Create a Bot Object
# TODO: fill approved_users list with all users in the database
bot = WebexBot(teams_bot_token=os.getenv("BOT_TOKEN"), approved_users=[])

# Add new commands for the bot to listen out for.
bot.add_command(EchoCommand())

# Call `run` for the bot to wait for incoming messages.
bot.run()