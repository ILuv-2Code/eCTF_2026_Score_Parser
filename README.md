# CTFd Challenge Solve Scraper

A Selenium-based script that logs into a CTFd instance, scrapes solve counts per challenge by team, and exports the results to a CSV file.

---

## Requirements

- Python 3.x
- A supported browser (Edge, Chrome, or Firefox) with its corresponding WebDriver

Install dependencies:
```bash
pip install -r packages.txt
```

---

## Setup

### 1. Configure Credentials

Create a `creds.json` file in the project root:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

> Do not commit `creds.json` to version control. Add it to your .gitignore

### 2. Select Your Browser

In the script, uncomment the WebDriver import that matches your browser:

```python
# Edge (default)
from selenium.webdriver.edge.webdriver import WebDriver

# Chrome
# from selenium.webdriver.chrome.webdriver import WebDriver

# Firefox
# from selenium.webdriver.firefox.webdriver import WebDriver
```

---

## Usage

```bash
python eCTF_Specific_Parser.py
```

Results will be saved to a `.csv` file in the project directory.

---

## Output

The script generates a CSV file containing solve counts for each challenge, organized by team.

---

## Notes

- Make sure your WebDriver version matches your installed browser version.
- This script was built for eCTF-specific CTFd instances and may need adjustments for other deployments.
