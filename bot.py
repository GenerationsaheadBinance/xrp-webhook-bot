from flask import Flask, request
import ccxt

app = Flask(__name__)

# Replace with your Binance API keys
binance = ccxt.binance({
    'apiKey': 'lZxM8dLKt42DLO0SbesHrfTVYJX1gJNC50WXjX0O2wSylY1n1V5lL8EcB97vjcjX',
    'secret': 'kN7hOZsUsteYR36OXeLwt9fZga4UdkxhSoIMFy9J2yikZBqREEhzCOeq8L2ooo5e',
    'enableRateLimit': True
})

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook received:", data)

    try:
        symbol = data['symbol'].replace("/", "").upper()
        price = float(data['price'])
        qty = float(data['quantity'])

        order = binance.create_limit_buy_order(symbol, qty, price)
        print("Order placed:", order)
        return {'status': 'success', 'order': order}

    except Exception as e:
        print("Error:", str(e))
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
