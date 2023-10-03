import os
import json
import openai
import logging
import asyncio
import requests
import websockets

openai.api_key = os.environ.get('OPENAI_API_KEY')
access_token = os.environ.get('PUSHBULLET_ACCESS_TOKEN')
device_iden = os.environ.get('DEVICE_ID')

headers = {
    'Access-Token': access_token,
    'Content-Type': 'application/json'
}

logging.basicConfig(level=logging.INFO)

async def listen_for_sms():
    while True:
        try:
            async with websockets.connect(f'wss://stream.pushbullet.com/websocket/{access_token}') as websocket:
                while True:
                    response = await websocket.recv()
                    message_data = json.loads(response)
                    if message_data.get('type') == 'push' and message_data.get('push', {}).get('type') == 'sms_changed':
                        notifications = message_data.get('push', {}).get('notifications', [])
                        for notification in notifications:
                            thread_id = notification.get('thread_id')
                            sender_name = notification.get('title')
                            sms_text = notification.get('body')
                            print(f'New SMS from {sender_name}: {sms_text}')
                            
                            threads_url = f'https://api.pushbullet.com/v2/permanents/{device_iden}_threads'

                            threads_response = requests.get(threads_url, headers=headers)
                            if threads_response.status_code == 200:
                                threads_data = threads_response.json()
                                threads = threads_data.get('threads', [])
                                for thread in threads:
                                    if thread.get('id') == thread_id:
                                        recipients = thread.get('recipients', [])
                                        if recipients:
                                            phone_number = recipients[0].get('address')
                                            if phone_number:
                                                await send_reply(phone_number, sms_text)
                                            else:
                                                logging.error(f'No phone number found for thread_id {thread_id}')
                                        else:
                                            logging.error(f'No recipients found for thread_id {thread_id}')
                                        break
                            else:
                                logging.error(f'Failed to get thread data: {threads_response.text}')
        except websockets.ConnectionClosedError as e:
            logging.error(f"Connection closed: {e}, retrying in 1 seconds...")
            await asyncio.sleep(1)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

async def send_reply(phone_number, sender_message):
    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for xxx, an xxx. "
                        "Your task is to inform patients that xxx will look at their messages later "
                        "and they can book a consultation directly on Doctolib at "
                        "https://www.doctolib.fr/xxx/xxx/xxx/booking."
                    )
                },
                {"role": "user", "content": sender_message}
            ]
        )
        gpt_message = gpt_response['choices'][0]['message']['content']
        print(f'Sending response to {phone_number}: {gpt_message}')  # Print statement added
        data = {
            'data': {
                'target_device_iden': device_iden,
                'addresses': [phone_number],
                'message': gpt_message
            }
        }
        response = requests.post('https://api.pushbullet.com/v2/texts', headers=headers, data=json.dumps(data))
        response.raise_for_status()
        logging.info('Reply sent successfully.')
    except Exception as e:
        logging.error(f'Failed to send reply: {e}')

# If you are running this in a Jupyter Notebook or similar environment:
await listen_for_sms()

# If you are running this in a standalone script:
# asyncio.get_event_loop().run_until_complete(listen_for_sms())
