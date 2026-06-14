from flask import Blueprint
from flask import request
from flask import render_template

from stock import *

stock_bp = Blueprint(
    "stock",
    __name__
)

@stock_bp.route("/")
def home():

    codes = load_watchlist()

    industry_rank = get_industry_rank()

    top10_industry = industry_rank[:10]

    industries = set()

    my_industries = get_my_industries()

    for info in codes.values():
        industries.add(
            info["industry"]
        )

    return render_template(
        "index.html",
        industries=sorted(industries),
        top10_industry=top10_industry,
        my_industries=my_industries,
        codes=codes,
        industry_rank=industry_rank
    )
    
@stock_bp.route("/watchlist")
def watchlist():
    import time
    start = time.time()

    codes = load_watchlist()
    selected_industry = request.args.get(
        "industry"
    )
    stocks = []

    for name, info in codes.items():
        if selected_industry:

            if info["industry"] != selected_industry:
                continue
        code = info["code"]
        industry = info["industry"]
        print("종목:", name)
        t1 = time.time()
        data = get_stock_data(code)
        print(name, "현재가", round(time.time() - t1, 2))

        t1 = time.time()
        avg_volume = get_average_volume(code)
        print(name, "평균거래량", round(time.time() - t1, 2))

        volume_ratio = data["volume"] / avg_volume
        
        volume_grade = get_volume_grade(volume_ratio)
        if volume_ratio >= 3:
            volume_color = "red"
            volume_icon = "🚀"

        elif volume_ratio >= 1.5:
            volume_color = "orange"
            volume_icon = "👀"

        else:
            volume_color = "black"
            volume_icon = ""

        t1 = time.time()
        flow = get_foreign_institution(code)
        print(name, "수급", round(time.time() - t1, 2))
        foreign_value = int(
            flow["foreign"]
            .replace(",", "")
        )

        institution_value = int(
            flow["institution"]
            .replace(",", "")
        )
        if foreign_value > 0:
            foreign_color = "red"
        elif foreign_value < 0:
            foreign_color = "blue"
        else:
            foreign_color = "black"

        if institution_value > 0:
            institution_color = "red"
        elif institution_value < 0:
            institution_color = "blue"
        else:
            institution_color = "black"


        signal = check_signal(
            data,
            volume_ratio
        )

        if signal == STRONG_SIGNAL:
            signal_text = "<span style='color:red'>🚀 강한급등</span>"

        elif signal == SIGNAL:
            signal_text = "<span style='color:orange'>🔥 급등</span>"

        else:
            signal_text = ""
        
        if data["change_rate"] > 0:
            change_color = "red"
        elif data["change_rate"] < 0:
            change_color = "blue"
        else:
            change_color = "black"

        buy_price = info.get("buy_price", "")

        profit_rate = ""

        target_price = info.get("target_price", "")
        stop_loss_price = info.get("stop_loss_price", "")

        decision = "관찰중"

        if buy_price:
            buy_price_value = int(buy_price)
            profit_rate = round(
                ((data["price"] - buy_price_value) / buy_price_value) * 100,
                2
            )

            if target_price and data["price"] >= int(target_price):
                decision = "목표가 도달: 일부 매도 검토"

            elif stop_loss_price and data["price"] <= int(stop_loss_price):
                decision = "손절가 도달: 매도 검토"

            elif profit_rate > 0:
                decision = "수익 중: 관찰"

            elif profit_rate < 0:
                decision = "손실 중: 감정 매도 금지"

            else:
                decision = "보유 유지"

        buy_price = info.get("buy_price", "")

        profit_rate = ""
        decision = "관찰중"

        target_price = info.get("target_price", "")
        stop_loss_price = info.get("stop_loss_price", "")

        if buy_price:

            buy_price_value = int(buy_price)

            profit_rate = round(
                (
                    (data["price"] - buy_price_value)
                    / buy_price_value
                ) * 100,
                2
            )

            if target_price and data["price"] >= int(target_price):

                decision = "🎯 목표가 도달"

            elif stop_loss_price and data["price"] <= int(stop_loss_price):

                decision = "🛑 손절가 도달"

            elif profit_rate > 0:

                decision = "👀 수익중"

            elif profit_rate < 0:

                decision = "⚠️ 손실중"

            else:

                decision = "보유 유지"

        stocks.append({
            "name": name,
            "industry": industry,
            "price": data["price"],
            "volume": data["volume"],
            "volume_display": f"{volume_ratio:.1f}",
            "volume_color": volume_color,
            "volume_icon": volume_icon,
            "foreign": flow["foreign"],
            "institution": flow["institution"],
            "foreign_color": foreign_color,
            "institution_color": institution_color,
            "change_rate": data["change_rate"],
            "buy_price": buy_price,
            "profit_rate": profit_rate,
            "target_price": target_price,
            "stop_loss_price": stop_loss_price,
            "decision": decision,
            "change_color": change_color,
            "signal_text": signal_text,
            "buy_price": buy_price,
            "profit_rate": profit_rate,
            "target_price": target_price,
            "stop_loss_price": stop_loss_price,
            "decision": decision,
            "code": code
        })
    print(
        "걸린시간:",
        round(time.time() - start, 2),
        "초"
    )
    return render_template(
        "watchlist.html",
        stocks=stocks,
        industries=sorted(
            set(
                info["industry"]
                for info in codes.values()
            )
        )
    )
@stock_bp.route("/stock/<name>")
def stock_detail(name):

    codes = load_watchlist()

    stock = codes[name]

    current_data = get_stock_data(
        stock["code"]
    )

    current_price = current_data["price"]

    buy_price = int(
        stock.get("buy_price", 0) or 0
    )

    target_price = int(
        stock.get("target_price", 0) or 0
    )

    stop_loss_price = int(
        stock.get("stop_loss_price", 0) or 0
    )

    profit_rate = 0

    if buy_price > 0:

        profit_rate = round(
            (
                current_price - buy_price
            ) / buy_price * 100,
            2
        )

    decision = "관찰중"

    if target_price > 0 and current_price >= target_price:

        decision = "🎯 목표가 도달"

    elif stop_loss_price > 0 and current_price <= stop_loss_price:

        decision = "🛑 손절가 도달"

    elif profit_rate > 10:

        decision = "📈 수익 확대중"

    elif profit_rate > 0:

        decision = "👀 수익중"

    elif profit_rate > -5:

        decision = "⏳ 보유 유지"

    else:

        decision = "⚠️ 손실 확대 주의"

    buy_reason_valid = stock.get("buy_reason_valid", "Y")

    if buy_reason_valid == "N":
        decision = "⚠ 매입이유 훼손: 재검토 필요"    
    return render_template(
        "stock_detail.html",
        name=name,
        stock=stock,
        current_price=current_price,
        profit_rate=profit_rate,
        decision=decision
    )