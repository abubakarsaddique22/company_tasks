# import os
# from PIL import Image

# # 🧭 Base folder where all scraped images are stored
# base_dir = r"C:\Users\dell\Desktop\zameen_scrap\zameen_images"

# # Loop through all subfolders
# for root, dirs, files in os.walk(base_dir):
#     for file in files:
#         file_path = os.path.join(root, file)
        
#         # Check only image files
#         if file.lower().endswith(('.jpg', '.jpeg', '.png')):
#             try:
#                 # Step 1: Remove 0-byte images
#                 if os.path.getsize(file_path) == 0:
#                     print(f"🗑️ Empty file removed: {file_path}")
#                     os.remove(file_path)
#                     continue

#                 # Step 2: Try opening image to detect corruption
#                 with Image.open(file_path) as img:
#                     img.verify()  # check if image is valid
#             except Exception as e:
#                 print(f"⚠️ Corrupted image removed: {file_path}")
#                 os.remove(file_path)



import os
import numpy as np
from PIL import Image, UnidentifiedImageError

# 🧭 Your base directory (update this path)
base_dir = r"C:\Users\dell\Desktop\zameen_scrap\zameen_images"

def is_blank_image(image_path, threshold=0.98):
    """
    Returns True if image is nearly white or single-color.
    threshold = 0.98 means 98%+ pixels same color (white or near-white).
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img_array = np.array(img)
        mean_color = np.mean(img_array, axis=(0, 1)) / 255.0  # normalize to 0–1
        white_ratio = np.mean(np.all(img_array > 240, axis=2))  # how many pixels are nearly white

        # Check if mostly white or flat color
        if white_ratio > threshold or np.std(img_array) < 3:  
            return True
        return False
    except UnidentifiedImageError:
        return True
    except Exception:
        return False

deleted = 0
checked = 0

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(root, file)
            checked += 1

            # Skip if file is 0 bytes
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                deleted += 1
                print(f"🗑️ Deleted empty file: {file_path}")
                continue

            # Check for blank / white image
            if is_blank_image(file_path):
                os.remove(file_path)
                deleted += 1
                print(f"⚪ Deleted blank image: {file_path}")

print(f"\n✅ Cleaning complete! Checked {checked} images, removed {deleted} bad ones.")
