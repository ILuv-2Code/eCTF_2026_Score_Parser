from selenium.webdriver.edge.webdriver import WebDriver ##change this to decide websdriver (Firefox, Chrome, etc)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
agent = WebDriver()


from selenium.webdriver.edge.options import Options
options = Options()
options.add_argument("--headless")      
options.add_argument("--disable-gpu")

import csv
import time


def wait_for_element(locator, timeout=10):
    return WebDriverWait(agent, timeout).until(
        EC.presence_of_element_located(locator)
    )

def wait_for_elements(locator, timeout=10):
    return WebDriverWait(agent, timeout).until(
        EC.presence_of_all_elements_located(locator)
    )

def wait_for_element_visible(locator, timeout=10):
    return WebDriverWait(agent, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_for_element_clickable(locator, timeout=10):
    return WebDriverWait(agent, timeout).until(
        EC.element_to_be_clickable(locator)
    )

def safe_click(element):

    agent.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
        element,
    )
    time.sleep(0.2)

    try:
        element.click()
    except ElementClickInterceptedException:
        agent.execute_script("arguments[0].click();", element)

def dismiss_any_open_modal():

    try:
        close_btn = agent.find_element(By.CSS_SELECTOR, "button.btn-close")
        safe_click(close_btn)
        WebDriverWait(agent, 5).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.modal-body"))
        )
    except Exception:
        pass


def page_login(url, submit_btn=None, **creds_info):
    agent.get(url)

    if creds_info and submit_btn:
        for key, value in creds_info.items():
            agent.find_element(By.ID, key).send_keys(value)
        agent.find_element(By.ID, submit_btn).click()


CHALLENGE_MAP = {
    "Steal Design":       "Steal Design",
    "Read Design":        "Read Design",
    "Backdoor":           "Backdoor Design",
    "Compromise Machine": "Compromise Machine",
    "Read Update":        "Read Update",
}
CHALLENGES = [
    "Steal Design",
    "Read Design",
    "Backdoor Design",
    "Compromise Machine",
    "Read Update",
]

TEAM_CATEGORY_PREFIX = "Attack - "

team_data = {}


page_login(
    url="https://ectf.ctfd.io/login",
    submit_btn="_submit",
    name= "username", ## username
    password= "password", ##input password
)

time.sleep(2)


categories = agent.find_elements(By.CSS_SELECTOR, "div.pt-5")

for cat_index in range(len(categories)):

    categories = agent.find_elements(By.CSS_SELECTOR, "div.pt-5")
    cat = categories[cat_index]

    try:
        category_name = cat.find_element(
            By.CSS_SELECTOR, ".category-header h3"
        ).text.strip()

        if not category_name.startswith(TEAM_CATEGORY_PREFIX):
            continue

        team_name = category_name[len(TEAM_CATEGORY_PREFIX):].strip()
        print(f"Processing team: {team_name}")

        if team_name not in team_data:
            team_data[team_name] = {ch: 0 for ch in CHALLENGES}

        buttons = cat.find_elements(By.CSS_SELECTOR, "button.challenge-button")

        for btn_index in range(len(buttons)):

            dismiss_any_open_modal()

            categories = agent.find_elements(By.CSS_SELECTOR, "div.pt-5")
            cat = categories[cat_index]
            buttons = cat.find_elements(By.CSS_SELECTOR, "button.challenge-button")
            btn = buttons[btn_index]

            try:
                challenge_name_full = btn.find_element(
                    By.CSS_SELECTOR, "p"
                ).text.strip()

                challenge_name = next(
                    (canonical for keyword, canonical in CHALLENGE_MAP.items()
                     if keyword in challenge_name_full),
                    None,
                )

                if not challenge_name:
                    continue

                safe_click(btn)

                modal = wait_for_element_visible(
                    (By.CSS_SELECTOR, "div.modal-body")
                )

                solves_tab = wait_for_element_clickable(
                    (By.CSS_SELECTOR, "button.challenge-solves")
                )
                safe_click(solves_tab)

                time.sleep(0.5)
                solves_rows = agent.find_elements(
                    By.CSS_SELECTOR, "#challenge-solves-names tr"
                )
                num_solves = len(solves_rows)
                team_data[team_name][challenge_name] = num_solves
                print(f"  [{team_name}] {challenge_name}: {num_solves} solve(s)")

                close_btn = modal.find_element(By.CSS_SELECTOR, "button.btn-close")
                safe_click(close_btn)

                WebDriverWait(agent, 10).until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, "div.modal-body")
                    )
                )

                time.sleep(0.3) 

            except (StaleElementReferenceException, TimeoutException) as e:
                print(f"[{team_name}] Skipping button #{btn_index}: {type(e).__name__}")
                dismiss_any_open_modal()
                continue
            except Exception as e:
                print(f"[{team_name}] Skipping button #{btn_index}: {e}")
                dismiss_any_open_modal()
                continue

    except Exception as e:
        print(f"Skipping category #{cat_index}: {e}")
        continue


with open("challenge_solves.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Team"] + CHALLENGES)
    writer.writeheader()

    for team, challenges in team_data.items():
        row = {"Team": team}
        row.update(challenges)
        writer.writerow(row)

print("CSV saved as 'challenge_solves.csv'")