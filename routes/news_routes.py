from flask import Blueprint

from stock import load_watchlist
from stock import get_news

news_bp = Blueprint(
    "news",
    __name__
)

@news_bp.route("/news/<code>")
def show_news(code):

    codes = load_watchlist()

    name = code

    for stock_name, info in codes.items():

        if info["code"] == code:
            name = stock_name
            break

    news = get_news(code)

    result = f"<h1>{name} 뉴스</h1>"

    for i, item in enumerate(news, start=1):

        result += f"""
        <p>
            {i}. {item['title']}
            <br>
            <a href="{item['link']}" target="_blank">
                기사 읽기
            </a>
        </p>
        """

    result += """
    <br><br>
    <a href="/">메인으로 돌아가기</a>
    """

    return result