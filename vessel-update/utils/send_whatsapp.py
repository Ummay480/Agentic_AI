from twilio.rest import Client
import os

def send_whatsApp_message(to: str, text: str):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    message = client.messages.create(
        body=text,
        from_=f'whatsapp:{os.getenv("TWILIO_PHONE_NUMBER")}',
        to=f'whatsapp:{to}'
    )
    return "Message sent successfully ✅"