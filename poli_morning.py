"""Fetches the latest political news from Naver at 7 AM."""

import os
import requests
import schedule
import time
from datetime import datetime

# Credentials for Naver Open API should be set as environment variables
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
    raise RuntimeError("NAVER_CLIENT_ID and NAVER_CLIENT_SECRET must be set")

NEWS_API_URL = "https://openapi.naver.com/v1/search/news.json"


def fetch_latest_politics_news():
    """Query Naver's news API for the latest politics articles."""
    params = {
        "query": "정치",
        "display": 5,
        "sort": "date",
    }
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    response = requests.get(NEWS_API_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    items = data.get("items", [])
    print(f"\n[{datetime.now():%Y-%m-%d %H:%M}] Latest Politics News")
    for item in items:
        title = item.get("title", "").replace("<b>", "").replace("</b>", "")
        link = item.get("originallink") or item.get("link")
        print(f"- {title}\n  {link}")


schedule.every().day.at("07:00").do(fetch_latest_politics_news)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(30)
