# ============================================================
# 🧩 GOOGLE MAPS MULTI-AREA SCRAPER (Stable Version)
# Extracts pizza shops in Lahore, Pakistan from Google Maps
# ============================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import csv, time, re, random, os

# ============================================================
# 🔧 CONFIGURATION
# ============================================================

AREAS = [
    "pizza shops in Gulberg Lahore",
    "pizza shops in DHA Lahore",
    "pizza shops in Model Town Lahore",
    "pizza shops in Johar Town Lahore",
    "pizza shops in Bahria Town Lahore",
    "pizza shops in Allama Iqbal Town Lahore",
    "pizza shops in Wapda Town Lahore",
]

OUTPUT_FILE = "lahore_pizza_shops.csv"
SCROLL_PAUSE = 3  # Wait between scrolls (in seconds)

# Chrome setup
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment to run without UI
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_data = []  # Final data for all areas

# ============================================================
# 🔍 FUNCTION: SCRAPE ONE AREA
# ============================================================
def scrape_area(area_query):
    print(f"\n🔍 Searching: {area_query}")
    driver.get("https://www.google.com/maps")
    time.sleep(4)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(area_query)
    search_box.send_keys(Keys.ENTER)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK"))
        )
        print("✅ Search results loaded.")
    except TimeoutException:
        print("⚠️ Search results not loaded, skipping area.")
        return []

    # Scroll sidebar until no new results
    try:
        scroll_box = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Results for") and @role="feed"]')
    except:
        print("⚠️ Scroll box not found.")
        return []

    previous_count = 0
    same_count_times = 0
    max_wait_cycles = 8

    while True:
        cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
        time.sleep(random.uniform(SCROLL_PAUSE, SCROLL_PAUSE + 2))

        new_count = len(driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK"))
        if new_count == previous_count:
            same_count_times += 1
        else:
            same_count_times = 0
            previous_count = new_count

        if same_count_times >= max_wait_cycles:
            break

    print(f"📦 Found {previous_count} visible shop cards.")

    area_data = []
    cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")

    for i in range(len(cards)):
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
            card = cards[i]
            driver.execute_script("arguments[0].scrollIntoView(true);", card)
            time.sleep(1)

            # Try to get the clickable link
            try:
                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                if not link:
                    print(f"⚠️ Card {i+1} has no link — skipped.")
                    continue
            except:
                print(f"⚠️ Card {i+1} not clickable — skipped.")
                continue

            # Open detail page
            driver.execute_script("window.open(arguments[0], '_blank');", link)
            driver.switch_to.window(driver.window_handles[-1])

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
            )

            # Helper
            def safe_text(by, selector):
                try:
                    return driver.find_element(by, selector).text.strip()
                except:
                    return "N/A"

            name = safe_text(By.CSS_SELECTOR, "h1.DUwDvf")
            category = safe_text(By.CSS_SELECTOR, "button.DkEaL")

            # --- Rating ---
            try:
                rating_span = driver.find_element(By.CSS_SELECTOR, "div.F7nice span[aria-hidden='true']")
                rating_text = rating_span.text.strip()
                match = re.match(r'^\d+(\.\d+)?$', rating_text)
                rating = match.group() if match else "N/A"
            except:
                rating = "N/A"

            # --- Address & Phone ---
            address = "N/A"
            phone = "N/A"
            try:
                blocks = driver.find_elements(By.CSS_SELECTOR, "div.AeaXub > div.rogA2c > div.Io6YTe")
                for b in blocks:
                    text = b.text.strip()
                    if "," in text and address == "N/A":
                        address = text
                    elif (re.match(r"(\+92|0)\d+", text) or re.search(r"\d", text)) and phone == "N/A":
                        phone = text
            except:
                pass

            # --- Website ---
            website = "N/A"
            try:
                website_elem = driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
                website = website_elem.get_attribute("href")
            except:
                pass

            print(f"🍕 {i+1}. {name} | ⭐ {rating} | 📍 {address} | ☎️ {phone} website : {website}")

            area_data.append({
                "Area": area_query,
                "Name": name,
                "Rating": rating,
                "Category": category,
                "Address": address,
                "Phone": phone,
                "Website": website
            })

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(1.5, 3.0))

        except Exception as e:
            print(f"⚠️ Skipping shop {i+1}: {e}")
            try:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                pass
            continue

    return area_data


# ============================================================
# 🚀 MAIN EXECUTION LOOP
# ============================================================
for area in AREAS:
    result = scrape_area(area)
    all_data.extend(result)

# ============================================================
# 💾 SAVE TO CSV
# ============================================================
if all_data:
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)
    print(f"\n💾 Saved total {len(all_data)} shops to {OUTPUT_FILE}")
else:
    print("\n❌ No data collected.")

driver.quit()
print("🎉 Task complete! All Lahore areas scraped successfully.")
