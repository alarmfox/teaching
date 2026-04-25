import requests
import json

url = "https://dtlab-api.capass.org"
access_key = "0InfNl5WZuR++sOUD4otAw=="

r = requests.get(url)

devices = r.json()

# retrieve device details
for device in devices:
    detail = requests.get(url + f"/{device['id']}")
    print(detail.json())


new_device = {
    "serial": "CAT-2960-5483221",
    "model": "Catalyst-2960x-48p",
    "type": "SWL2",
    "interfaces": [
        {
            "name": "VLAN1",
            "address": "192.168.1.100",
            "netmask": "255.255.255.0",
            "description": "A VLAN",
            "status": "Administrative down",
        }
    ],
}

headers = {"Authorization": f"Bearer {access_key}"}

r = requests.post(url, headers=headers, data=json.dumps(new_device))

print(r.status_code, r.json())

print(r.cookies)
print(requests.get(url + "/3", cookies=r.cookies).json())
