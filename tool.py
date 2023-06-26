from selenium import webdriver
import time
import os
import requests
import io
from PIL import Image
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


num_imgs = 1000
# Set up webdriver
driver = webdriver.Chrome()
# JavaScript code to take array output with elements are links of images
script = """
function myFunction() {
	'use strict';
	const imageElements = document.querySelectorAll('img');
	const imageUrls = Array.from(imageElements).map(img => img.src);
	console.log(imageUrls);
	return imageUrls;
};
return myFunction();
setInterval(myFunction, 1000);
"""
# Create folder to save images
folder_path_AI_generated_images = "AI_generated_images"
if not os.path.exists(folder_path_AI_generated_images):
    os.makedirs(folder_path_AI_generated_images)

folder_path_true_images = "true images"
if not os.path.exists(folder_path_true_images):
    os.makedirs(folder_path_true_images)

# Function download images
def download(filtered_urls,folder_path):
	for i, url in enumerate(filtered_urls):
		response = requests.get(url)
		img = Image.open(io.BytesIO(response.content))
		img = img.resize((300, 300), Image.ANTIALIAS)  # resize image
		filename = os.path.join(folder_path, f'image_{i+1}.jpg')
		img.save(filename)  # save resize image
		print(f'Save image_{i+1}.jpg')

	print(f'All images downloaded and resized in {folder_path} successfully!')


# Open web
driver.get("https://generated.photos/faces")

# Loop
while True:
	# Run JavaScript code and save output to imageUrls variable
    image_urls = driver.execute_script(script)
    print(len(image_urls))
	# I check with num_imgs + 100 because the elements of output console sometime is not the correct link of image I need
	# So I take more links that I need to avoid this issue
    if len(image_urls) > num_imgs + 100:
        break

    else:
		# Scroll the web page to the bottom
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(1)
        # Press button Load more
        load_more_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "loadmore-btn")))
        driver.execute_script("arguments[0].click();", load_more_btn)
	# Delay
    time.sleep(1)
# Take array to save values
filtered_urls_AI = []
for url in image_urls:
    if url.startswith('https://images.generated.photos'):
        filtered_urls_AI.append(url)
	# This code will take the number of link images we need
    if len(filtered_urls_AI) == num_imgs:
        break
# Download images
download(filtered_urls_AI,folder_path_AI_generated_images)




# Open web
driver.get("https://www.pexels.com/vi-vn/tim-kiem/cat/")

# Loop
while True:
    # Run JavaScript code and save output to imageUrls variable
    image_urls = driver.execute_script(script)
    print(len(image_urls))
	# I check with num_imgs + 100 because the elements of output console sometime is not the correct link of image I need
	# So I take more links that I need to avoid this issue
    if len(image_urls) > num_imgs + 100:
        break
    # Scroll the web page to the bottom
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    # Delay    
    time.sleep(1)
# Take array to save values
filtered_urls_true_images = []
for url in image_urls:
    if url.startswith('https://images.pexels.com/photos'):
        filtered_urls_true_images.append(url)
	# This code will take the number of link images we need
    if len(filtered_urls_true_images) == num_imgs:
        break
# Download images
download(filtered_urls_true_images,folder_path_true_images)

