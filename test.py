import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/main.naver?code=005930"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html.parser")

links = soup.find_all("a")

for i, link in enumerate(links):

    text = link.get_text(strip=True)

    href = link.get("href")

    if 43 <= i <= 55:

        print("=" * 50)
        print(text)
        print(href)