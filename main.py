

codes = {
    "삼성전자": "005930",
    "SK하이닉스": "000660",
    "LG씨엔에스": "064400",
    "에코프로": "086520"
}

for name, code in codes.items():
    data = get_stock_data(code)

    if data is None:
        print(f"{name} 데이터 실패")
        continue

    print(f"\n[{name}]")
    print("현재가:", data["price"])
    print("거래량:", data["volume"])
    print("상승률:", data["change_rate"], "%")

    signal = check_signal(data)

    if signal == 2:
        print("🚀 강한 급등")

    elif signal == 1:
        print("🔥 급등 감지")

    else:
        print("🚫 신호 없음")