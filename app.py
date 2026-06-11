from flask import Flask, request
from routes.manage_routes import manage_bp
from routes.news_routes import news_bp
from routes.stock_routes import stock_bp

app = Flask(__name__)
app.register_blueprint(manage_bp)
app.register_blueprint(news_bp)
app.register_blueprint(stock_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

