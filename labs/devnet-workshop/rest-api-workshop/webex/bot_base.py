import sys
import requests
from flask import Flask, request

access_token = ""
base_url = "https://webexapis.com"

if access_token is None:
    print("Missing access token")
    sys.exit(1)

headers = {
    "Authorization": "Bearer {}".format(access_token),
    "Content-Type": "application/json",
}

app = Flask(__name__)


# Dynamic webhook creation
# Ngrok runs a local REST API
# the bot can use the api to get the random generated url
# and create a webhook or updating an existing one
# This function retrieves the public URL from the ngrok service.
# Ngrok is used to expose local servers to the internet.
# It fetches the list of tunnels and returns the public URL of the first tunnel.
def get_public_url() -> str:
    res = requests.get("http://localhost:4040/api/tunnels")
    res.raise_for_status()
    tunnels = res.json()
    return tunnels["tunnels"][0]["public_url"]


# This function creates a webhook on the Webex platform.
# It uses the public URL provided by ngrok to set up the webhook.
# If a webhook with the same name or URL already exists, it deletes the existing one and creates a new one.
def create_webhook(public_url: str) -> None:
    url = base_url + "/v1/webhooks"
    body = {
        "name": "webex-bot",
        "targetUrl": public_url + "/webhook",
        "resource": "messages",
        "event": "created",
    }
    res = requests.post(url, headers=headers, json=body)

    if res.status_code == 409:
        print("webhooks already exists, removing existing one")
        # get all webhooks
        webhooks = requests.get(url, headers=headers).json()
        # find the webhook which gives conflicts and remove it
        for webhook in webhooks["items"]:
            if webhook["targetUrl"] == public_url or webhook["name"] == "webex-bot":
                print(webhook)
                requests.delete(url + f"/{webhook['id']}", headers=headers)

        # finally re-create the webhook
        requests.post(url, headers=headers, json=body).raise_for_status()


print("connecting to ngrok local api...")
ngrok_url = get_public_url()
print("found ngrok public url", ngrok_url)

print("attempting to create webhook")
create_webhook(ngrok_url)
print("webhook created successfully")


# This function retrieves details of a specific room in Webex by its ID.
# It sends a GET request to the Webex API and returns the room details as a dictionary.
def get_room_details(id: str) -> dict:
    url = base_url + "/v1/rooms/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


# This function retrieves the details of the bot itself.
# It sends a GET request to the Webex API to fetch the bot's information.
def get_self_details() -> dict:
    url = base_url + "/v1/people/me"
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


# This function retrieves the details of a specific message in Webex by its ID.
# It sends a GET request to the Webex API and returns the message details as a dictionary.
def get_message_details(id: str) -> dict:
    url = base_url + "/v1/messages/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


# This function fetches a random cat fact from the catfact.ninja API.
# It returns the cat fact as a string.
def get_catfact() -> str:
    response = requests.get("https://catfact.ninja/fact")
    response.raise_for_status()
    json_data = response.json()
    return json_data["fact"]


# This function sends a message to a specific room in Webex.
# It takes the message text and the room ID as parameters and posts the message using the Webex API.
def send_message(text: str, room_id: str) -> None:
    url = base_url + "/v1/messages"
    res = requests.post(url, headers=headers, json={"text": text, "roomId": room_id})

    res.raise_for_status()


# This function executes a command based on the message received.
# If the command is "/cat", it fetches a cat fact and sends it to the room.
# Otherwise, it sends a default message indicating the command was not understood.
def execute_cmd(cmd: str, room_id: str) -> str:
    if cmd.lower().startswith("/cat"):
        fact = get_catfact()
        send_message(fact, room_id)
    else:
        send_message("Sorry, I didn't understand", room_id)


# This function handles incoming webhook POST requests from Webex.
# It checks if the message was sent by the bot itself to prevent loops.
# It retrieves the room and message details, then executes the command in the message.
@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.json

    # This is a VERY IMPORTANT loop prevention control step.
    # If you respond to all messages...  You will respond to the messages
    # that the bot posts and thereby create a loop condition.
    me = get_self_details()
    if json_data["data"]["personId"] == me["id"]:
        # Message was sent by me (bot); do not respond.
        return "OK"

    # get room
    room_id = json_data["data"]["roomId"]

    # get message
    message_id = json_data["data"]["id"]
    message = get_message_details(message_id)

    # parse message
    execute_cmd(message["text"], room_id)

    return "OK"


if __name__ == "__main__":
    app.run()
