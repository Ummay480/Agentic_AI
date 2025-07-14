import os
import csv
import fitz
import difflib
import json
import subprocess
from dotenv import load_dotenv
import chainlit as cl
from chainlit.message import Message
from openai import AsyncOpenAI

load_dotenv()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def match_hs_code(item_name):
    with open("hs_lookup.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        items = [row["Item"] for row in reader]

    matches = difflib.get_close_matches(item_name.strip().lower(), [i.lower() for i in items], n=1, cutoff=0.5)

    if matches:
        matched_name = matches[0]
        with open("hs_lookup.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Item"].strip().lower() == matched_name:
                    return f"{row['HS Code']} (matched with: {row['Item']})"

    return "❓ Not Found — Needs Manual Classification"

@cl.on_chat_start
async def start():
    await Message("📦 Upload your Import Invoice PDF **or** paste invoice text below.").send()

@cl.on_message
async def handle_input(message: cl.Message):
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                path = os.path.join(UPLOAD_DIR, element.name)
                file_bytes = await element.get_content()
                with open(path, "wb") as f:
                    f.write(file_bytes)

                extracted_text = extract_text_from_pdf(path)
                await process_invoice(extracted_text)
                return

    await process_invoice(message.content)

async def process_invoice(text):
    await Message("🧠 Processing invoice using Gemini...").send()

    prompt = f"""
You're an AI assistant specialized in import invoice processing.

From the following raw invoice text, extract and return only these fields in valid JSON format:
- Invoice Number
- Invoice Date
- Item Description
- Quantity
- Unit Value
- Total Value
- Country of Origin
- Currency (if available)
- HS Code (if listed)
- Incoterm (if mentioned)

Text:
{text}
"""

    response = await client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    extracted = response.choices[0].message.content
    print("🔍 Gemini raw output:\n", extracted)

    try:
        data = json.loads(extracted)
    except Exception:
        await Message("⚠️ Gemini returned invalid JSON:\n```\n" + extracted + "\n```").send()
        return

    if not data.get("Incoterm"):
        data["Incoterm"] = "⚠️ Not specified — please add manually"

    item_name = data.get("Item") or data.get("Item Description") or ""
    if not data.get("HS Code") or "not found" in str(data.get("HS Code")).lower():
        data["HS Code"] = match_hs_code(item_name)

    with open("extracted_invoice.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    await Message(
        content=f"✅ Extracted Invoice:\n```json\n{json.dumps(data, indent=2)}\n```",
        actions=[
            cl.Action(name="run_automation", value="run", label="🚀 Run WEBOC Automation")
        ]
    ).send()

@cl.on_action
async def handle_action(action: cl.Action):
    if action.name == "run_automation":
        await Message("🔄 Launching WEBOC automation...").send()

        try:
            result = subprocess.run(["python", "weboc_automation.py"], capture_output=True, text=True)
            if result.returncode == 0:
                await Message("✅ Automation script finished successfully.").send()
            else:
                await Message(f"❌ Error during automation:\n```\n{result.stderr}\n```").send()
        except Exception as e:
            await Message(f"❌ Failed to run script:\n{str(e)}").send()
