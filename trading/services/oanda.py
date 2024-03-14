import oandapyV20.endpoints.orders as orders
from oandapyV20 import API
import oandapyV20.endpoints.positions as positions
import json
import requests

data_history = []
trade_counter = 0

# # # kit  # 2
# api_key = "eabb3691d3963211e3c3a1bf57ffafcc-920523c2b86b6317c84d3e491209cd87"
# account_id = "101-001-25888676-002"

# my Account
# api_key = "f2267fecaf428118ef39dfaee4aa0ee3-0a3a264a3c9cd117632c7b938e1b5068"
# account_id = "101-001-27976524-001"


class AlpacaService:
    def __init__(self, api_key, api_secret, test_mode=False):
        self.api = API(access_token=api_key, environment="practice")
        self.account_id = api_secret
        self.api_key = api_key
        self.test_mode = test_mode


    def get_account_balance(self):
        endpoint = f"https://api-fxpractice.oanda.com/v3/accounts/{self.account_id}/summary"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            account_summary = response.json()["account"]
            balance = float(account_summary["balance"])
            return balance
        else:
            print("Error:", response.status_code, response.text)


    def has_open_positions(self):
        r = positions.OpenPositions(accountID=self.account_id)
        self.api.request(r)
        return len(r.response['positions']) > 0


    def format_ticker(ticker):
        return ticker[:3] + '_' + ticker[3:]


    def execute_order(self,instrument, units, side, entry_price):

        account_balance = self.get_account_balance()
        print("Account balance  is :", account_balance)
        leverage = 20
        print("side is :", side)

        position_size = (account_balance * 0.05) * leverage
        print("Position size is :", position_size)

        if side == "buy":
            units = int(position_size)
        elif side == "sell":
            units = int(position_size)

        if side == "buy":
            # stopLossPercent = 0.001  # 0.1% of the entry price
            # takeProfitPercent = 0.001  # 0.1% of the entry  price
            # take_profit = entry_price + (entry_price * takeProfitPercent)
            # stop_loss = entry_price - (entry_price * stopLossPercent)
            # print("profit for long is", take_profit)
            # print("loss for long is", stop_loss)
            order_data = {
                "order": {
                    "instrument": instrument,
                    "units": units,
                    "type": "MARKET"
                }
            }
        elif side == "sell":
            # stopLossPercent = 0.001  # 0.1% of the entry price
            # takeProfitPercent = 0.001  # 0.1% of the entry  price
            # take_profit = entry_price - (entry_price * takeProfitPercent)
            # stop_loss = entry_price + (entry_price * stopLossPercent)
            # print("profit for short is", take_profit)
            # print("loss for short is", stop_loss)
            order_data = {
                "order": {
                    "instrument": instrument,
                    "units": -units,
                    "type": "MARKET"
                    # "stopLossOnFill": {
                    #     "timeInForce": "GTC",
                    #     "price": str(round(stop_loss, 2))
                    # },
                    # "takeProfitOnFill": {
                    #     "timeInForce": "GTC",
                    #     "price": str(round(take_profit, 2))
                    # }
                }
            }

        order = orders.OrderCreate(accountID=self.account_id, data=order_data)
        response = self.api.request(order)
        print(json.dumps(response, indent=4))




# def webhook():

#     data = request.get_json()
#     # extract data
#     print(data)
#     units = int(data["strategy"]["order_contracts"])
#     ticker = data["ticker"]
#     side = data["strategy"]["order_action"]
#     entry_price = float(data["strategy"]["order_price"])
#     # format the ticker
#     instrument = format_ticker(ticker)
#     # if has_open_positions():
#     #     print("Order not executed because there are open positions.")
#     #     # return jsonify(data), 200
#     # close all open positions
#     # close_all_positions()
#     # print("All open positions closed.")
#     # execute order function
#     execute_order(instrument, units, side, entry_price)
#     print("Order executed!")
#     return jsonify(data), 200

