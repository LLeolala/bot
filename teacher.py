import pytesseract
import sys
import os
from PIL import Image
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
# 設定Tesseract執行文件的路徑（根據您的安裝位置）
#pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# 開啟圖片
arguments = sys.argv
q = arguments[1]
a = os.path.basename(q) # 2-12.py
b = a
filtered_chars = [char for char in b if char.isnumeric() or char == '-']
result = ''.join(filtered_chars) # 2-12
image_path = './images/' + str(result) +'.JPEG' #mac
image = Image.open(image_path)

# # 使用Tesseract進行OCR識別
try:
    text = pytesseract.image_to_string(image,lang="chi_tra+eng")
    print(text)
except:
    print("錯誤")
load_dotenv()
# # 開檔案
with open(q,"r") as f:
    answer = str(f.readlines())
    llm = OpenAI(openai_api_key=os.getenv("api_key"))
    chat_model = ChatOpenAI(openai_api_key=os.getenv("api_key"))
    print(chat_model.predict(text + "\n" + answer + "有需要更改的地方嗎？"))
    # sys.exit()
# # 顯示識別的文字
# # print(text)
