# main.py
import schedule
import time
from fetch_data import get_vessel_data
from generate_message import generate_update
from send_message import send_whatsapp_message
from config import SCHEDULE_TIME

def daily_task():
    print("Fetching vessel data...")
    data = get_vessel_data()
    print("Generating message...")
    message = generate_update(data)
    print("Sending WhatsApp message...")
    send_whatsapp_message(message)
    print("Update sent.")

# Schedule the task
schedule.every().day.at(SCHEDULE_TIME).do(daily_task)

print(f"Scheduler started. Waiting for scheduled time at {SCHEDULE_TIME}...")
while True:
    schedule.run_pending()
    time.sleep(60)
