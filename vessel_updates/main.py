# main.py

import chainlit as cl
from agents.vessel_agent import get_vessel_data

@cl.on_message
async def handle_message(msg: cl.Message):
    if "track" in msg.content.lower():
        # Extract date from message (basic logic)
        import re
        date_match = re.search(r"\d{1,2}\w{2}\s+\w+", msg.content)
        date_str = date_match.group(0) if date_match else "Unknown"

        # Convert to proper format (you can enhance this)
        date_query = "25th July"  # parse from user input dynamically
        vessel_info = get_vessel_data(date_query)

        await cl.Message(content="\n".join([", ".join(v) for v in vessel_info])).send()
