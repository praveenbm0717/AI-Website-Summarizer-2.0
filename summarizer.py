"""
summarizer.py

AI Website Summarizer

Features
--------
✓ Groq API
✓ Error Handling
✓ Statistics
✓ Response Time
✓ Professional Prompt
"""

import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from scraper import fetch_website_contents

load_dotenv()

# ----------------------------
# API Key
# ----------------------------

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"

# ----------------------------
# System Prompt
# ----------------------------

SYSTEM_PROMPT = """
You are an expert Website Summarizer.

Your job is to produce a concise,
professional summary.

Rules:

• Ignore menus
• Ignore advertisements
• Ignore repeated text
• Ignore cookies
• Ignore navigation links

Return ONLY markdown.

Structure:

# Website Summary

## Overview

## Key Points

## Target Audience

## Main Features

## Final Takeaway

Maximum 150 words.
"""

# ----------------------------
# Summarize
# ----------------------------

def summarize(url):

    start = time.time()

    website = fetch_website_contents(url)

    # scraper already returns errors
    if website.startswith("❌"):
        return (
            website,
            "0",
            "0",
            "0 sec"
        )

    try:

        response = client.chat.completions.create(

            model=MODEL,

            temperature=0.3,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": website
                }
            ]
        )

    except Exception as e:

        return (
            f"❌ AI Error\n\n{e}",
            "0",
            "0",
            "0 sec"
        )

    summary = response.choices[0].message.content

    if not summary:
        summary = "No summary generated."

    words = len(summary.split())

    chars = len(summary)

    elapsed = round(
        time.time() - start,
        2
    )

    return (
        summary,
        f"{words} Words",
        f"{chars} Characters",
        f"{elapsed} sec"
    )