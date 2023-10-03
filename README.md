# Automated SMS Reply System

This system automates the process of replying to incoming SMS messages using Pushbullet and OpenAI's GPT-3.

## Overview

Given the influx of messages in the medical domain, this system listens for incoming SMS via Pushbullet's WebSocket API and generates human-like responses using OpenAI's GPT-3. The response guides patients to book their appointments online.

## Prerequisites

- Python 3.x
- `openai`, `requests`, and `websockets` Python libraries. Install them using:

  ```bash
  pip install openai requests websockets
  ```

## Configuration

Set up environment variables:
''
OPENAI_API_KEY: Your OpenAI API key.
PUSHBULLET_ACCESS_TOKEN: Your Pushbullet access token.
DEVICE_ID: The device identifier for Pushbullet.
''
Clone the repository and navigate to the project directory.

## Usage
Run the script:

bash
Copy code
python your_script_name.py
Disclaimer
This project is a side experiment and is not intended for production use, especially in the medical field. Ensure data privacy and consider self-hosting for sensitive applications. Always prioritize the privacy and security of patient data.
