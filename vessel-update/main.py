import chainlit as cl

@cl.on_chat_start
async def start():
    await cl.Message("🚢 Welcome to Karachi Vessel Bot! Ask for today's vessels or send WhatsApp number.").send()

@cl.on_message
async def handle(message: cl.Message):
    from agents.vessel_agent import handle_user_message
    await handle_user_message(message)