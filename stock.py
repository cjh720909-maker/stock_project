import requests
from bs4 import BeautifulSoup
import json

NO_SIGNAL = 0
SIGNAL = 1
STRONG_SIGNAL = 2


def to_int(text):
    return int(text.replace(",", ""))

def get_stock_data(code):
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    res.encoding = "euc-kr"

    soup = BeautifulSoup(res.text, "html.parser")

    # 현재가
    price_tag = soup.select_one("p.no_today span.blind")
    if not price_tag:
        return None
    price = price_tag.text

    # 정보들
    infos = soup.select("table.no_info span.blind")

    if len(infos) < 5:
        return None

    yesterday = infos[0].text
    volume = infos[3].text

    try:
        price_int = to_int(price)
        yesterday_int = to_int(yesterday)
        volume_int = to_int(volume)
    except:
        return None

    change_rate = (price_int - yesterday_int) / yesterday_int * 100

    return {
        "price": price_int,
        "volume": volume_int,
        "change_rate": round(change_rate, 2)
    }

def get_average_volume(code):
    url = f"https://finance.naver.com/item/sise_day.naver?code={code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    res.encoding = "euc-kr"

    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.text

    index = text.find("거래량")

    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.find_all("tr")

    volumes = []

    for i in range(2, 7):
        text = rows[i].get_text(" ", strip=True)

        parts = text.split()

        volume = parts[-1]

        volume = to_int(volume)

        volumes.append(volume)
    average = sum(volumes) / len(volumes)
    return average

def check_signal(data):
    if data["change_rate"] >= 5 and data["volume"] >= 1000000:
        return STRONG_SIGNAL

    elif data["change_rate"] >= 3 and data["volume"] >= 500000:
        return SIGNAL

    else:
        return NO_SIGNAL

def load_watchlist():

    with open("watchlist.json", "r", encoding="utf-8") as file:
        codes = json.load(file)

    return codes
