# # import requests

# # API_KEY = "AIzaSyDpjaRinwhukWzDW1ZCUCsVtjvcOFqWZoY"
# # query = "pizza shops in Lahore"

# # # Step 1: Search for pizza shops
# # url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
# # response = requests.get(url)
# # data = response.json()

# # if data["status"] != "OK":
# #     print("Error:", data.get("error_message"))
# # else:
# #     for place in data["results"]:
# #         name = place.get("name")
# #         address = place.get("formatted_address")
# #         rating = place.get("rating")
# #         place_id = place.get("place_id")

# #         print(f"\n🍕 {name} — {address} — ⭐ {rating}")
        
# #         # Step 2: Get details (website, phone, etc.)
# #         details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website&key={API_KEY}"
# #         details_data = requests.get(details_url).json()
        
# #         if details_data["status"] == "OK":
# #             details = details_data["result"]
# #             print("📞 Phone:", details.get("formatted_phone_number"))
# #             print("🌐 Website:", details.get("website"))
# #         else:
# #             print("⚠️ Details not found.")


# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
# # from webdriver_manager.chrome import ChromeDriverManager
# # import csv, time

# # # ---------------- SETTINGS ----------------
# # SEARCH_QUERY = "pizza shops in Lahore"
# # OUTPUT_FILE = "lahore_pizza_shops.csv"
# # SCROLL_PAUSE = 2

# # # ---------------- SETUP ----------------
# # options = Options()
# # options.add_argument("--start-maximized")
# # # options.add_argument("--headless")  # uncomment if needed
# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # print(f"🔍 Opening Google Maps for: {SEARCH_QUERY}")
# # driver.get("https://www.google.com/maps")
# # time.sleep(3)

# # # search in box
# # search_box = driver.find_element(By.ID, "searchboxinput")
# # search_box.send_keys(SEARCH_QUERY)
# # search_box.send_keys(Keys.ENTER)

# # # wait for search results
# # WebDriverWait(driver, 20).until(
# #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK"))
# # )
# # print("✅ Search results loaded.")

# # # scroll down to load all results
# # scroll_xpath = '//div[contains(@aria-label,"Results for") and @role="feed"]'
# # scroll_box = driver.find_element(By.XPATH, scroll_xpath)
# # last_height = 0
# # while True:
# #     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
# #     time.sleep(SCROLL_PAUSE)
# #     new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
# #     if new_height == last_height:
# #         break
# #     last_height = new_height

# # time.sleep(2)
# # cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
# # print(f"📦 Found {len(cards)} restaurant cards.")

# # data = []

# # # loop through all cards
# # for i in range(len(cards)):
# #     try:
# #         cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
# #         card = cards[i]
# #         driver.execute_script("arguments[0].scrollIntoView(true);", card)
# #         time.sleep(1)

# #         link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
# #         driver.execute_script("window.open(arguments[0], '_blank');", link)
# #         driver.switch_to.window(driver.window_handles[-1])

# #         # wait for title
# #         WebDriverWait(driver, 15).until(
# #             EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
# #         )

# #         # ----- extract info -----
# #         def safe_find(selector, by=By.CSS_SELECTOR):
# #             try:
# #                 return driver.find_element(by, selector).text
# #             except:
# #                 return "N/A"

# #         title = safe_find("h1.DUwDvf")
# #         rating = safe_find("span.ceNzKf")
# #         try:
# #             reviews = driver.find_element(By.XPATH, "//span[contains(@aria-label,'reviews')]").text
# #         except:
# #             reviews = "N/A"
# #         try:
# #             price = driver.find_element(By.XPATH, "//span[contains(text(),'Rs')]").text
# #         except:
# #             price = "N/A"
# #         category = safe_find("button.DkEaL")
# #         address = safe_find("button[data-item-id='address']")
# #         phone = safe_find("button[data-item-id='phone']")
# #         website = safe_find("a[data-item-id='authority']")

# #         data.append({
# #             "Name": title,
# #             "Rating": rating,
# #             "Reviews": reviews,
# #             "Price": price,
# #             "Category": category,
# #             "Phone": phone,
# #             "Address": address,
# #             "Website": website,
# #         })

