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
# Thiết lập trình duyệt
driver = webdriver.Chrome()
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

folder_path_AI_generated_images = "AI_generated_images"
if not os.path.exists(folder_path_AI_generated_images):
    os.makedirs(folder_path_AI_generated_images)

folder_path_true_images = "true images"
if not os.path.exists(folder_path_true_images):
    os.makedirs(folder_path_true_images)

# Lặp qua các URL của ảnh và tải xuống
def download(filtered_urls,folder_path):
	for i, url in enumerate(filtered_urls):
		response = requests.get(url)
		img = Image.open(io.BytesIO(response.content))
		img = img.resize((300, 300), Image.ANTIALIAS)  # Chỉnh kích thước ảnh
		filename = os.path.join(folder_path, f'image_{i+1}.jpg')
		img.save(filename)  # Lưu ảnh đã chỉnh kích thước
		print(f'Save image_{i+1}.jpg')

	print(f'All images downloaded and resized in {folder_path} successfully!')

# Download AI-generated-images
# Mở trang web
driver.get("https://generated.photos/faces")

# Thực thi đoạn mã JavaScript và lưu giá trị của biến imageUrls vào biến URLs
while True:
    image_urls = driver.execute_script(script)
    print(len(image_urls))
    if len(image_urls) > num_imgs + 100:
        break
    #URLs += image_urls
    else:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(1)
        # Ấn nút Load more
        load_more_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "loadmore-btn")))
        # Ấn nút Load more
        driver.execute_script("arguments[0].click();", load_more_btn)
    time.sleep(1)
filtered_urls_AI = []
for url in image_urls:
    if url.startswith('https://images.generated.photos'):
        filtered_urls_AI.append(url)
    if len(filtered_urls_AI) == num_imgs:
        break

download(filtered_urls_AI,folder_path_AI_generated_images)




# Mở trang web
driver.get("https://www.pexels.com/vi-vn/tim-kiem/cat/")

# Thực thi đoạn mã JavaScript và lưu giá trị của biến imageUrls vào biến URLs
while True:
    #scroll_down(wd)
    image_urls = driver.execute_script(script)
    print(len(image_urls))
    if len(image_urls) > num_imgs + 100:
        break
    #URLs += image_urls
    else:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Cuộn trang đến cuối trang
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
filtered_urls_true_images = []
for url in image_urls:
    if url.startswith('https://images.pexels.com/photos'):
        filtered_urls_true_images.append(url)
    if len(filtered_urls_true_images) == num_imgs:
        break

download(filtered_urls_true_images,folder_path_true_images)

