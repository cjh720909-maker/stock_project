from flask import Blueprint
from flask import request
from flask import render_template
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

    status = request.form.get("status", "관찰중")
    buy_date = request.form.get("buy_date", "")
    buy_price = request.form.get("buy_price", "")
    quantity = request.form.get("quantity", "")
    buy_reason = request.form.get("buy_reason", "")
    target_price = request.form.get("target_price", "")
    buy_reason_valid = request.form.get("buy_reason_valid", "Y")
    stop_loss_price = request.form.get("stop_loss_price", "")
    sell_rule = request.form.get("sell_rule", "")
    memo = request.form.get("memo", "")

    codes = load_watchlist()

    codes[name] = {
        "code": code,
        "industry": industry,
        "status": status,
        "buy_date": buy_date,
        "buy_price": buy_price,
        "quantity": quantity,
        "buy_reason": buy_reason,
        "target_price": target_price,
        "stop_loss_price": stop_loss_price,
        "sell_rule": sell_rule,
        "buy_reason_valid": buy_reason_valid,
        "memo": memo
    }

    save_watchlist(codes)

    return """
    <script>
        alert("종목 추가 완료");
        location.href="/watchlist";
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

@manage_bp.route("/edit/<name>")
def edit_stock(name):

    codes = load_watchlist()

    stock = codes[name]

    return render_template(
        "edit_stock.html",
        name=name,
        stock=stock
    )


@manage_bp.route("/update/<name>", methods=["POST"])
def update_stock(name):

    codes = load_watchlist()

    codes[name] = {
        "code": request.form.get("code", ""),
        "industry": request.form.get("industry", ""),
        "status": request.form.get("status", "관찰중"),
        "buy_date": request.form.get("buy_date", ""),
        "buy_price": request.form.get("buy_price", ""),
        "quantity": request.form.get("quantity", ""),
        "buy_reason": request.form.get("buy_reason", ""),
        "target_price": request.form.get("target_price", ""),
        "stop_loss_price": request.form.get("stop_loss_price", ""),
        "sell_rule": request.form.get("sell_rule", ""),
        "buy_reason_valid": request.form.get("buy_reason_valid", "Y"),
        "memo": request.form.get("memo", "")
    }

    save_watchlist(codes)

    return """
    <script>
        alert("수정 완료");
        location.href="/watchlist";
    </script>
    """