# MAPAS Grade Scraper 🎓

A Python scraper that monitors the **2025.MAPAS.Status** Google Sheet for grade updates and sends WhatsApp notifications when grades are posted.

---

## 📋 Overview

This script automatically checks a published Google Sheet for your grade in the "nota sesiune scris" column. When a grade appears, it sends you a WhatsApp message via Twilio.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Main programming language |
| **BeautifulSoup4** | HTML parsing and web scraping |
| **Requests** | HTTP requests to fetch the Google Sheet |
| **Twilio API** | WhatsApp message delivery |
| **python-dotenv** | Environment variable management |
| **Koyeb** | Cloud deployment (runs 24/7) |

---

**Summary:**
1. Fetches the published Google Sheet every 5 minutes
2. Parses HTML to find your row (by student ID)
3. Checks if cell [1] (nota sesiune scris) has a value
4. If empty → waits 5 minutes and checks again
5. If grade found → sends WhatsApp message and exits

---

## 📁 Project Structure

```
Scrapper_Verificare_Note/
├── mapas_grade_sms.py    # Main scraper script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local only)
└── README.md              # This file
```

