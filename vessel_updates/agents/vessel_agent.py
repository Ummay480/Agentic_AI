# agents/vessel_agent.py

from googleapiclient.discovery import build
from datetime import datetime
import os

def get_vessel_data(date_query):
    service = build('sheets', 'v4', developerKey=os.getenv("GOOGLE_API_KEY"))
    sheet = service.spreadsheets()
    spreadsheet_id = "YOUR_SPREADSHEET_ID"
    range_name = "Sheet1!A2:E100"  # Adjust range based on your sheet

    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    rows = result.get('values', [])

    matched = [row for row in rows if row[0].strip() == date_query]
    return matched or [["No vessel found for that date."]]
