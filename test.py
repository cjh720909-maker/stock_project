import requests
from bs4 import BeautifulSoup


def test_industry_rank():

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

    for item in industries[:10]:

        print(
            item["name"],
            item["change"]
        )
        
if __name__ == "__main__":
    test_industry_rank()