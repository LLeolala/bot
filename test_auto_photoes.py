import os
import time
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager  # 引入 ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager. chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# # 設定網頁URL
url = 'https://play.google.com/books/reader?id=nFRWEAAAQBAJ&pg=GBS.SA9-PA17&hl=zh-TW'

# # 初始化 Chrome WebDriver，自動下載並設定 Chrome WebDriver


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# # 前往指定網址
driver.get(url)

# # 等待網頁加載，你可能需要調整等待的時間
time.sleep(5)

# # 找到所有的圖片元素# 
img_elements = driver.find_elements(By.CLASS_NAME, 'display')

# # 建立目錄來儲存圖片
os.makedirs('images', exist_ok=True)

# # 擷取並下載圖片
for img_element in img_elements:
    img_url = img_element.get_attribute('src')
    if img_url:
        img_data = requests.get(img_url).content
        img_name = img_url.split('/')[-1]
        img_path = os.path.join('images', img_name)
        
        with open(img_path, 'wb') as img_file:
            img_file.write(img_data)
            print(f"Downloaded: {img_name}")

# # 關閉瀏覽器
driver.quit()
