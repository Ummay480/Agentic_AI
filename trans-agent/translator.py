from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = AsyncOpenAI, OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

writer = Agent(
    name="Translator Agent",
    instructions="""
    You are a translation agent. Translate the given English text into:
    - Chinese (中文)
    - Japanese (日本語)
    - Korean (한국어)
    - Mongolian
    - Romanian
    """
)

response = Runner.run_sync(
    writer,
    input="write an essay about Generative AI***",
    run_config=config
)

print(response.final_output)
