import os
import chainlit as cl
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome! Translate anything.").send()

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Translating...")
    await msg.send()

    try:
        response = completion(
            model="gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=[{"role": "user", "content": message.content}],
            provider="gemini"
        )

        msg.content = response.choices[0].message.content
        await msg.update()

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
