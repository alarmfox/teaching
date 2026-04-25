import marimo

__generated_with = "0.12.9"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # DTLab 2025 -  Devnet Workshop

        Welcome!

        Follow this presentation at: https://marimo.app/?slug=pfzza1

        In this workshop, you will learn about:

        - [] APIs
        - [] HTTP protocol and architecture
        - [] Rest APIs
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Understanding JSON
        *Javascript Object Notation* (JSON) is the most used **text-format** for exchanging data in REST APIs.

        ```json
        {
            "first_name": "Giuseppe",
            "last_name": "Capasso",
            "role": "instructor",
            "age": 27,
            "interests": [
                "music",
                "games"
            ],
            "projects": [
                {
                    "name": "Shadowfax",
                    "description": "A Rust RISCV trusted firwmare implementing COVE Specification",
                    "link": "https://github.com/Granp4sso/shadowfax.git"
                },
                {
                    "name": "enclave-benchmark",
                    "description": "A tool to compare SGX vs non SGX applicaitions in Rust",
                    "link": "https://github.com/Granp4sso/shadowfax.git"
                }
            ]
        }
        ```
        ## Dealing with JSON in Python

        Json is mapped to Python dictionaries using native `json` library.

        ```py
        import json
        ```

        It exposes 2 methods:

        - `json.loads`: converts a JSON string in a Python dictionary
        - `json.dumps`: converts a Python dictionary in a JSON string
        """
    )
    return


@app.cell
def _():
    import json

    dummy_json = r"""
    {
            "first_name": "Giuseppe",
            "last_name": "Capasso",
            "role": "instructor",
            "age": 27,
            "interests": [
                "music",
                "games"
            ],
            "projects": [
                {
                    "name": "Shadowfax",
                    "description": "A Rust RISCV trusted firwmare implementing COVE Specification",
                    "link": "https://github.com/Granp4sso/shadowfax.git"
                },
                {
                    "name": "enclave-benchmark",
                    "description": "A tool to compare SGX vs non SGX applicaitions in Rust",
                    "link": "https://github.com/Granp4sso/shadowfax.git"
                }
            ]
    }
    """

    ## Add the code to convert the dictionary from JSON
    d = json.loads(dummy_json)
    print(d["first_name"])
    return d, dummy_json, json


@app.cell
def _(json):
    my_dict = {
        "sw0": {
            "vlan1": {
                "ip": "192.168.1.10",
                "netmask": "255.255.255.0",
                "description": "Vlan interface"
            }
        },
        "r0": {
            "g0/0/0": {
                "ip": "192.168.1.254",
                "netmask": "255.255.255.0",
                "description": "LAN 1 gw"
            },
            "g0/0/1": {
                "ip": "192.168.2.254",
                "netmask": "255.255.255.0",
                "description": "LAN 2 gw"
            }
        }
    }

    ## Add the code to convert the dictionary in JSON
    json.dumps(my_dict)
    return (my_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Use a web API

        We need to perform **HTTP** requests using Python. Each request has a method: 

        - GET
        - PUT
        - POST
        - DELETE

        We will use `requests` library and attempt to fetch resources from a server:

        ```py
        import requests

        url = "https://dtlab-api.capass.org"

        requests.get(url)
        ```

        The `requests` library offers functions for each method. Each function accept 3 parameters:

        - the url as a string
        - headers as a dictionary
        - body as a string
        """
    )
    return


@app.cell
def _():
    import requests

    url = "https://dtlab-api.capass.org"
    api_key = "0InfNl5WZuR++sOUD4otAw=="

    # Get all devices
    requests.get(url)

    # Get device details

    # Create a new device

    # Update a device

    # Delete a device

    return api_key, requests, url


@app.cell(hide_code=True)
def _(mo):
    token_field = mo.ui.text(label="Webex access Token", kind="password")
    mo.md(
        f"""
        # Use Webex API

        We will learn basics Webex API. First, we need to understand how this API works, so head over to the [documentation](https://developer.webex.com/docs/basics).

        Perform the login andget a **personal access token** from [here](https://developer.webex.com/docs/getting-started).

        {token_field}

        Now, let's try to retrieve the rooms we are in. Look up the [documentation]()
        """
    )
    return (token_field,)


@app.cell
def _(token_field):
    # Retrieve the field
    webex_token = token_field.value
    print(webex_token)

    ## Complete the code retrieving the rooms

    return (webex_token,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Your turn

        This exercise will have 3 parts: 

        - Send a message in a room of your choice using Webex API
        - Retrieve last messages you sent in Webex
        - Work in tables, one of you creates a room and others sends messages in that room
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
