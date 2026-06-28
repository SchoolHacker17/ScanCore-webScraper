# ScanCore Web Scraper

A Python‑based internal web crawler that scans a target website, extracts useful or sensitive text‑based data, and recursively follows internal links. The tool provides real‑time, color‑coded terminal output and a complete summary of all findings after each scan.

---

## 🔍 Core Functionality
The scraper:

- Accepts a starting URL  
- Identifies the site’s **root domain**  
- Performs a controlled **BFS crawl** (default: 100 pages)  
- Downloads each page using `requests`  
- Parses HTML with **BeautifulSoup**  
- Extracts visible text  
- Searches for:
  - Email addresses  
  - IPv4 addresses  
  - Phone numbers  
  - Custom tokens matching `key_XXXXXXXXXXXXXXXX`  
- Prints results for each page  
- Adds internal links to the crawl queue  
- Displays a final summary of all collected data  

---

## 📦 Data Extracted
The crawler identifies and stores:

- **Emails**  
- **IP addresses**  
- **Phone numbers**  
- **Custom regex matches** (`key_` + 16 alphanumeric characters)

All results are stored in sets to avoid duplicates.

---

## 🧭 Crawling Logic
The script uses:

- A **deque queue** for BFS traversal  
- A **visited set** to prevent duplicate scans  
- `urljoin()` to resolve relative links  
- `tldextract` to determine domain boundaries  

Only URLs that start with `http` and match the **root domain** are crawled.

---

## 🎨 Terminal Output
Using Colorama, the script prints:

- A stylized ASCII banner  
- Per‑page scan summaries  
- Skip notices for unreachable or error‑status pages  
- A final aggregated results section  

Colors help distinguish scanning, skipping, and final output.

---

## 🧪 User Interaction
The script runs in a loop, allowing repeated scans without restarting. After each crawl, it displays:

- Total pages scanned  
- All unique emails  
- All unique IP addresses  
- All unique phone numbers  
- All custom regex matches  

Type `q` to quit.

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install requests beautifulsoup4 tldextract colorama