# #         print(f"✅ {i+1}. {title}")
# #         driver.close()
# #         driver.switch_to.window(driver.window_handles[0])
# #         time.sleep(2)

# #     except Exception as e:
# #         print(f"⚠️ Error on item {i+1}: {e}")
# #         try:
# #             driver.close()
# #             driver.switch_to.window(driver.window_handles[0])
# #         except:
# #             pass
# #         continue

# # # ---------------- SAVE ----------------
# # if data:
# #     with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
# #         writer = csv.DictWriter(f, fieldnames=data[0].keys())
# #         writer.writeheader()
# #         writer.writerows(data)
# #     print(f"\n💾 Saved {len(data)} restaurants to {OUTPUT_FILE}")
# # else:
# #     print("\n❌ No data collected.")

# # driver.quit()
# # print("🎉 Done!")

# # ============================================================
# # 🧩 GOOGLE MAPS RESTAURANT SCRAPER (USING SELENIUM)
# # ============================================================
# # TASK:
# #   1️⃣ Search for “pizza shops in Lahore”
# #   2️⃣ Scroll to load all visible results
# #   3️⃣ Click each shop → open in new tab
# #   4️⃣ Extract details (name, rating, address, phone, website)
# #   5️⃣ Save all data to CSV file
# #
# # ⚙️ TOOLS USED:
# #   - Selenium (for browser automation)
# #   - webdriver_manager (for auto ChromeDriver)
# #   - CSV module (for data saving)
# #
# # 🧑‍💻 WRITTEN BY: ChatGPT (GPT-5)
# # ============================================================

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from webdriver_manager.chrome import ChromeDriverManager
# import csv
# import time


# # ============================================================
# # 🔧 CONFIGURATION
# # ============================================================

# SEARCH_QUERY = "pizza shops in Lahore"   # Your search keyword
# OUTPUT_FILE = "lahore_pizza_shops.csv"   # CSV output file name
# SCROLL_PAUSE = 2                         # Wait time while scrolling

# # Chrome setup (optional: enable headless mode)
# options = Options()
# options.add_argument("--start-maximized")
# # options.add_argument("--headless")     # Uncomment if you don’t want browser UI

# # Create Chrome driver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# # ============================================================
# # 🔍 STEP 1: OPEN GOOGLE MAPS & SEARCH
# # ============================================================

# print(f"🔍 Opening Google Maps for: {SEARCH_QUERY}")
# driver.get("https://www.google.com/maps")
# time.sleep(3)  # Wait for map homepage to fully load

# # Locate search box and enter the query
# search_box = driver.find_element(By.ID, "searchboxinput")
# search_box.send_keys(SEARCH_QUERY)
# search_box.send_keys(Keys.ENTER)

# # Wait for the search results (shop list on the left) to appear
# WebDriverWait(driver, 25).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK"))
# )
# print("✅ Search results loaded successfully.")


# # ============================================================
# # 📜 STEP 2: SCROLL TO LOAD ALL RESULTS
# # ============================================================

# scroll_xpath = '//div[contains(@aria-label,"Results for") and @role="feed"]'
# scroll_box = driver.find_element(By.XPATH, scroll_xpath)

# last_height = 0
# while True:
#     # Scroll the sidebar down
#     driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
#     time.sleep(SCROLL_PAUSE)

#     # Measure height — if unchanged, we reached the end
#     new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
#     if new_height == last_height:
#         break
#     last_height = new_height

# print("📜 Finished scrolling all visible shops.\n")


# # ============================================================
# # 📦 STEP 3: COLLECT ALL SHOP CARDS
# # ============================================================

# cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
# print(f"📦 Found {len(cards)} restaurant listings.\n")

# data = []  # To store final results


# # ============================================================
# # 🌀 STEP 4: LOOP THROUGH EACH SHOP & EXTRACT DETAILS
# # ============================================================

# for i in range(len(cards)):
#     try:
#         # Re-locate cards each iteration (DOM reloads when we click)
#         cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
#         card = cards[i]

#         # Scroll card into view (to ensure it’s clickable)
#         driver.execute_script("arguments[0].scrollIntoView(true);", card)
#         time.sleep(1)

#         # Extract link to detail page
#         link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

