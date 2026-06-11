from flask import Blueprint
from flask import request

from stock import *

stock_bp = Blueprint(
    "stock",
    __name__
)

@stock_bp.route("/")
def home():

    selected_industry = request.args.get("industry")

    codes = load_watchlist()
    industry_rank = get_industry_rank()
    top10_industry = industry_rank[:10]
    industries = set()
    my_industries = get_my_industries()

    for info in codes.values():
        industries.add(info["industry"])

    result = """
        
    <html>
    <head>
        <title>주식 감시 시스템</title>
    </head>
    <body>

    <h1>주식 감시 시스템</h1>
    """
    result += """
    <a href="/">전체</a>
    """    
    for industry in sorted(industries):

        result += f"""
        |
        <a href="/?industry={industry}">
            {industry}
        </a>
        """
    result += """
    <br><br>

    <h2>🔥 오늘의 강세 업종 TOP10</h2>
    """

    for i, item in enumerate(top10_industry):

        change_value = float(
            item["change"].replace("%", "").replace("+", "")
        )

        if change_value >= 5:
            color = "red"

        elif change_value >= 2:
            color = "orange"

        else:
            color = "green"

        if i == 0:
            icon = "🥇"

        elif i == 1:
            icon = "🥈"

        elif i == 2:
            icon = "🥉"

        else:
            icon = "📌"

        related_stocks = []

        for stock_name, info in codes.items():

            if info["industry"] == item["name"]:

                related_stocks.append(stock_name)

        result += f"""
        <span style="color:{color}">
            {item["name"]} : {item["change"]}
        </span>

        <br>

        <br><br>
        """    
    result += "<br><br>"
    result += """
    <h2>📌 내 관심 업종</h2>
    """

    for industry in my_industries:

        related_stocks = []

        for stock_name, info in codes.items():

            if info["industry"] == industry:

                related_stocks.append(stock_name)
        
        industry_change = "정보없음"

        for item in industry_rank:

            if item["name"] == industry:

                industry_change = item["change"]
                break

        result += f"""
        <b>{industry}</b>
        ({industry_change})
        <br>

        관심종목 :
        {", ".join(related_stocks)}

        <br><br>
        """
    result += f"""
    <form action="/add" method="post">

        종목명 :
        <input type="text" name="name">

        종목코드 :
        <input type="text" name="code">

        업종 :
        <input type="text" name="industry">

        <input type="submit" value="추가">

    </form>
    
    <br>

    <table border="1" cellpadding="10">
        <tr>
            <th>종목명</th>
            <th>업종</th>
            <th>현재가</th>
            <th>거래량</th>
            <th>평균거래량</th>
            <th>거래량배수</th>
            <th>거래량평가</th>
            <th>외국인</th>
            <th>기관</th>
            <th>수급평가</th>
            <th>상승률</th>
            <th>신호</th>
            <th>관리</th>
        </tr>
    """

    for name, info in codes.items():
        if selected_industry:

            if info["industry"] != selected_industry:
                continue

        code = info["code"]
        industry = info["industry"]
        data = get_stock_data(code)
        avg_volume = get_average_volume(code)

        volume_ratio = data["volume"] / avg_volume
        volume_grade = get_volume_grade(volume_ratio)
        flow = get_foreign_institution(code)
        flow_grade = get_flow_grade(flow["foreign"], flow["institution"])

        signal = check_signal(data, volume_ratio)
        
        if signal == STRONG_SIGNAL:
            signal_text = "<span style='color:red'>🚀 강한급등</span>"

        elif signal == SIGNAL:
            signal_text = "<span style='color:orange'>🔥 급등</span>"

        else:
            signal_text = ""

        result += f"""
        <tr>
           <td>{name}</td>
           <td>{industry}</td>
            <td>{data['price']:,}</td>
            <td>{data['volume']:,}</td>
            <td>{avg_volume:,.0f}</td>
            <td>{volume_ratio:.2f}배</td>
            <td>{volume_grade}</td>
            <td>{flow['foreign']}</td>
            <td>{flow['institution']}</td>
            <td>{flow_grade}</td>
            <td>{data['change_rate']}%</td>
            <td>{signal_text}</td>            
            <td>
                <a href="/news/{code}">
                    뉴스
                </a>
            </td>
            <td>
                <a href="/delete/{name}">
                    삭제
                </a>
            </td>
        </tr>
        """

    result += """
    </table>

    </body>
    </html>
    """
    return result
