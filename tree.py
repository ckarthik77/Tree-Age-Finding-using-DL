import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO

# Configurations
NUM_IMAGES = 200  # Number of images to download
SEARCH_QUERY = "different tree species high quality"
SEARCH_URL = f"https://www.google.com/search?tbm=isch&q={SEARCH_QUERY.replace(' ', '+')}"

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no browser UI)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open Google Images search
driver.get(SEARCH_URL)
time.sleep(3)

# Scroll down to load more images
for _ in range(5):  
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Find image elements
image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

# Create folder for images
os.makedirs("tree_images", exist_ok=True)

# Prepare CSV for metadata
metadata = []

# Download images
count = 0
for img in image_elements:
    if count >= NUM_IMAGES:
        break
    try:
        img_url = img.get_attribute("src")
        if img_url and img_url.startswith("http"):
            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))

            # Save image
            filename = f"tree_{count+1}.jpg"
            image_path = os.path.join("tree_images", filename)
            image.save(image_path, "JPEG")

            # Save metadata
            metadata.append([filename, img_url, image.size[0], image.size[1]])
            count += 1
            print(f"Downloaded {count}/{NUM_IMAGES} images")
    except Exception as e:
        print(f"Error downloading image {count}: {e}")

# Save metadata as CSV
df = pd.DataFrame(metadata, columns=["Filename", "Image URL", "Width", "Height"])
df.to_csv("tree_images_metadata.csv", index=False)

# Close browser
driver.quit()
print("✅ Image scraping complete! Metadata saved as 'tree_images_metadata.csv'")
