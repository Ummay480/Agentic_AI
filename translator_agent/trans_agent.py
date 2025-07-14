import os
import json
import chainlit as cl
from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(
        content="Welcome to the **Translator Agent by Ummay Kulsoom**!\n\nPlease tell me **what you want to translate** and **into which language**?"
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Translating...!")
    await msg.send()

    history = cl.user_session.get("chat_history") or []

    # Always start with at least the latest message
    contents = []

    if history:
        for m in history:
            if m["role"] == "user":
                contents.append({"role": "user", "parts": [{"text": m["content"]}]})
            elif m["role"] == "assistant":
                contents.append({"role": "model", "parts": [{"text": m["content"]}]})

    # Add the new message to avoid sending empty contents
    contents.append({"role": "user", "parts": [{"text": message.content}]})

    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            contents=contents
        )

        # Support both response formats (depends on litellm version/config)
        if hasattr(response.choices[0].message, "content"):
            response_content = response.choices[0].message.content
        elif hasattr(response.choices[0].message, "parts"):
            response_content = response.choices[0].message.parts[0].text
        else:
            response_content = "No content returned from model."

        msg.content = response_content
        await msg.update()

        # Save new history
        history.append({"role": "user", "content": message.content})
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()


@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat_history") or []
    with open("translation_chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
    print("Chat history saved.")
