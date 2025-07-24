import requests
from bs4 import BeautifulSoup

def fetch_karachi_expected():
    try:
        url = "https://www.kpt.gov.pk/en/vessel-schedule"  # Replace with actual URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        vessels = []
        for row in soup.select('table.vessel-schedule tr'):
            cols = row.find_all('td')
            if cols:
                vessels.append({
                    'vessel': cols[0].text.strip(),
                    'eta': cols[1].text.strip(),
                    'type': cols[2].text.strip()
                })
        return vessels
    except Exception as e:
        print(f"Error fetching vessel data: {str(e)}")
        return [
            {"vessel": "Ship A", "eta": "2025-07-22", "type": "Cargo"},
            {"vessel": "Ship B", "eta": "2025-07-23", "type": "Container"}
        ]