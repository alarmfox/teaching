import os
import sys
import requests

from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("WEBEXAPI_TOKEN")

if access_token is None:
    print("Missing access token")
    sys.exit(1)

base_url = 'https://webexapis.com'

# get rooms
rooms_url = base_url + "/v1/rooms"

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'max': '100'}
rooms = requests.get(rooms_url, headers=headers, params=params)

if rooms.status_code != 200:
    print(rooms.json())
    sys.exit(1)

rooms = rooms.json()

# search for room "Test"
for room in rooms["items"]:
    if room["title"] == "Test":
        # print(room)
        room_id = room["id"]

print("Room id is", room_id)
message_url = base_url + "/v1/messages"

body = {
    "roomId": room_id,
    "text": "Hello from python"
}

message = requests.post(message_url, headers=headers, json=body)

print(message.json())
