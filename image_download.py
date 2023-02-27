import csv
import os
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# 取得當前工作目錄
path = os.getcwd() 

# 建立 images 資料夾，如果不存在的話
if not os.path.isdir(os.path.join(path, 'images')):
    os.mkdir(os.path.join(path, 'images'))

# 讀取 CSV 檔案
with open(f'{path}/img.csv', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)

    # 遍歷 CSV 每一行的網址
    for row in csv_reader:
        url = row[0]
        print(f"Downloading images from {url} ...")

        try:
            # 發送 HTTP 請求，並解析網頁內容
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 找到圖片的<img>標籤
            img_tag = soup.find(class_='rakutenLimitedId_ImageMain1-3')

            # 取得圖片的src屬性
            img_url = img_tag.select('img')[0]['src']

            # 移除圖片 URL 中的 ? 及其後面的字串
            img_url = img_url.split('?')[0]

            # 取番號作為檔名
            img_title = url.strip().split('/')
            # 清除回傳串列裡的空字串
            removeEmptyString = [i.strip() for i in img_title if i.strip()!='']
            img_title = removeEmptyString[-1]
            print(img_title)


            # 下載圖片並存檔
            img_data = requests.get(img_url).content
            filename = os.path.basename(img_title)
            with open(f"{path}/images/{filename}.jpg", 'wb') as img_file:
                img_file.write(img_data)
            print(f"{img_url} downloaded successfully.")
        except:
            with open('error.txt', 'a') as error_file:
                error_file.write(f"{url}\n")
            print(f"{img_url} download failed.")
