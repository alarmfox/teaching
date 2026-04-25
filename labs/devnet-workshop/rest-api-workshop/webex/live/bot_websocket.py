import requests
from webex_bot.commands.echo import EchoCommand, Command
from webex_bot.webex_bot import WebexBot

access_token = "NTg0YzhhOWUtNzk2ZC00ZGZmLWIzYjItNGVkZThmMzE3YjQyNjJlNmVmYjItMGUw_PF84_9db17efa-dc2f-4ca3-90ae-30a52866391a"
# sanaza
access_token = "NzRmOWZhNWMtNTViYi00YWM3LTg2NzUtODI5N2Y2ZDRkYmEzODk0YzI1YmQtNWRi_P0A1_71b6b34c-abff-4407-ac50-5e62323aed80"
# giuseppe@capass.org
access_token = "YWJmNTNjNGMtMWIzNC00YzRiLWIzMWUtODljN2YzMmE3YTc3ZDY5NDgyNDYtMjVj_PE93_dd712212-d424-458d-8970-a5d6debea706"
# luca comentale
access_token = "NTcxNDFjZmQtNTcwNS00YjhkLWI0N2EtZTE3ZjFhNzQzNGU5NWI0YTc3YWUtZGIy_P0A1_bbd62b13-3612-4c34-8eff-7f35cdce90eb"

scan_card = {
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2",
    "body": [
        {
            "type": "TextBlock",
            "text": "Enter the IP address to scan:",
            "wrap": True,
        },
        {
            "type": "Input.Text",
            "id": "ipAddress",
            "placeholder": "e.g. 192.168.1.1",
        },
    ],
    "actions": [{"type": "Action.Submit", "title": "Scan"}],
}


class CatFact(Command):
    def __init__(self):
        super().__init__(
            command_keyword="cat-fact",
            help_message="Get a random cat fact",
            card=None,
        )

    def execute(self, message, attachment_actions, activity):
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()
        json_data = response.json()

        return json_data["fact"]


class Scan(Command):
    def __init__(self):
        super().__init__(
            command_keyword="scan",
            help_message="Perform scan on a single host or a network",
            card=scan_card,
        )

    def execute(self, message, attachment_actions, activity):
        # Extract the IP address from the card input
        ip_address = attachment_actions.inputs.get("ipAddress", "unknown")

        # Fake a response as if nmap was executed
        fake_nmap_response = (
            f"Scanning IP: {ip_address}\nPort 22: Open\nPort 80: Open\nPort 443: Closed"
        )

        return fake_nmap_response


# Create a Bot Object
# TODO: fill approved_users list with all users in the database
bot = WebexBot(
    teams_bot_token=access_token,
)

# Add new commands for the bot to listen out for.
bot.add_command(EchoCommand())
bot.add_command(CatFact())
bot.add_command(Scan())

# Call `run` for the bot to wait for incoming messages.
bot.run()
