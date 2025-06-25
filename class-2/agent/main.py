# For get file from vs code
import os

# for accessing key
from agents import AAgent, syncOpenAI, Runner, OpenAIChatCompletionsModel, Agent
from dotenv import load_dotenv

# for making main function awaited
import asyncio
import chainlit as cl

load_dotenv

                                                     
gemini_api_key=os.getenv("GEMINI_API_KEY")

External_client = AsyncOpenAI (
    #  Create external Client using Async
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",,
)

model = OpenAIChatCompletionsModel



def main():
    print("Hello from agent!")


if __name__ == "__main__":
    asyncio.run( main())
