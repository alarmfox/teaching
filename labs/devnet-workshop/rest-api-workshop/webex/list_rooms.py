import os
import requests

from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv("WEBEXAPI_TOKEN")

url = 'https://webexapis.com/v1/rooms'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'max': '100'}

res = requests.get(url, headers=headers, params=params)

res.raise_for_status()
print(res.text, res.status_code)
