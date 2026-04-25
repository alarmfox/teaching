import sys
import tempfile
import requests
from flask import Flask, request
from webexpythonsdk import WebexAPI, ApiError
from webexpythonsdk.models.cards import AdaptiveCard
from webexpythonsdk.models.cards.inputs import Text
from webexpythonsdk.models.cards.card_elements import TextBlock
from webexpythonsdk.models.cards.actions import Submit

# Access token for authenticating with the Webex API
access_token = ""

# Check if the access token is provided
if access_token is None:
    print("Missing access token")
    sys.exit(1)

# Initialize the Webex API client with the access token
api = WebexAPI(access_token=access_token)

# retrieve bot details like email ecc
bot_info = api.people.me()

# Define an adaptive card for scanning IP addresses
scan_card = AdaptiveCard(
    body=[
        TextBlock(text="Enter the IP address to scan", wrap=True),
        Text(id="ipAddress", placeholder="e.g. 192.168.1.1"),
    ],
    actions=[Submit(title="Scan")],
)

# Create a Flask application instance
app = Flask(__name__)


# Function to get the public URL from ngrok
# Ngrok is used to expose the local server to the internet
def get_public_url() -> str:
    # Send a GET request to the ngrok API to retrieve tunnel information
    res = requests.get("http://localhost:4040/api/tunnels")
    res.raise_for_status()  # Raise an error if the request was unsuccessful
    tunnels = res.json()  # Parse the JSON response
    return tunnels["tunnels"][0][
        "public_url"
    ]  # Return the public URL of the first tunnel


# Function to create a webhook in Webex
# Webhooks allow the bot to receive events from Webex, such as new messages
def create_webhook(
    public_url: str, name: str, resource: str, event: str = "created"
) -> None:
    try:
        # Attempt to create a new webhook with the specified parameters
        api.webhooks.create(
            name,
            public_url,
            resource,
            event,
        )
    except ApiError as e:
        # Handle the case where a webhook with the same name already exists
        if e.status_code != 409:
            raise (e)  # Raise any other API errors


# Connect to the ngrok local API to get the public URL
print("connecting to ngrok local api...", end="")
ngrok_url = get_public_url()
print("found ngrok public url", ngrok_url)

# Create a webhook for receiving messages
print("attempting to create webhook for messages...", end="")
create_webhook(ngrok_url + "/webhook/messages", "webex-bot-messages", "messages")
print("ok")

# Create a webhook for receiving attachment actions (e.g., card submissions)
print("attempting to create webhook for attachment actions (cards)...", end="")
create_webhook(
    ngrok_url + "/webhook/attachment-actions", "webex-bot-cards", "attachmentActions"
)
print("ok")


# Function to get a random cat fact from an external API
def get_catfact() -> str:
    response = requests.get(
        "https://catfact.ninja/fact"
    )  # Send a GET request to the cat fact API
    response.raise_for_status()  # Raise an error if the request was unsuccessful
    json_data = response.json()  # Parse the JSON response
    return json_data["fact"]  # Return the cat fact


# Function to get a random cat image from an external API
def get_image():
    url = "https://cataas.com/cat"  # URL of the cat image API

    res = requests.get(url)  # Send a GET request to the API

    res.raise_for_status()  # Raise an error if the request was unsuccessful

    return res.content  # Return the image content


# Function to execute a command based on the message text
def execute_cmd(cmd: str, room_id: str, parent_id: str) -> str:
    if cmd.lower().startswith("cat-fact"):
        # If the command is "cat-fact", get a cat fact and send it as a message
        fact = get_catfact()
        api.messages.create(room_id, parent_id, text=fact)
    elif cmd.lower().startswith("cat-image"):
        # If the command is "cat-image", get a cat image and send it as a message
        image_content = get_image()
        with tempfile.NamedTemporaryFile(delete=True, suffix=".png") as temp_file:
            temp_file.write(image_content)
            api.messages.create(room_id, parent_id, files=[temp_file.name])
    elif cmd.lower().startswith("scan"):
        # If the command is "scan", send the scan card as a message
        api.messages.create(
            room_id, parent_id, text="fallback", attachments=[scan_card]
        )
    else:
        # If the command is not recognized, send an error message
        api.messages.create(room_id, parent_id, text="Sorry, I didn't understand")


# Flask route to handle incoming messages
@app.route("/webhook/messages", methods=["POST"])
def webhook_messages():
    # Check if the message was sent by the bot itself to prevent loops
    if request.json["data"]["personId"] == bot_info.id:
        return "OK"
    # Get the room ID from the incoming request
    room_id = request.json["data"]["roomId"]

    # Get the message ID from the incoming request
    message_id = request.json["data"]["id"]

    # Retrieve the message details using the Webex API
    message = api.messages.get(message_id)
    parent_id = message.parentId

    print(request.json)  # Print the incoming request for debugging

    # Execute the command based on the message text
    execute_cmd(message.text, room_id, message_id if parent_id is None else parent_id)

    return "OK"  # Return a success response


# Flask route to handle attachment actions (e.g., card submissions)
@app.route("/webhook/attachment-actions", methods=["POST"])
def webhook_attachment_actions():
    # Retrieve the action details using the Webex API
    action = api.attachment_actions.get(request.json["data"]["id"])
    # Retrieve the message details using the Webex API
    message_details = api.messages.get(action.messageId)

    # Send a message with the scan result
    api.messages.create(
        action.roomId,
        message_details.parentId,
        text="Nmap scan result: Ports 22 and 80 are open.",
    )

    print(request.json)  # Print the incoming request for debugging
    return "OK"  # Return a success response


# Main entry point of the application
if __name__ == "__main__":
    app.run()  # Run the Flask application
