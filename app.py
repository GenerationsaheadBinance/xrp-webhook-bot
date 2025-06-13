from flask import Flask, request, jsonify
import ccxt

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No JSON payload"}), 400

    symbol = data.get("symbol")
    price = float(data.get("price", 0))
    quantity = float(data.get("quantity", 0))

    try:
        exchange = ccxt.binance({
            "apiKey": "lZxM8dLKt42DLO0SbesHrfTVYJX1gJNC50WXjX0O2wSylY1n1V5lL8EcB97vjcjX",
            "secret": "kN7hOZsUsteYR36OXeLwt9fZga4UdkxhSoIMFy9J2yikZBqREEhzCOeq8L2ooo5e",
            "enableRateLimit": True,
        })

        # Place real order
        order = exchange.create_limit_buy_order(symbol=symbol, amount=quantity, price=price)

        return jsonify({"status": "success", "order": order})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
