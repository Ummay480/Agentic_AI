import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv()
set_tracing_disabled(True)

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=provider,
)
# Web Developer
web_dev = Agent(
    name="web Developer expert",
    instructions="Build responsive and performant website using modern framework",
    model=model,
    handoff_description="handoff to web developer if the task is releated with web development."

)
# app developer
mobile_dev = Agent(
    name="Mobile App Devloper Expert",
    instructions="Build mobile application using modern framework.",
    model=model,
    handoff_description="handoff to app developer if the task is related to mobile app development."
)

#Marketing Agent
marketing = Agent(
    name =" Marketing Expert Agent",
    instructions="Create and execute Marketing strategies for product launches.",
    model=model,
    handoff_description="handoff to marketing agent if the task is related to marketing."
)
async def myAgent(user_input):
    manager = Agent(
        name = "Manager",
        instructions="You will chat with the user and delegate task to specialized agents base on their request",
        model=model,
        handoffs=[web_dev, mobile_dev, marketing]
    )

    response = await Runner.run(
        manager,
        input=user_input
    )

    return response.final_output