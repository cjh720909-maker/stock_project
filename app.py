from flask import Flask
from stock import get_stock_data
from stock import get_average_volume
from stock import load_watchlist
from stock import check_signal
from stock import SIGNAL, STRONG_SIGNAL, NO_SIGNAL


app = Flask(__name__)

@app.route("/")
def home():

    codes = load_watchlist()

    result = """
        
    <html>
    <head>
        <title>주식 감시 시스템</title>
    </head>
    <body>

    <h1>주식 감시 시스템</h1>

    <table border="1" cellpadding="10">
        <tr>
            <th>종목명</th>
            <th>현재가</th>
            <th>거래량</th>
            <th>평균거래량</th>
            <th>거래량배수</th>
            <th>상승률</th>
            <th>신호</th>
        </tr>
    """

    for name, code in codes.items():

        data = get_stock_data(code)
        avg_volume = get_average_volume(code)

        volume_ratio = data["volume"] / avg_volume

        signal = check_signal(data)

        if signal == STRONG_SIGNAL:
            signal_text = "<span style='color:red'>🚀 강한급등</span>"

        elif signal == SIGNAL:
            signal_text = "<span style='color:orange'>🔥 급등</span>"

        else:
            signal_text = ""

        result += f"""
        <tr>
           <td>{name}</td>
            <td>{data['price']:,}</td>
            <td>{data['volume']:,}</td>
            <td>{avg_volume:,.0f}</td>
            <td>{volume_ratio:.2f}배</td>
            <td>{data['change_rate']}%</td>
            <td>{signal_text}</td>
        </tr>
        """

    result += """
    </table>

    </body>
    </html>
    """
    return result

if __name__ == "__main__":
    app.run(debug=True)

