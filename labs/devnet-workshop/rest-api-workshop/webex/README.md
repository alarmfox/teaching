# Webex Chatbot Lab

## Introduction
Welcome to the Webex Chatbot Lab! In this lab, you will create a simple chatbot using the Webex API. You will start with a starter file that provides basic functionality, and your task will be to extend it by adding new commands.

## Prerequisites
Before you begin, ensure you have the following:
- Basic knowledge of the Python programming language
- Familiarity with the Flask framework
- A Webex account with access to the Webex API
- Python and Flask installed on your computer

## Getting Started

You will receive two files as input:
- `bot_base.py`: This file contains the basic structure of your chatbot.
- `requirements.txt`: This file lists the necessary Python dependencies.


## Installing Dependencies

To start working on the lab tasks, you need to install the required Python dependencies. Follow the instructions below:

1. **Navigate to the Project Directory**: Open a terminal or command prompt and navigate to the directory where your project files are located.

2. **Install Dependencies**: Run the following command to install the dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Using ngrok

To expose your local server to the internet, you will use ngrok. This is necessary for Webex to send messages to your bot.

1. **Download ngrok**: Visit [ngrok's website](https://ngrok.com/download) and download the appropriate version for your operating system.

2. **Install ngrok**: Follow the installation instructions provided on the ngrok website.

3. **Run ngrok**: In your terminal, navigate to the directory where ngrok is installed and run the following command to expose your local server:

   ```bash
   ./ngrok http 5000
   ```

   This will provide you with a public URL that you can use to configure your Webex bot.


## Lab Tasks

### Task 1: Add a Command to Send Cat Images
Your first task is to add a command that allows the chatbot to send cat images to users. You can use the [Cataas API](https://cataas.com/cat) to fetch cat images. Below is a simple script to save the image as a `png` file:

```python
import requests

r = requests.get("https://cataas.com/cat")
with open("out.png", "wb") as f:
    f.write(r.content)
```

To understand how to send attachments to a Webex message, refer to [this article](https://developer.webex.com/docs/basics).

### Task 2: Add More Commands (Optional)
If you complete Task 1 quickly and wish to further enhance your chatbot, consider adding more commands of your choice. For example, you can add commands to fetch jokes, weather updates, or news articles. Be creative and explore different APIs to expand your chatbot's functionality.
