from flask import Flask, request, jsonify, render_template, Response, send_from_directory
import json
from datetime import datetime
import threading
from oanda_api import OandaAPI

app = Flask(__name__)

account_id = "101-001-16126588-001"
access_token = "a76e021bca12d780ba28d7176744a7b8-3662309689014e9e58bb42013cda2fba"
oanda = OandaAPI(account_id, access_token)

running = True
log_messages = []

def log_message(message):
    timestamp = datetime.now().strftime('%m-%d-%y %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    log_messages.append(log_entry)
    if len(log_messages) > 100:
        log_messages.pop(0)

def generate_logs():
    while True:
        if log_messages:
            yield f"data: {log_messages.pop(0)}\n\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global running
    running = True
    log_message("Bot started")
    return ''

@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    log_message("Bot stopped")
    return ''

@app.route('/logs')
def logs():
    return Response(generate_logs(), mimetype='text/event-stream')

@app.route('/webhook', methods=['POST'])
def webhook():
    log_message("Webhook endpoint hit!")
    global running
    if not running:
        log_message("Webhook endpoint hit: Bot not running")
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
        log_message(f"Error processing webhook data: {e}")
        return jsonify({"error": "Invalid data"}), 400
    
    if signal == 'buy':
        oanda.create_order(instrument, 1000, 'buy', take_profit)
        log_message(f"Webhook: Buy order placed for {instrument} with take profit at {take_profit}")

    elif signal == 'sell':
        oanda.create_order(instrument, -1000, 'sell', take_profit)
        log_message(f"Webhook: Sell order placed for {instrument} with take profit at {take_profit}")

    elif signal == 'manual': #testing purposes
        log_message("Calling create_order")
        oanda.create_order(instrument, 1000, 'buy', take_profit)
        log_message(f"Webhook: Manual order placed for {instrument} with take profit at {take_profit}")
    
    return jsonify({"status": "order executed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
                           


        