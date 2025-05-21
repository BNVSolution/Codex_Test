"""Simple GUI to display the latest politics news from Naver."""

import os
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext

import requests

# Credentials for Naver Open API should be set as environment variables
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
    raise RuntimeError("NAVER_CLIENT_ID and NAVER_CLIENT_SECRET must be set")

NEWS_API_URL = "https://openapi.naver.com/v1/search/news.json"


def fetch_latest_politics_news():
    """Return a list of (title, link) tuples for the latest politics news."""
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
    items = []
    for item in data.get("items", []):
        title = item.get("title", "").replace("<b>", "").replace("</b>", "")
        link = item.get("originallink") or item.get("link")
        items.append((title, link))
    return items


def refresh_news():
    """Fetch news and display them in the text widget."""
    try:
        news_items = fetch_latest_politics_news()
    except Exception as exc:
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, f"Error fetching news: {exc}")
        return

    text_widget.delete("1.0", tk.END)
    text_widget.insert(
        tk.END,
        f"[{datetime.now():%Y-%m-%d %H:%M}] Latest Politics News\n",
    )
    for title, link in news_items:
        text_widget.insert(tk.END, f"- {title}\n  {link}\n")


root = tk.Tk()
root.title("Politics News")

text_widget = scrolledtext.ScrolledText(root, width=80, height=20)
text_widget.pack(fill=tk.BOTH, expand=True)

refresh_button = tk.Button(root, text="Refresh", command=refresh_news)
refresh_button.pack(pady=5)

refresh_news()
root.mainloop()
