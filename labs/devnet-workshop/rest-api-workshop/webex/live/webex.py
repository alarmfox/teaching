import requests

base_url = "https://webexapis.com"
# access_token = "NmRjNmE5MzItOTIyNi00YmE1LTlmYmUtMmMzMTgwZmMxMjRiMmRiMWQyMzEtYTBj_PF84_9db17efa-dc2f-4ca3-90ae-30a52866391a"
access_token = "NGFhMzg3ODEtZDUxNy00NjgxLTgyYTYtOTEwZjZjNzM5NzFlNmEwM2EyODUtMzAy_P0A1_bbd62b13-3612-4c34-8eff-7f35cdce90eb"

headers = {"Authorization": f"Bearer {access_token}"}

rooms = requests.get(base_url + "/v1/rooms", headers=headers).json()

room_id = rooms["items"][0]["id"]

print(room_id)

data = {"roomId": room_id, "text": "ciao"}

print(requests.post(base_url + "/v1/messages", headers=headers, data=data).json())
