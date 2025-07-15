#I told ChatGPT the logic for this task and took this code from Chatgpt as this was a basic task with minimal logic

from __future__ import annotations

import json
import time
from pathlib import Path
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

# ---------------------------------------------------------------------------
# Optional: Handle UTF-8 printing on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. Selenium setup
# ---------------------------------------------------------------------------
options = Options()

# Uncomment the next line to run Chrome in headless mode
# options.add_argument("--headless=new")

options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

browser = webdriver.Chrome(options=options)
ui_wait = WebDriverWait(browser, 20)

url = "https://soilhealth.dac.gov.in/nutrient-dashboard"
state_district_map: dict[str, list[str]] = {}


def safe_click(locator: tuple, click_desc: str = "") -> None:
    """Wait for element to be clickable, then click. Raises on timeout."""
    elem = ui_wait.until(EC.element_to_be_clickable(locator), f"{click_desc} not clickable")
    elem.click()


def get_list_items(listbox_id: str) -> list[str]:
    """Return all <li> texts inside the given list‑box (already visible)."""
    ul_locator = (By.ID, listbox_id)
    ui_wait.until(EC.visibility_of_element_located(ul_locator), f"{listbox_id} not visible")
    lis = browser.find_elements(By.CSS_SELECTOR, f"#{listbox_id} li")
    return [li.get_attribute("data-id") for li in lis if li.get_attribute("data-id")]


def neutral_click() -> None:
    """Click on page body to close any open dropdown."""
    try:
        browser.find_element(By.TAG_NAME, "body").click()
    except Exception:
        pass
    time.sleep(0.2)

# ---------------------------------------------------------------------------
# 3. Main scraping logic
# ---------------------------------------------------------------------------
try:
    browser.get(url)

    # 3.1 Reveal the filter panel
    safe_click((By.XPATH, "//button[contains(., 'Filter')]"), "'Filter' button")

    # 3.2 Get list of states
    safe_click((By.ID, "State"), "State dropdown")
    states = get_list_items("State-listbox")
    neutral_click()

    if not states:
        raise RuntimeError("No states found – page structure may have changed.")

    # 3.3 For each state, get its districts
    for state in states:
        try:
            # Re-open State dropdown
            safe_click((By.ID, "State"), "State dropdown (loop)")

            # Click the state <li>
            xpath = f"//ul[@id='State-listbox']/li[@data-id='{state}']"   # or "@value='…'"
            safe_click((By.XPATH, xpath), f"state '{state}' option")

            # Open District dropdown
            safe_click((By.ID, "District"), "District dropdown")
            districts = get_list_items("District-listbox")
            neutral_click()

            # Save to dict
            state_district_map[state] = districts or []

            # Print formatted output
            print(f"[OK] {state:<20} -> {len(districts)} districts")
            for d in districts:
                print(f"    - {d}")

        except (TimeoutException,
                StaleElementReferenceException,
                ElementClickInterceptedException) as err:
            print(f"[WARN] Skipped '{state}' due to {type(err).__name__}: {err}")
            neutral_click()
            continue

finally:
    browser.quit()

# ---------------------------------------------------------------------------
# 4. Save to JSON
# ---------------------------------------------------------------------------
out_file = Path("state_district_data.json")
out_file.write_text(json.dumps(state_district_map, indent=2), encoding="utf-8")
print(f"\nScraping completed successfully.\nData written to {out_file.resolve()}")
