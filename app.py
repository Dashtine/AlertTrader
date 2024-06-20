from flask import Flask, request, jsonify, render_template
import json
from oanda_api import OandaAPI

app = Flask(__name__)

account_id = "101-001-16126588-001"
access_token = "a76e021bca12d780ba28d7176744a7b8-3662309689014e9e58bb42013cda2fba"
oanda = OandaAPI(account_id, access_token)

running = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global running
    running = True
    print("Bot started")
    return 'Bot started'

@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    print("Bot stopped")
    return 'Bot stopped'

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook endpoint hit!")
    global running
    if not running:
        print("Webhook endpoint hit: Bot not running")
        return jsonify({"error": "Bot not running"}), 400
    
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = json.loads(request.data.decode('utf-8'))
        print(data)
        signal = data.get('signal')
        instrument = data.get('instrument')
        take_profit = data.get('take_profit')
    except Exception as e:
        print(f"Error processing webhook data: {e}")
        return jsonify({"error": "Invalid data"}), 400
    
    if signal == 'buy':
        oanda.create_order(instrument, 1000, 'buy', take_profit)
        print(f"Webhook: Buy order placed for {instrument} with take profit at {take_profit}")

    elif signal == 'sell':
        oanda.create_order(instrument, -1000, 'sell', take_profit)
        print(f"Webhook: Sell order placed for {instrument} with take profit at {take_profit}")

    elif signal == 'manual': #testing purposes
        print("Calling create_order")
        oanda.create_order(instrument, 1000, 'buy', take_profit)
        print(f"Webhook: Manual order placed for {instrument} with take profit at {take_profit}")
    
    return jsonify({"status": "order executed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
                           


        