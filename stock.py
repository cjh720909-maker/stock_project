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

def check_signal(data, volume_ratio):

    if data["change_rate"] >= 5 and volume_ratio >= 2:
        return STRONG_SIGNAL

    elif data["change_rate"] >= 3 and volume_ratio >= 1.5:
        return SIGNAL

    else:
        return NO_SIGNAL

def load_watchlist():

    with open("watchlist.json", "r", encoding="utf-8") as file:
        codes = json.load(file)

    return codes
def get_volume_grade(volume_ratio):
    if volume_ratio >= 3:
        return "💥 거래량폭발"

    if volume_ratio >= 2:
        return "🚀 수급유입"

    if volume_ratio >= 1.5:
        return "👀 관심"

    return "보통"
def get_flow_grade(foreign, institution):

    foreign_num = int(foreign.replace(",", ""))

    institution_num = int(institution.replace(",", ""))

    if foreign_num > 0 and institution_num > 0:
        return "🟢 동반매수"

    elif foreign_num > 0 and institution_num < 0:
        return "🔵 외국인매수"

    elif foreign_num < 0 and institution_num > 0:
        return "🟠 기관매수"

    else:
        return "🔴 동반매도"
def get_foreign_institution(code):

    url = f"https://finance.naver.com/item/main.naver?code={code}"

    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    res.encoding = "euc-kr"

    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.find_all("table")

    table = tables[3]

    rows = table.find_all("tr")

    today_row = rows[2]

    cols = today_row.find_all("td")

    foreign = cols[2].get_text(strip=True)

    institution = cols[3].get_text(strip=True)

    return {
        "foreign": foreign,
        "institution": institution
    }
    
    
def test_foreign_data(code):

    url = f"https://finance.naver.com/item/main.naver?code={code}"

    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    res.encoding = "euc-kr"

    soup = BeautifulSoup(res.text, "html.parser")

    iframes = soup.find_all("iframe")

    print("iframe 개수:", len(iframes))

    for i, iframe in enumerate(iframes):
        print("iframe 번호:", i)
        print(iframe)
        print("=" * 50)

    tables = soup.find_all("table")

    print("테이블 개수:", len(tables))
    for i, table in enumerate(tables):
        print("테이블:", i)

        text = table.get_text(" ", strip=True)

        print(text[:300])

        print("=" * 50)

    table = tables[3]

    rows = table.find_all("tr")

    print("행 개수:", len(rows))

    for i, row in enumerate(rows):
        print("행 번호:", i)

        cols = row.get_text(" ", strip=True)

        print(cols)

        print("=" * 50)

    today_row = rows[2]

    cols = today_row.find_all("td")

    print("칸 개수:", len(cols))

    for i, col in enumerate(cols):
        print(i, col.get_text(strip=True))


if __name__ == "__main__":

    data = get_foreign_institution("005930")

    print(data)
    