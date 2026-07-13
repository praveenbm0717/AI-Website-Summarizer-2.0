"""
scraper.py

A robust website scraper for the AI Website Summarizer.

Features
--------
✓ URL validation
✓ Automatic https://
✓ Custom headers
✓ Timeout handling
✓ SSL handling
✓ Redirect handling
✓ Removes unwanted HTML
✓ Cleans extracted text
✓ Limits very large pages
"""

import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse

# -----------------------------
# Configuration
# -----------------------------

TIMEOUT = 15

MAX_CONTENT_LENGTH = 6000

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    ),
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.9",
}


# -----------------------------
# Validate URL
# -----------------------------

def validate_url(url: str):

    url = url.strip()

    if not url:
        raise ValueError("Please enter a website URL.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:
        raise ValueError("Invalid website URL.")

    return url


# -----------------------------
# Clean Extracted Text
# -----------------------------

def clean_text(text: str):

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


# -----------------------------
# Fetch Website
# -----------------------------

def fetch_website_contents(url: str):

    try:

        url = validate_url(url)

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

    except ValueError as e:
        return f"❌ {e}"

    except requests.exceptions.Timeout:
        return "❌ Request timed out."

    except requests.exceptions.SSLError:
        return "❌ SSL Certificate Error."

    except requests.exceptions.TooManyRedirects:
        return "❌ Too many redirects."

    except requests.exceptions.ConnectionError:
        return "❌ Unable to connect to the website."

    except requests.exceptions.HTTPError:

        code = response.status_code

        if code == 403:
            return "❌ Website blocked this request (403 Forbidden)."

        if code == 404:
            return "❌ Website not found (404)."

        return f"❌ HTTP Error {code}"

    except requests.exceptions.RequestException as e:
        return f"❌ {e}"

    # -----------------------------
    # Parse HTML
    # -----------------------------

    soup = BeautifulSoup(response.text, "html.parser")

    title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else "No Title"
    )

    # Remove unnecessary elements

    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "aside",
        "noscript",
        "svg",
        "form",
        "button",
        "img",
        "video",
        "audio",
    ]):
        tag.decompose()

    text = soup.get_text(
        separator="\n",
        strip=True
    )

    text = clean_text(text)

    if len(text) < 100:
        return "❌ Website contains very little readable content."

    # Prevent huge prompts

    if len(text) > MAX_CONTENT_LENGTH:
        text = text[:MAX_CONTENT_LENGTH]

    return f"""
Website Title

{title}

Website Content

{text}
"""