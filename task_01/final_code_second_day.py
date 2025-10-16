from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os 
import requests

HEADLESS = False       # Set to True to hide browser
PAUSE = 3.5
MAX_PAGES = 1          # Number of pages to scrape


# ---------------------- Helper Pause ----------------------
def slow_pause(multiplier=1.0):
    time.sleep(PAUSE * multiplier)


# ---------------------- SETUP DRIVER ----------------------
def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--renderer-process-limit=2")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.set_window_size(1200, 900)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20)
    return driver


# ---------------------- DOWNLOAD IMAGE ----------------------
def download_image(url, filename, folder_name):
    """
    Downloads image into 'zameen_images/<folder_name>' automatically created folder.
    Returns clickable local path for Excel.
    """
    try:
        base_folder = r"C:\Users\dell\Desktop\zameen_scrap\zameen_images"
        folder_path = os.path.join(base_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)  # ✅ Auto-create folder

        safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
        filepath = os.path.join(folder_path, safe_name)

        res = requests.get(url, timeout=80)
        if res.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(res.content)
            abs_path = os.path.abspath(filepath)
            return f"file:///{abs_path.replace('\\', '/')}"
        else:
            print(f"⚠️ Failed to download ({res.status_code}): {url}")
            return None
    except Exception as e:
        print(f"⚠️ Error downloading image: {e}")
        return None


