import datetime
import json
from typing import List, Dict
# schedular agent
def schedular_agent(topics:List[str],deadline: str) ->List[Dict]:
    try:
        deadline_date = datetime.datetime.strptime(deadline, %Y-%M-%D").date()
    except ValueError:
        raise ValueError("Invalid date formate, Use YYYY-MM-DD.")


    today = datetime.date.today()
    days_remaining = (deadline_date = today).days
    if days_remaining <= 0:
        raise ValueError("Deadline must be a future date.")
    
    study_days = max(1, day_remaining // len(topics))
