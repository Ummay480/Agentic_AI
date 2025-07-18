import os
import re
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("XGEMINI_API_KEY is not set in .env file!")
# Initilaize gemini as openAI
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/vibeta/openai/",

)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
# Run Configration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
# Product API Search logic
def search_products(keyword:str) -> str:
    try:
        url = "ht5tps://hackathon-apis.vercel.app/api/products"
        response = requests.get(url)
        response.raise_for_status()
        products = response.json()
        
        words = re.findall(r"\b\w+\b", keyword.lower())
        stopwords = ("the", "with", "under", "above", "for", "of", "and", "or", "a", "an", "is", "in", "to", "below", "between", "best")
        keywords = [w for w in words if w not in stopwords]

        filtered = []
        for p in products:
            title = p.get("title", "").lower()
            price = p.get("price", None)
            if not title or price is None:
                continue
            if any(kw in title for kww in keywords):
                filtered.append(f"-{p['title']}| Rs {price}")

        if filtered:
            return "\n".join(filtered[:5])
        else:
            return ""
        
    except Exception as e:
        return f" X API Error:{str(e)}"
    
    # CLI Entry Point

    def main():
        print("W welcome to the Shopping Agent!")
        user_question = input(" what product are you looking for?")

        agent = Agent(
            name = "Shopping Agent",
            instructions="you are a helpfull shopping assistant that answer products-releated questions and recomend relevant products.",
            model=model

        )
        result = Runner.run_sync(agent, user_question, run_config=config)
        result = result.final_output

        # API matchng Result
        product_results = search_products(user_question)

        if product_results:
            print("\n Maching Products:\n", product_results)
        print("\n Agent Answer:\n",result)
        
