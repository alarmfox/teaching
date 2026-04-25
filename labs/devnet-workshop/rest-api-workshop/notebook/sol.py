import requests

url = "https://dtlab-api.capass.org"
api_key = ""

## Get all devices
r = requests.get(url)
cookie = r.headers["Set-Cookie"]

## Create a new device
headers = { 
    "Cookie": cookie, 
    "Content-Type": "application/json", 
    "Authorization": f"Bearer {api_key}" 
}

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
            "status": "Administrative down"
        }
    ]
}

new_device = requests.post(url, headers = headers, data =  json.dumps(new_device))

new_device.json()

## Get device detail

r = requests.get(url + "/1")
r.json()

## Update a device
updated_device = {
    "serial": "CAT-2960-5483221",
    "model": "Catalyst-2960x-48p",
    "type": "SWL2",
    "interfaces": [
        {
            "name": "VLAN1",
            "address": "192.168.1.200",
            "netmask": "255.255.255.0",
            "description": "A VLAN",
            "status": "UP"
        }
    ]
}
updated_device = requests.put(url + "/1", headers = headers, data =  json.dumps(updated_device))

updated_device.json()

## Delete a device

requests.delete(url + "/1", headers=headers)

webex_token = token_field.value

webex_base_url = "https://webexapis.com"

webex_headers = {"Authorization": f"Bearer {webex_token}"}
requests.get(webex_base_url + "/v1/rooms", headers = webex_headers).json()

