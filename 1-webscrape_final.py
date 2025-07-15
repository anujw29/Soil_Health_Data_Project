import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, InvalidSessionIdException

#Initial setup
download_folder = os.path.abspath("Downloads/Anuj/CSVs")
os.makedirs(download_folder, exist_ok=True)
log_path = os.path.join(download_folder, "log.txt")

# Initialize browser and ui_wait as global variables
browser = None
ui_wait = None

# Main code starts here(I have tried to include many edge cases I noticed as my code failed many times, so had to reiterate with the cases, I also tried this code on my friend's laptop and worked well, there is still a chance that I might have missed something)
def launch_browser():
    global browser, ui_wait
    if browser is not None:
        browser.quit()
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(options=chrome_options)
    ui_wait = WebDriverWait(browser, 20)

#Code for logging messages(The messages' format is [OK] for success, [SKIP] for skipped, and [ERROR] for errors which is inspired from Chatgpt)

def log(message):
    print(message)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def open_dashboard():
    global browser, ui_wait
    try:
        browser.get("https://soilhealth.dac.gov.in/nutrient-dashboard")
        ui_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Table View')]"))).click()
        ui_wait.until(EC.element_to_be_clickable((By.ID, "Cycle"))).click()
        ui_wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), '2023-24')]"))).click()
        ui_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Filter')]"))).click()
    except (TimeoutException, InvalidSessionIdException) as e:
        log(f"[ERROR] Failed to initialize dashboard: {str(e)}. Restarting browser...")
        launch_browser()
        open_dashboard()

#Makes list of all options in a dropdown(but doesen't click it right then)(I tried to create something which makes a list and then selects the first option, but got some bugs maybe because I was using the 'keys' library for it)
def get_all_options(input_id):
    global browser, ui_wait
    try:
        input_box = ui_wait.until(EC.element_to_be_clickable((By.ID, input_id)))
        input_box.click()
        time.sleep(1)
        options = ui_wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li")))
        items = [opt.text.strip() for opt in options if opt.text.strip()]
        input_box.send_keys(Keys.ESCAPE)
        return items
    except (TimeoutException, InvalidSessionIdException) as e:
        log(f"[ERROR] Failed to get options for {input_id}: {str(e)}. Restarting browser...")
        launch_browser()
        open_dashboard()
        return []

def select_autocomplete_value(input_id, value, next_id=None):
    global browser, ui_wait
    try:
        input_box = ui_wait.until(EC.presence_of_element_located((By.ID, input_id)))
        input_box = ui_wait.until(EC.element_to_be_clickable((By.ID, input_id)))
        input_box.clear()
        input_box.send_keys(value)
        time.sleep(1)
        input_box.send_keys(Keys.ARROW_DOWN)
        input_box.send_keys(Keys.ENTER)
        browser.find_element(By.TAG_NAME, "body").click()
        time.sleep(1.5)
        if next_id:
            ui_wait.until(EC.presence_of_element_located((By.ID, next_id)))
    except (TimeoutException, InvalidSessionIdException) as e:
        log(f"[ERROR] Failed to select {value} for {input_id}: {str(e)}. Restarting browser...")
        launch_browser()
        open_dashboard()

def clean_filename(name):
    return name.replace("&", "and").replace(" ", "_").replace("/", "-")

def ui_wait_for_download(old_files, timeout=30):
    start_time = time.time()
    while True:
        new_files = os.listdir(download_folder)
        added = list(set(new_files) - set(old_files))
        for f in added:
            if not f.endswith(".crdownload"):
                return f
        if time.time() - start_time > timeout:
            return None
        time.sleep(1)

#Main code(chrome opens, selects state, district, block, and downloads CSVs)

launch_browser()
open_dashboard()
state_list = get_all_options("State")

for state in state_list:
    try:
        open_dashboard()
        select_autocomplete_value("State", state, next_id="District")
        district_list = get_all_options("District")
    except Exception as e:
        log(f"[SKIP] Failed to load districts for state: {state} - {str(e)}")
        continue

    for district in district_list:
        try:
            open_dashboard()
            select_autocomplete_value("State", state, next_id="District")
            select_autocomplete_value("District", district, next_id="Block")
            block_list = get_all_options("Block")
        except Exception as e:
            log(f"[SKIP] Failed to load blocks for: {state} > {district} - {str(e)}")
            continue

        block_index = 0
        while block_index < len(block_list):
            block = block_list[block_index]
            try:
                log(f"[TRY] {state} > {district} > {block}")
                select_autocomplete_value("Block", block)

                # Try to close filter
                try:
                    ui_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Close')]"))).click()
                    time.sleep(1)
                except Exception as e:
                    log(f"[SKIP] 'Close' button missing: {state} > {district} > {block} - {str(e)}")
                    block_index += 1
                    continue

                # Check data availability
                try:
                    # Check if table has data or "No Rows To Show" message
                    no_data = browser.find_elements(By.XPATH, "//div[contains(text(), 'No Rows To Show')]")
                    if no_data:
                        log(f"[SKIP] No data available (No Rows To Show): {state} > {district} > {block}")
                        block_index += 1
                        # Reinitialize dashboard and reselect state and district for next block
                        open_dashboard()
                        select_autocomplete_value("State", state, next_id="District")
                        select_autocomplete_value("District", district, next_id="Block")
                        continue

                    # Check if Export button is clickable
                    export_button = ui_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Export')]")))
                    old_files = os.listdir(download_folder)
                    export_button.click()
                    ui_wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'CSV')]"))).click()

                    # Wait for download
                    downloaded = ui_wait_for_download(old_files)
                    if downloaded:
                        safe_name = clean_filename(f"{state}{district}{block}") + ".csv"
                        shutil.move(os.path.join(download_folder, downloaded), os.path.join(download_folder, safe_name))
                        log(f"[OK] Saved: {safe_name}")
                    else:
                        log(f"[FAIL] Download timeout: {state} > {district} > {block}")
                except (TimeoutException, ElementClickInterceptedException):
                    log(f"[SKIP] Export button disabled or no data: {state} > {district} > {block}")
                    block_index += 1
                    # Reinitialize dashboard and reselect state and district for next block
                    open_dashboard()
                    select_autocomplete_value("State", state, next_id="District")
                    select_autocomplete_value("District", district, next_id="Block")
                    continue

            except (InvalidSessionIdException, TimeoutException) as e:
                log(f"[ERROR] Session error on: {state} > {district} > {block} - {str(e)}. Restarting browser...")
                launch_browser()
                open_dashboard()
                # Reinitialize state and district to continue from the current block
                try:
                    select_autocomplete_value("State", state, next_id="District")
                    select_autocomplete_value("District", district, next_id="Block")
                except Exception as e:
                    log(f"[SKIP] Could not reset for block: {state} > {district} > {block} - {str(e)}")
                    break  # Move to next district

            except Exception as e:
                log(f"[SKIP] Error on: {state} > {district} > {block} - {str(e)}")

            # Move to next block
            block_index += 1

            # Refresh and reselect if more blocks(I have tried to include edge cases)
            if block_index < len(block_list):
                try:
                    open_dashboard()
                    select_autocomplete_value("State", state, next_id="District")
                    select_autocomplete_value("District", district, next_id="Block")
                except Exception as e:
                    log(f"[SKIP] Could not reset for next block after: {state} > {district} - {str(e)}")
                    break  # move to next district

browser.quit()
