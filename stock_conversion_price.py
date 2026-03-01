'''
追縱google的新聞，關鍵字 "轉換價格"。
'''


import urllib.parse
import requests
import feedparser

def check_news():
    # 1. 設定關鍵字並轉換為 URL 編碼格式
    query = "轉換價格 when:1h"  # 搜尋過去一天內的新聞
    encoded_query = urllib.parse.quote(query)

    # 將網址改為 Google 新聞的 RSS 搜尋端點
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"

    # 2. 發送請求以獲取 RSS 內容
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(rss_url, headers=headers)

    # 3. 使用 feedparser 解析回傳的 XML 內容
    feed = feedparser.parse(response.content)

    news_list = []

    # 4. 迴圈讀取每一篇新聞
    for entry in feed.entries:
        news_list.append({
            'title': entry.title,
            'link': entry.link,
            'source': entry.source.title if 'source' in entry else '未知',
            'time': entry.published
        })

    # 回傳抓取到的新聞列表，給 run.py 接收
    return news_list





