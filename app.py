from flask import Flask, request, jsonify
import ccxt
import os

app = Flask(__name__)

# Initialize the Binance exchange
exchange = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_SECRET'),
    'enableRateLimit': True
})

@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    try:
        symbol = data['symbol']       # e.g., 'XRP/USDT'
        side = data['side'].lower()   # 'buy' or 'sell'
        price = float(data['price'])
        quantity = float(data['quantity'])

        stop_loss = float(data['stop_loss']) if 'stop_loss' in data else None
        take_profit = float(data['take_profit']) if 'take_profit' in data else None

        # Place the order
        if side == 'buy':
            order = exchange.create_limit_buy_order(symbol, quantity, price)
        elif side == 'sell':
            order = exchange.create_limit_sell_order(symbol, quantity, price)
        else:
            return jsonify({'error': 'Invalid side: use "buy" or "sell"'}), 400

        # You can implement custom logic to handle stop_loss/take_profit
        # For now, just print/log it — future version can add OCO orders
        if stop_loss or take_profit:
            print(f"Stop Loss: {stop_loss}, Take Profit: {take_profit} (not yet auto-managed)")

        return jsonify({'success': True, 'order': order})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "XRP Scalping Bot is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)