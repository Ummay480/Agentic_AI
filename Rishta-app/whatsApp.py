import chainlit as cl
import requests
from agents import function_tool
import os

@function_tool
def send_whatsApp_message(number: str, message: str) -> str:
    """
    Simulates sending a WhatsApp message.
    In production, replace this with real API like Twilio or WhatsApp Business API.
    """

    instance_id = os.getenv("INSTANCE_ID")
    token = os.getenv("API_TOKEN")

    url = f"https://api.ultramsg.com/{{instance_id}}/messages/chat"

    payload = {
        "token": token,
        "to": number,
        "body": message
    }

    response = requests.post(url, data=payload)
    if response.status_code ==200:
    
        return f"Message sent successfully to {number}"
    else:
        return f" X failed to send message. Error: {response.text}"
