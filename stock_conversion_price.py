'''
整合discord 轉換價格的群組，以關鍵字「轉換價格」查找最新的google新聞，
並且將新聞發送到discord群組中。

'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

# 紀錄已發送的新聞
sent_news_file = 'sent_news.json'
if os.path.exists(sent_news_file):
    with open(sent_news_file, 'r', encoding='utf-8') as f:
        sent_news = set(json.load(f))
else:
    sent_news = set()

# 紀錄上次檢查日期的文件
last_checked_date_file = 'last_checked_date.txt'
if os.path.exists(last_checked_date_file):
    with open(last_checked_date_file, 'r', encoding='utf-8') as f:
        last_checked_date = f.read().strip()
else:
    last_checked_date = datetime.now().strftime('%Y%m%d')

def save_sent_news():
    with open(sent_news_file, 'w', encoding='utf-8') as f:
        json.dump(list(sent_news), f, ensure_ascii=False, indent=4)

def save_last_checked_date(date):
    with open(last_checked_date_file, 'w', encoding='utf-8') as f:
        f.write(date)

def get_google_news():
    # 搜尋關鍵字「轉換價格」 1小時內的新聞
    url = f'https://news.google.com/search?q=%E8%BD%89%E6%8F%9B%E5%83%B9%E6%A0%BC%20when%3A1h&hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    # return soup

    news_list = []
    for item in soup.find_all("article", class_="IFHyqb"): # 更新的 Google 新聞項目 class
        title_tag = item.find("a", class_="JtKRv")
        title = title_tag.text if title_tag else "No title" # 標題
        link = title_tag["href"] if title_tag else "No link" # 連結
        if link.startswith("."):
            link = "https://news.google.com" + link[1:]
        source_tag = item.find("div", class_="vr1PYe")
        source = source_tag.text if source_tag else "No source" # 來源
        date_tag = item.find("time", class_="hvbAAd")
        date = date_tag.text if date_tag else "No date" # 日期

        news_id = title
        if news_id not in sent_news:
            sent_news.add(news_id)
            news_list.append({
                "title": title,
                "link": link,
                "source": source,
                "date": date
            })

    save_sent_news()
    return news_list

def check_news():
    global last_checked_date
    today = datetime.now().strftime('%Y%m%d')
    
    # 如果跨日，清空 sent_announcements
    if today != last_checked_date:
        sent_news.clear()
        last_checked_date = today
        save_sent_news()
        save_last_checked_date(today)

    new_news = get_google_news()

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
    if new_news:
        # 處理新公告，例如發送通知
        print(f"有新的news - {current_time}")
  
    else:
        print(f"沒有新的news - {current_time}")

    return new_news

if __name__ == "__main__":
    check_news()