from flask import Blueprint
from flask import request

from stock import load_watchlist
from stock import save_watchlist

manage_bp = Blueprint(
    "manage",
    __name__
)

@manage_bp.route("/add", methods=["POST"])
def add_stock():

    name = request.form["name"]
    code = request.form["code"]
    industry = request.form["industry"]

    codes = load_watchlist()

    codes[name] = {
        "code": code,
        "industry": industry
    }

    save_watchlist(codes)

    return """
    <script>
        alert("종목 추가 완료");
        location.href="/";
    </script>
    """

@manage_bp.route("/delete/<name>")
def delete_stock(name):

    codes = load_watchlist()

    if name in codes:
        del codes[name]

    save_watchlist(codes)

    return """
    <script>
        location.href="/";
    </script>
    """