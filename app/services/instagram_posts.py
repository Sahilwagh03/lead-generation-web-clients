import re
import requests

USERNAME_REGEX = re.compile(r'"username"\s*:\s*"([^"]+)"')

def extract_username_from_post(post_url: str) -> str | None:
    r = requests.get(post_url, timeout=15)
    if r.status_code != 200:
        return None

    match = USERNAME_REGEX.search(r.text)
    if match:
        return match.group(1)

    return None
