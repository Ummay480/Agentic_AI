import os
import re
from dotenv import load_dotenv
import chainlit as cl
try:
    import google.generativeai as genai
except ImportError:
    genai = None
try:
    from data.fetch_vessels import fetch_karachi_expected
except ImportError:
    def fetch_karachi_expected():
        return [
            {"vessel": "Ship A", "eta": "2025-07-22", "type": "Cargo"},
            {"vessel": "Ship B", "eta": "2025-07-23", "type": "Container"}
        ]
try:
    from utils.send_whatsapp import send_whatsApp_message
except ImportError:
    def send_whatsApp_message(number, message):
        return f"Mock: Message sent to {number}"

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if genai and API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

async def handle_user_message(message: cl.Message):
    await cl.Message("📡 Checking updates...").send()

    user_input = message.content.lower()
    vessel_data = fetch_karachi_expected()
    response_text = "🚢 Karachi Port Today:\n" + "\n".join(
        [f"{v['vessel']} - {v['eta']} @ {v['type']}" for v in vessel_data]
    )

    if "details" in user_input and model:
        try:
            response = await model.generate_content_async(user_input)
            response_text += f"\n\nAdditional Info: {response.text}"
        except Exception as e:
            response_text += f"\n\nError fetching additional info: {str(e)}"
    elif not model:
        response_text += "\n\nGemini API not available (missing API key or library)."

    await cl.Message(response_text).send()

    if "whatsapp" in user_input:
        number_match = re.search(r'03\d{9}', user_input)
        if number_match:
            number = number_match.group(0)
            msg_text = "🚢 Karachi Port Today:\n" + "\n".join(
                [f"{v['vessel']} - {v['eta']} @ {v['type']}" for v in vessel_data]
            )
            response = send_whatsApp_message(f"+92{number[1:]}", msg_text)
            await cl.Message(f"📲 {response}").send()