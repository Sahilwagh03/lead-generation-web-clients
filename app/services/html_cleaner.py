from bs4 import BeautifulSoup

def clean_html_keep_links(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Remove noise
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    cleaned_parts = []

    for elem in soup.find_all(["a", "span", "div", "p"]):
        text = elem.get_text(strip=True)

        if not text:
            continue

        if elem.name == "a":
            href = elem.get("href")
            if href:
                cleaned_parts.append(f"{text} ({href})")
            else:
                cleaned_parts.append(text)
        else:
            cleaned_parts.append(text)

    # Deduplicate lines
    seen = set()
    final_lines = []
    for line in cleaned_parts:
        if line not in seen:
            seen.add(line)
            final_lines.append(line)

    return "\n".join(final_lines[:120])