# ---------------------- SCRAPER FUNCTION ----------------------
def scrape_zameen():
    driver = create_driver(HEADLESS)
    wait = WebDriverWait(driver, 25)
    properties = []

    try:
        print("🌐 Opening Zameen homepage...")
        try:
            driver.get("https://www.zameen.com/")
        except TimeoutException:
            print("⚠️ Homepage load timeout, forcing stop...")
            driver.execute_script("window.stop();")
        slow_pause(2)

        # Step 1: Select Lahore
        print("🏙️ Selecting Lahore...")
        city_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[name='City'] div[role='button']")))
        driver.execute_script("arguments[0].click();", city_dropdown)
        slow_pause(1.5)
        lahore_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Lahore']")))
        driver.execute_script("arguments[0].click();", lahore_button)
        slow_pause(2)
        print("✅ Lahore selected")

        # Step 2: Click Find button
        find_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Find button']")))
        driver.execute_script("arguments[0].click();", find_button)
        print("🔍 Find button clicked")
        slow_pause(3)

        # Step 3: Loop through pages
        for page_num in range(1, MAX_PAGES + 1):
            print(f"\n📄 Scraping page {page_num}/{MAX_PAGES}...")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.a37d52f0[role='article']")))
            property_cards = driver.find_elements(By.CSS_SELECTOR, "li.a37d52f0[role='article']")
            print(f"🎯 Found {len(property_cards)} property cards")

            for index in range(min(5, len(property_cards))):
                try:
                    print(f"\n➡️ Opening property {index + 1}...")
                    property_cards = driver.find_elements(By.CSS_SELECTOR, "li.a37d52f0[role='article']")
                    driver.execute_script("arguments[0].scrollIntoView(true);", property_cards[index])
                    slow_pause(1)

                    # ✅ Automatically create subfolder for this card
                    subfolder = f"page{page_num}_card{index+1}"

                    # Front Image
                    try:
                        img_elem = property_cards[index].find_element(By.CSS_SELECTOR, "div._317a748d img[aria-label='Listing photo']")
                        front_image = img_elem.get_attribute("src")
                    except:
                        front_image = None

                    image_path = None
                    if front_image:
                        image_path = download_image(front_image, "front.jpg", subfolder)

                    # Open property detail
                    link_elem = property_cards[index].find_element(By.CSS_SELECTOR, "a[aria-label='Listing link']")
                    driver.execute_script("arguments[0].click();", link_elem)
                    slow_pause(3)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.aea614fd")))

                    info = {}
                    try:
                        info["Title"] = driver.find_element(By.CSS_SELECTOR, "h1.aea614fd").text.strip()
                    except:
                        info["Title"] = "N/A"

                    cards = driver.find_elements(By.CSS_SELECTOR, "div._61c347da")  # parent div of price

                    for card in cards:
                        try:
                            price_element = card.find_element(By.CSS_SELECTOR, "span[aria-label='Price']")
                            price = price_element.text.strip()
                            info['Price'] = price 
                        except NoSuchElementException:
                            price = ""

                        print(price)

                    # Details
                    details = {}
                    try:
                        detail_items = driver.find_elements(By.CSS_SELECTOR, "div._83bb17d1 ul li")
                        for li in detail_items:
                            key = li.find_element(By.CSS_SELECTOR, "span.ed0db22a").text.strip()
                            value = li.find_element(By.CSS_SELECTOR, "span._2fdf7fc5").text.strip()
                            details[key] = value
                    except:
                        pass

                    # Extra Features
                    extra_features = {}
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                        slow_pause(1.5)
                        feature_spans = driver.find_elements(By.CSS_SELECTOR, "span._9121cbf9")
                        for span in feature_spans:
                            text = span.text.strip()
                            for feature in ["Built in year", "Parking Spaces", "Floor", "Servant Quarters", "Kitchens"]:
                                if text.startswith(feature):
                                    value = text.split(":", 1)[1].strip() if ":" in text else "Yes"
                                    extra_features[feature] = value
                    except:
                        pass

                    # ✅ Download ALL images inside property page
                    all_imgs = []
                    try:
                        img_elems = driver.find_elements(By.CSS_SELECTOR, "img[src*='zameen']")
                        for i, img in enumerate(img_elems, start=1):
                            src = img.get_attribute("src")
                            if src and src not in all_imgs:
                                path = download_image(src, f"img_{i}.jpg", subfolder)
                                if path:
                                    all_imgs.append(path)
                    except Exception as e:
                        print(f"⚠️ Image extraction error: {e}")

                    # Add all info
                    info.update({
                        "Type": details.get("Type", "N/A"),
                        "Location": details.get("Location", "N/A"),
                        "Bath(s)": details.get("Bath(s)", "N/A"),
                        "Area": details.get("Area", "N/A"),
                        "Purpose": details.get("Purpose", "N/A"),
                        "Bedroom(s)": details.get("Bedroom(s)", "N/A"),
                        "Added": details.get("Added", "N/A"),
                        "Built in year": extra_features.get("Built in year", "N/A"),
                        "Parking Spaces": extra_features.get("Parking Spaces", "N/A"),
                        "Floor": extra_features.get("Floor", "N/A"),
                        "Servant Quarters": extra_features.get("Servant Quarters", "N/A"),
                        "Kitchens": extra_features.get("Kitchens", "N/A"),
                        "Front_Image": image_path if image_path else "N/A",
                        "Other_Images": ", ".join(all_imgs) if all_imgs else "N/A",
                        "URL": driver.current_url,
                    })

                    properties.append(info)
                    print(f"✅ Scraped: {info['Title'][:60]} | {info['Price']} | {len(all_imgs)} imgs")

                    # Go back
                    try:
                        driver.back()
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.a37d52f0[role='article']")))
                    except TimeoutException:
                        driver.execute_script("window.stop();")
                    slow_pause(2.5)

                except Exception as e:
                    print(f"❌ Error scraping property {index + 1}: {e}")
                    try:
                        driver.back()
                    except:
                        pass
                    slow_pause(1)
                    continue

            # Next page
            try:
                print(f"➡️ Going to next page ({page_num + 1})...")
                next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Next']")))
                driver.execute_script("arguments[0].click();", next_page)
                slow_pause(4)
            except:
                print("🚫 No next page found.")
                break

        # Save Data
        print("\n💾 Saving data...")
        df = pd.DataFrame(properties)
        df.to_excel("zameen_properties.xlsx", index=False)
        print("✅ Saved: 'zameen_properties.xlsx'")

    except Exception as e:
        print(f"❌ Fatal error: {e}")

    finally:
        input("Press Enter to close browser...")
        driver.quit()
        print("🧹 Browser closed.")


if __name__ == "__main__":
    scrape_zameen()