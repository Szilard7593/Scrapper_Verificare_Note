#!/usr/bin/env python3
"""
MAPAS Grade Scraper - VERSION (checks cell [1])
"""

"""
[Check] → Fetch page → Grade empty? → Wait 5 min → [Check again] → Fetch page → Grade posted! → WhatsApp! 
"""

import os
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Config from .env
SHEET_URL = os.getenv('SHEET_URL')
YOUR_ID = os.getenv('YOUR_ID')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL'))


def send_whatsapp(message):
    """Send WhatsApp message via Twilio."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_='whatsapp:' + TWILIO_PHONE_NUMBER,
            to='whatsapp:' + YOUR_PHONE_NUMBER
        )
        print("[WHATSAPP SENT]")
    except Exception as e:
        print(f"[WHATSAPP ERROR] {e}")


def check_grade():
    """Check if cell [1] (nota sesiune scris) has a grade."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(SHEET_URL, headers=headers, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find row with your ID
    for row in soup.find_all('tr'):
        if YOUR_ID in row.get_text():
            cells = row.find_all('td')

            # Check cell [1] - nota sesiune scris (td.s13)
            if len(cells) > 4 and cells[4].get_text(strip=True):
                return cells[4].get_text(strip=True)
    return None


def main():
    print(f"Nota student {YOUR_ID}...")

    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking...", end=" ")

        try:
            grade = check_grade()

            if grade:
                print(f"GRADE FOUND: {grade}")
                send_whatsapp(f"MAPAS nota sesiune scris: {grade}")
                time.sleep(60*60*2) # wait 2 hpurs, trying to avoind spam
            else:
                print("No grade yet")

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()