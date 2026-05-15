import sys
import requests
from flask import Flask, request
from requests_toolbelt.multipart.encoder import MultipartEncoder

access_token = "OGJkYTczNGQtYTJmYi00YTUyLWFlZDQtODhlODM5MzE3NmZhZjQyY2ExNGQtMjg4_PF84_9db17efa-dc2f-4ca3-90ae-30a52866391a"
base_url = "https://webexapis.com"

if access_token is None:
    print("Missing access token")
    sys.exit(1)

headers = {
    "Authorization": "Bearer {}".format(access_token),
    "Content-Type": "application/json",
}

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

app = Flask(__name__)


# Dynamic webhook creation
# Ngrok runs a local REST API
# the bot can use the api to get the random generated url
# and create a webhook or updating an existing one
def get_public_url() -> str:
    res = requests.get("http://localhost:4040/api/tunnels")
    res.raise_for_status()
    tunnels = res.json()
    return tunnels["tunnels"][0]["public_url"]


def create_webhook(
    public_url: str, name: str, resource: str, event: str = "created"
) -> None:
    url = base_url + "/v1/webhooks"
    body = {
        "name": name,
        "targetUrl": public_url,
        "resource": resource,
        "event": event,
    }
    res = requests.post(url, headers=headers, json=body)

    if res.status_code == 409:
        print("webhooks already exists, removing existing one if necessary")
        # get all webhooks
        webhooks = requests.get(url, headers=headers).json()
        # find the webhook which gives conflicts and remove it
        for webhook in webhooks["items"]:
            if webhook["name"] == "webex-bot" and webhook["targetUrl"] != public_url:
                requests.delete(url + f"/{webhook['id']}", headers=headers)
                # finally re-create the webhook
                requests.post(url, headers=headers, json=body).raise_for_status()


print("connecting to ngrok local api...", end="")
ngrok_url = get_public_url()
print("found ngrok public url", ngrok_url)

print("attempting to create webhook for messages...", end="")
create_webhook(ngrok_url + "/webhook/messages", "webex-bot-messages", "messages")
print("ok")

print("attempting to create webhook for attachment actions (cards)...", end="")
create_webhook(
    ngrok_url + "/webhook/attachment-actions", "webex-bot-cards", "attachmentActions"
)
print("ok")


def get_room_details(id: str) -> dict:
    url = base_url + "/v1/rooms/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_self_details() -> dict:
    url = base_url + "/v1/people/me"
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_message_details(id: str) -> dict:
    url = base_url + "/v1/messages/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_catfact() -> str:
    """Get a cat fact from catfact.ninja and return it as a string.

    Functions for Soundhound, Google, IBM Watson, or other APIs can be added
    to create the desired functionality into this bot.

    """
    response = requests.get("https://catfact.ninja/fact")
    response.raise_for_status()
    json_data = response.json()
    return json_data["fact"]


def get_image():
    url = "https://cataas.com/cat"

    res = requests.get(url)

    res.raise_for_status()

    return res.content


def send_simple_text_message(
    room_id: str, text: str, parentId: str | None = None
) -> None:
    url = base_url + "/v1/messages"
    res = requests.post(
        url,
        headers=headers,
        json={
            "text": text,
            "roomId": room_id,
            "parentId": parentId,
        },
    )

    # res.raise_for_status()

    print(res.json())


def send_image(room_id: str, content: str | bytes, parentId: str) -> None:
    m = MultipartEncoder(
        {
            "roomId": room_id,
            "text": "Here is your picture",
            "parentId": parentId,
            "files": ("cat.png", content, "image/png"),
        }
    )

    r = requests.post(
        "https://webexapis.com/v1/messages",
        data=m,
        headers={
            "Authorization": "Bearer {}".format(access_token),
            "Content-Type": m.content_type,
        },
    )

    r.raise_for_status()

    print(r.json())


def send_card(room_id: str, card_content: dict, parentId: str) -> None:
    """
    Send a card to a Webex room.

    :param room_id: The ID of the Webex room.
    :param card_content: The content of the card in JSON format.
    """
    url = base_url + "/v1/messages"
    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json",
    }
    payload = {
        "roomId": room_id,
        "markdown": "This is your card",
        "parentId": parentId,
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card_content,
            }
        ],
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    print("Card sent successfully:", response.json())


def execute_cmd(cmd: str, room_id: str, prev_msg_id: str) -> str:
    if cmd.lower().startswith("cat-fact"):
        fact = get_catfact()
        send_simple_text_message(room_id, fact, prev_msg_id)
    elif cmd.lower().startswith("cat-image"):
        image = get_image()
        send_image(room_id, image, prev_msg_id)
    elif cmd.lower().startswith("scan"):
        send_card(room_id, scan_card, prev_msg_id)
    else:
        send_simple_text_message(room_id, "Sorry, I didn't understand", prev_msg_id)


def get_actions_detail(id: str) -> dict:
    url = base_url + f"/v1/attachment/actions/{id}"

    r = requests.get(url, headers=headers)

    r.raise_for_status()

    return r.json()


@app.route("/webhook/messages", methods=["POST"])
def webhook_messages():
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

    print(json_data)

    # parse message
    execute_cmd(message["text"], room_id, message_id)

    return "OK"


@app.route("/webhook/attachment-actions", methods=["POST"])
def webhook_attachment_actions():
    action = get_actions_detail(request.json["data"]["id"])
    message_details = get_message_details(action["messageId"])

    send_simple_text_message(
        action["roomId"],
        "Nmap scan result: Ports 22 and 80 are open.",
        message_details["parentId"],
    )

    return "OK"


if __name__ == "__main__":
    app.run()
