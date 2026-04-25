# REST API Lab Guide

## Introduction
Welcome to the REST API Lab! In this lab, you will learn how to interact with a REST API using Postman. Follow the instructions below to set up Postman and complete the lab activities.

## Prerequisites
Before you begin, make sure you have the following:
- Postman installed on your computer
- Basic knowledge of HTTP methods (GET, POST, DELETE, PUT)
- Basic understanding of REST APIs and JSON

### Installing Postman
Follow the instructions below to download and install Postman for your specific platform:

- **Windows**:
  - Download Postman for Windows from [here](https://www.postman.com/downloads/).
  - Run the installer and follow the installation instructions.

- **Mac**:
  - Download Postman for Mac from [here](https://www.postman.com/downloads/).
  - Open the downloaded .dmg file and drag Postman to your Applications folder.

- **Linux (Debian-based distro)**:
  - Download Postman for Linux from [here](https://www.postman.com/downloads/).
  - Open a terminal and navigate to the directory where the downloaded file is located.
  - Run the following commands:
    ```bash
    sudo tar -xzf Postman-linux-x64-8.0.9.tar.gz -C /opt
    sudo ln -s /opt/Postman/Postman /usr/bin/postman
    ```

## Lab Activities

### Activity 1: Perform a GET Request
1. Open Postman.
2. In the request URL field, enter the endpoint URL: `http://example.com/devices`.
3. Select the HTTP method as **GET**.
4. Click the **Send** button to execute the request.
5. Review the response body to see the list of devices returned by the API.

### Activity 2: Perform a GET Request for Device Details
1. Open Postman.
2. In the request URL field, enter the endpoint URL: `http://example.com/devices/{id}` (replace `{id}` with the ID of the device you want to retrieve details for).
3. Select the HTTP method as **GET**.
4. Click the **Send** button to execute the request.
5. Review the response body to see the details of the device.

### Activity 3: Perform a DELETE Request (with Authentication)
1. Open Postman.
2. In the request URL field, enter the endpoint URL: `http://example.com/devices/{id}` (replace `{id}` with the ID of the device you want to delete).
3. Select the HTTP method as **DELETE**.
4. Go to the **Authorization** tab.
5. Select **Bearer Token** from the Type dropdown.
6. Enter the static token `0InfNl5WZuR++sOUD4otAw==`.
7. Click the **Send** button to execute the request.
8. Verify that the device has been successfully deleted.

### Activity 4: Perform a POST Request to Create a New Device (with Authentication)
1. Open Postman.
2. In the request URL field, enter the endpoint URL: `http://example.com/devices`.
3. Select the HTTP method as **POST**.
4. Go to the **Authorization** tab.
5. Select **Bearer Token** from the Type dropdown.
6. Enter the static token `0InfNl5WZuR++sOUD4otAw==`.
4. Go to the **Body** tab.
5. Select **Raw** and choose **JSON** from the dropdown.
6. Enter the JSON object representing the new device:

```json
{
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
```

### Activity 5: Perform a PUT Request to Update a Device
1. Open Postman.
2. In the request URL field, enter the endpoint URL: `http://example.com/devices/{id}` (replace `{id}` with the ID of the device you want to update).
3. Select the HTTP method as **PUT**.
4. Go to the **Authorization** tab.
5. Select **Bearer Token** from the Type dropdown.
6. Enter the static token `0InfNl5WZuR++sOUD4otAw==`.
7. Go to the **Body** tab.
8. Select **Raw** and choose **JSON** from the dropdown.
9. Enter the updated JSON object representing the device:

```json
{
    "serial": "UPDATED_SERIAL_NUMBER",
    "model": "UPDATED_MODEL",
    "type": "UPDATED_TYPE",
    "interfaces": [
        {
            "name": "VLAN1",
            "address": "UPDATED_IP_ADDRESS",
            "netmask": "UPDATED_NETMASK",
            "description": "UPDATED_DESCRIPTION",
            "status": "UPDATED_STATUS"
        }
    ]
}

```
## Conclusion
Congratulations! You have completed the REST API lab using Postman. You have learned how to perform GET, PUT, DELETE, and POST requests, as well as how to handle authentication using Bearer tokens.

If you have any questions or need assistance, feel free to ask your instructor or classmates.

Happy API testing!

