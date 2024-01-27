import pytesseract
import sys
from PIL import Image
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
# 設定Tesseract執行文件的路徑（根據您的安裝位置）
#pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# 開啟圖片
arguments = sys.argv
image_path = arguments[1]
image = Image.open(image_path)

# 使用Tesseract進行OCR識別
text = pytesseract.image_to_string(image,lang="chi_tra+eng")

# 顯示識別的文字
print(text)
