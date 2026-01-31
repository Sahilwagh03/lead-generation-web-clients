import time
import requests

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_profile_html(username: str) -> str | None:
    url = f"https://www.instagram.com/{username}/"

    r = requests.get(url, headers=BASE_HEADERS, timeout=15)

    if r.status_code != 200:
        return None

    html = r.text.lower()
    if "login" in html or "challenge" in html:
        return None

    time.sleep(3)  # 👈 critical (safe rate)
    return r.text
