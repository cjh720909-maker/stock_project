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

    rows = soup.find_all("tr")

    volumes = []

    for row in rows:

        parts = row.get_text(" ", strip=True).split()

        if len(parts) >= 8:

            volume = parts[-1]

            volume = to_int(volume)

            volumes.append(volume)

        if len(volumes) == 5:
            break

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
def save_watchlist(codes):

    with open("watchlist.json", "w", encoding="utf-8") as file:
        json.dump(
            codes,
            file,
            ensure_ascii=False,
            indent=4
        )

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

    for row in rows:

        cols = row.find_all("td")

        if len(cols) == 4:

            foreign = cols[2].get_text(strip=True)

            institution = cols[3].get_text(strip=True)

            return {
                "foreign": foreign,
                "institution": institution
            }

    return {
        "foreign": "0",
        "institution": "0"
    }

def get_news(code):

    url = f"https://finance.naver.com/item/main.naver?code={code}"

    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    links = soup.find_all("a")

    news_list = []

    for link in links:

        title = link.get_text(strip=True)
        href = link.get("href")

        if not title:
            continue
        if not href:
            continue

        if "@code@" in title:
            continue

        if "관련" in title:
            continue

        if len(title) < 15:
            continue

        news_list.append({
            "title": title,
            "link": "https://finance.naver.com" + href
        })

        if len(news_list) == 5:
            break

    return news_list

def get_industry_rank():

    url = "https://finance.naver.com/sise/sise_group.naver?type=upjong"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find_all("table")[0]

    rows = table.find_all("tr")

    industries = []

    for row in rows:

        cols = row.find_all("td")

        if len(cols) < 2:
            continue

        name = cols[0].get_text(strip=True)

        change = cols[1].get_text(strip=True)

        industries.append({
            "name": name,
            "change": change
        })

    return industries

def get_my_industries():

    codes = load_watchlist()

    industries = set()

    for info in codes.values():

        industries.add(info["industry"])

    return sorted(list(industries))