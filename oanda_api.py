import requests

class OandaAPI:
    def __init__(self, account_id, access_token):
        self.account_id = account_id
        self.access_token = access_token
        self.base_url = "https://api-fxpractice.oanda.com/v3"

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def create_order(self, instrument, units, side, take_profit):
        print("Creating order")
        url = f"{self.base_url}/accounts/{self.account_id}/orders"
        data = {
            "order": {
                "instrument": instrument,
                "units": str(units),
                "type": "MARKET",
                "timeInForce": "FOK",
                "takeProfitOnFill": {
                "price": str(2.00)
                }
            }
        }
        response = requests.post(url, json=data, headers=self.get_headers())
        return response.json()