#         # Open shop in a new browser tab
#         driver.execute_script("window.open(arguments[0], '_blank');", link)
#         driver.switch_to.window(driver.window_handles[-1])  # Switch focus to new tab

#         # Wait until shop detail page fully loads
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
#         )

#         # =====================================================
#         # 🧾 STEP 5: EXTRACT EACH FIELD WITH INDIVIDUAL TRY/EXCEPT
#         # =====================================================

#         # --- Title / Name ---
#         try:
#             name = driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text.strip()
#         except:
#             name = "N/A"

#         # --- Rating (4.5 etc.) ---
#         try:
#             rating = driver.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']").text.strip()
#         except:
#             rating = "N/A"

#         # --- Category (Pizza restaurant etc.) ---
#         try:
#             category = driver.find_element(By.CSS_SELECTOR, "button.DkEaL").text.strip()
#         except:
#             category = "N/A"

#         # --- Address ---
#         # try:
#         #     address = driver.find_element(
#         #         By.CSS_SELECTOR, "div.Io6YTe.fontBodyMedium.kR99db.fdkmkc"
#         #     ).text.strip()
#         # except:
#         #     address = "N/A"

#         # --- Phone ---
#         # try:
#         #     phone = driver.find_element(
#         #         By.XPATH,
#         #         "//div[contains(@class,'AeaXub')]//div[contains(@class,'rogA2c')]/div[contains(@class,'Io6YTe')]"
#         #     ).text.strip()
#         # except:
#         #     phone = "N/A"

#         # try:
#         #     # Try to find the phone number div
#         #     phone_element = driver.find_element(By.CLASS_NAME, 'Io6YTe')
#         #     phone_number = phone_element.text.strip()
#         #     print("Phone Number:", phone_number)
#         # except NoSuchElementException:
#         #     print("Phone number not found!")

#         # --- Extract addresses ---
#         addresses = []
#         try:
#             # Find all divs that look like addresses (they usually have the icon wrapper)
#             address_blocks = driver.find_elements(By.CSS_SELECTOR, "div.AeaXub div.rogA2c")
#             for block in address_blocks:
#                 text = block.find_element(By.CLASS_NAME, "Io6YTe").text.strip()
#                 # Filter only addresses (e.g., check if it contains comma or number)
#                 if "," in text:  
#                     addresses.append(text)
#         except NoSuchElementException:
#             print("No addresses found.")

#         # --- Extract phone numbers ---
#         phones = []
#         try:
#             # Either standalone phone divs or inside the same AeaXub blocks
#             phone_blocks = driver.find_elements(By.CSS_SELECTOR, "div.Io6YTe")
#             for block in phone_blocks:
#                 text = block.text.strip()
#                 # Simple filter: if text starts with +92 or any number pattern
#                 if text.startswith("+92") and text not in phones:
#                     phones.append(text)
#         except NoSuchElementException:
#             print("No phone numbers found.")
#         # --- Website ---
#         try:
#             website = driver.find_element(
#                 By.XPATH,
#                 "//div[contains(@class,'AeaXub')]//div[contains(@class,'rogA2c ITvuef')]/div[contains(@class,'Io6YTe')]"
#             ).text.strip()
#         except:
#             website = "N/A"

#         # =====================================================
#         # 🖨️ PRINT TO CONSOLE
#         # =====================================================

#         print(f"🍕 {i+1}. {name}")
#         print(f"   ⭐ Rating: {rating}")
#         print(f"   📂 Category: {category}")
#         print(f"   📍 Address: {addresses}")
#         print(f"   ☎️ Phone: {phones}")
#         print(f"   🌐 Website: {website}")
#         print("------------------------------------------------------")

#         # =====================================================
#         # 💾 SAVE RECORD IN MEMORY
#         # =====================================================

#         data.append({
#             "Name": name,
#             "Rating": rating,
#             "Category": category,
#             "Address": addresses,
#             "Phone": phones,
#             "Website": website
#         })

#         # Close this shop’s tab and return to main results tab
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(2)

#     except Exception as e:
#         print(f"⚠️ Skipping shop {i+1} due to error: {e}")
#         try:
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])
#         except:
#             pass
#         continue


# # ============================================================
# # 💾 STEP 6: WRITE RESULTS TO CSV FILE
# # ============================================================

