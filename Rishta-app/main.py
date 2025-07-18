from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from whatsApp import send_whatsApp_message
import asyncio
import chainlit as cl

load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
api_key = API_KEY,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)
model = OpenAIChatCompletionsModel(
model = "gemini-2.5-flash",
openai_client=external_client
)
@function_tool
def get_user_data(min_age: int) -> list[dict]:
    "Retrive user data base on a minimum age"
    users = [
        {"name": "Muneeb","age":22},
        {"name": "Soaib","age":26},
        {"name": "Sarim","age":24},
        {"name": "Muneeb","age":23},
        {"name": "Muneeb","age":21},
        {"name": "Muneeb","age":25},
    ]
    for user in users:
        if user["age"] < min_age:
            users.remove(user)

    return users

# Rishty wali agent
rishty_agent = Agent(
    name = "Rishty_wali",
    instructions = """
        you are Rishty wali Aunti. Find matches from a custom tool based on age only.
        Reply short and send whatsApp message only if user asks.""",
    model=model,
    tools=[get_user_data,send_whatsApp_message]

)
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message("Assalam o alaikum! I am Match Maker Agent, tell me your age, and WhatsApp no ").send()

# Runner
@cl.on_message
async def main(message:cl.Message):
    await cl.Message("Thinking...").send()
    history = cl.user_session.get("history")or[]
    history.append({"role":"user", "content":message.content})

    result = Runner.run_sync(
        rishty_agent,
        input=history
    )

    history.append({"role": "assistsnt", "content": result.final_output})

    cl.user_session.set("history", history)

    await cl.Message(content=result.final_output).send()

