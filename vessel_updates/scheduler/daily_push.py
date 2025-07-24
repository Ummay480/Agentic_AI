from data.fetch_vessels import fetch_karachi_expected
from utils.send_whatsapp import send_whatsApp_message

subscribers = ["+923123456789", "+923456789123"]

def run_daily():
    vessels = fetch_karachi_expected()
    text = "🚢 Karachi Port Today:\n" + "\n".join(
        f"{v['vessel']} - {v['eta']} @ {v['type']}" for v in vessels
    )
    for number in subscribers:
        send_whatsApp_message(number, text)

run_daily()
