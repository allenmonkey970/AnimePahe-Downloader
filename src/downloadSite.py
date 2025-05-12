import os
import re
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

DOWNLOAD_DIR = os.path.abspath("downloads")

def extract_download_urls(filename):
    url_pattern = re.compile(r'https?://[^\s]+')
    download_urls = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().lower().startswith("page:"):
                continue
            urls = url_pattern.findall(line)
            download_urls.extend(urls)
    return download_urls

def get_final_kwik_link(driver, url):
    driver.get(url)
    final_href = None
    for _ in range(20):
        time.sleep(1)
        redirect_buttons = driver.find_elements(By.CSS_SELECTOR, "a.redirect")
        if redirect_buttons:
            href = redirect_buttons[0].get_attribute("href")
            if href and not href.startswith("#") and "kwik.si" in href:
                final_href = href
                break
    return final_href

def wait_for_new_file(before_files, timeout=120):
    for _ in range(timeout):
        after_files = set(os.listdir(DOWNLOAD_DIR))
        new_files = after_files - before_files
        if new_files:
            return new_files.pop()
        time.sleep(1)
    return None

def handle_kwik_download(driver, kwik_url):
    driver.get(kwik_url)
    time.sleep(5)
    try:
        # Find the download form and button
        form = driver.find_element(By.XPATH, '//form[contains(@action, "/d/")]')
        button = form.find_element(By.TAG_NAME, "button")

        # List files in download dir before clicking
        before_files = set(os.listdir(DOWNLOAD_DIR))

        ActionChains(driver).move_to_element(button).click(button).perform()
        print("Clicked download button. Waiting for file...")

        # Wait for new file to appear in download dir
        downloaded_file = wait_for_new_file(before_files)
        if downloaded_file:
            print(f"Downloaded file: {os.path.join(DOWNLOAD_DIR, downloaded_file)}")
        else:
            print("No new file detected in download directory. You may need to solve a captcha in the browser window.")
            input("Press Enter after download completes or captcha is solved...")
    except Exception as e:
        print(f"Could not complete download automatically: {e}")

def main():
    filename = input("Enter the path to your websites txt file (e.g. websites.txt): ").strip()
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    download_urls = extract_download_urls(filename)
    if not download_urls:
        print("No valid download URLs found in the file.")
        return

    print(f"\nFound {len(download_urls)} valid download URLs. Launching browser...\n")
    options = uc.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = uc.Chrome(options=options)

    for idx, url in enumerate(download_urls, 1):
        print(f"\n[{idx}/{len(download_urls)}] Fetching: {url}")
        kwik_url = get_final_kwik_link(driver, url)
        if not kwik_url:
            print("Could not get redirect link, skipping...")
            continue
        print(f"Redirected to: {kwik_url}")

        handle_kwik_download(driver, kwik_url)
        print("If the file hasn't appeared, check the open browser window for a captcha or further instructions.")

    input("Press Enter to close the browser when all downloads are complete.")
    driver.quit()
    print(f"\nDone. All files saved to: {DOWNLOAD_DIR}")

if __name__ == "__main__":
    main()