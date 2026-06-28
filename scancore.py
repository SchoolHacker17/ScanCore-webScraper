import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tldextract
from collections import deque
from colorama import Fore, Style, init

init(autoreset=True)


print(Fore.RED + r"""
  ____                   ____               
 / ___|  ___ __ _ _ __  / ___|___  _ __ ___ 
 \___ \ / __/ _` | '_ \| |   / _ \| '__/ _ \
  ___) | (_| (_| | | | | |__| (_) | | |  __/
 |____/ \___\__,_|_| |_|\____\___/|_|  \___|
                                            
""")

# -----------------------------
# Regex patterns
# -----------------------------
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
PHONE_REGEX = re.compile(r"\b(?:\+?\d{1,3})?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
CUSTOM_REGEX = re.compile(r"\bkey_[A-Za-z0-9]{16}\b")

# -----------------------------
# Helpers
# -----------------------------
def get_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def is_internal(url, root_domain):
    return get_domain(url) == root_domain

# -----------------------------
# Main crawler
# -----------------------------
def crawl(start_url, max_pages=100):
    root_domain = get_domain(start_url)
    visited = set()
    queue = deque([start_url])

    results = {
        "emails": set(),
        "ips": set(),
        "phones": set(),
        "custom": set(),
        "pages_scanned": 0
    }

    while queue and len(visited) < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        try:
            response = requests.get(url, timeout=8)
        except Exception:
            print(Fore.BLUE + f"[SKIP] Failed to load: {url}")
            continue

        if response.status_code >= 400:
            print(Fore.BLUE + f"[SKIP] Error {response.status_code}: {url}")
            continue

        results["pages_scanned"] += 1

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(" ", strip=True)

        # Extract data
        emails = EMAIL_REGEX.findall(text)
        ips = IP_REGEX.findall(text)
        phones = PHONE_REGEX.findall(text)
        custom = CUSTOM_REGEX.findall(text)

        # -----------------------------
        # Print results for THIS page
        # -----------------------------
        print(Fore.BLUE + "\n" + "=" * 60)
        print(Fore.BLUE + f"Scanning: {url}")
        print(Fore.BLUE + "-" * 60)

        if emails:
            print(Fore.BLUE + f"Emails: {emails}")
            results["emails"].update(emails)
        else:
            print(Fore.BLUE + "Emails: None")

        if ips:
            print(Fore.BLUE + f"IP Addresses: {ips}")
            results["ips"].update(ips)
        else:
            print(Fore.BLUE + "IP Addresses: None")

        if phones:
            print(Fore.BLUE + f"Phone Numbers: {phones}")
            results["phones"].update(phones)
        else:
            print(Fore.BLUE + "Phone Numbers: None")

        if custom:
            print(Fore.BLUE + f"Custom Matches: {custom}")
            results["custom"].update(custom)
        else:
            print(Fore.BLUE + "Custom Matches: None")

        print(Fore.BLUE + "=" * 60)

        # Crawl internal links
        for a in soup.find_all("a", href=True):
            new_url = urljoin(url, a["href"])
            if new_url.startswith("http") and is_internal(new_url, root_domain):
                if new_url not in visited:
                    queue.append(new_url)

    return results


# -----------------------------
# Looping Program
# -----------------------------
while True:
    print(Fore.BLUE + "\n=== Website Data Scraper ===")
    start = input(Fore.BLUE + "Enter a website URL (or type 'q' to quit): ").strip()

    if start.lower() == "q":
        break

    if not start.startswith("http"):
        start = "https://" + start

    data = crawl(start)

    print(Fore.GREEN + "\n=== FINAL RESULTS ===")
    print(Fore.GREEN + f"Total Pages Scanned: {data['pages_scanned']}")
    print(Fore.GREEN + f"All Emails: {data['emails']}")
    print(Fore.GREEN + f"All IP Addresses: {data['ips']}")
    print(Fore.GREEN + f"All Phone Numbers: {data['phones']}")
    print(Fore.GREEN + f"All Custom Matches: {data['custom']}")

    input(Fore.GREEN + "\nPress Enter to scan another URL...")