# if data:
#     with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=data[0].keys())
#         writer.writeheader()
#         writer.writerows(data)
#     print(f"\n💾 Saved {len(data)} records to {OUTPUT_FILE}")
# else:
#     print("\n❌ No data extracted.")

# # ============================================================
# # 🏁 STEP 7: CLEANUP
# # ============================================================
# driver.quit()
# print("🎉 Task complete! All data saved successfully.")



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import re

# ================= CONFIG =================
SEARCH_QUERY = "pizza shops in Lahore"
OUTPUT_FILE = "lahore_pizza_shops.csv"
SCROLL_PAUSE = 2

options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment to run headless

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ================= OPEN MAPS & SEARCH =================
driver.get("https://www.google.com/maps")
time.sleep(3)
search_box = driver.find_element(By.ID, "searchboxinput")
search_box.send_keys(SEARCH_QUERY)
search_box.send_keys(Keys.ENTER)

WebDriverWait(driver, 25).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK"))
)
print("✅ Search results loaded.")

# ================= SCROLL TO LOAD =================
scroll_box = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Results for") and @role="feed"]')
last_height = 0
while True:
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box)
    time.sleep(SCROLL_PAUSE)
    new_height = driver.execute_script("return arguments[0].scrollHeight", scroll_box)
    if new_height == last_height:
        break
    last_height = new_height

# ================= COLLECT CARDS =================
cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
print(f"📦 Found {len(cards)} shops.")
data = []

# ================= LOOP THROUGH CARDS =================
for i in range(len(cards)):
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
        card = cards[i]
        driver.execute_script("arguments[0].scrollIntoView(true);", card)
        time.sleep(1)

        link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.execute_script("window.open(arguments[0], '_blank');", link)
        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.DUwDvf"))
        )

        # --- Helper function ---
        def safe_text(by, selector):
            try:
                return driver.find_element(by, selector).text.strip()
            except:
                return "N/A"

        name = safe_text(By.CSS_SELECTOR, "h1.DUwDvf")
        # rating = safe_text(By.CSS_SELECTOR, "span[aria-hidden='true']")
        category = safe_text(By.CSS_SELECTOR, "button.DkEaL")
        # --- Extract rating as numeric only ---
        try:
        # Locate the span that contains numeric rating
            rating_span = driver.find_element(By.CSS_SELECTOR, "div.F7nice span[aria-hidden='true']")
            rating_text = rating_span.text.strip()
            
            # Use regex to extract only digits/decimal
            match = re.match(r'^\d+(\.\d+)?$', rating_text)
            if match:
                rating = match.group()
            else:
                rating = "N/A"
        except:
            rating = "N/A"


        try:
            # Locate the span that contains numeric rating
            rating_span = driver.find_element(By.CSS_SELECTOR, "div.F7nice span[aria-hidden='true']")
            rating_text = rating_span.text.strip()
            
            # Use regex to extract only digits/decimal
            match = re.match(r'^\d+(\.\d+)?$', rating_text)
            if match:
                rating = match.group()
            else:
                rating = "N/A"
        except:
            rating = "N/A"

        print("⭐ Rating:", rating)


        # --- Extract address & phone using pattern matching ---
        address = "N/A"
        phone = "N/A"
        try:
            blocks = driver.find_elements(By.CSS_SELECTOR, "div.AeaXub > div.rogA2c > div.Io6YTe")
            for b in blocks:
                text = b.text.strip()
                # If contains comma, treat as address
                if "," in text and address == "N/A":
                    address = text
                # If matches phone pattern (starts with +92 or contains digits)
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

        # --- Print & Save ---
        print(f"{i+1}. {name} | ⭐ {rating} | 📍 {address} | ☎️ {phone} | 🌐 {website}")

        data.append({
            "Name": name,
            "Rating": rating,
            "Category": category,
            "Address": address,
            "Phone": phone,
            "Website": website
        })

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Skipping shop {i+1}: {e}")
        try:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
        continue

# ================= SAVE TO CSV =================
if data:
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"\n💾 Saved {len(data)} records to {OUTPUT_FILE}")
else:
    print("\n❌ No data extracted.")

driver.quit()
print("🎉 Task complete!")
