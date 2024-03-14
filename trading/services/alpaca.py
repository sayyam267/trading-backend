# from alpaca_trade_api.rest import *
import alpaca_trade_api as api
import os
import time
import config
import pandas as pd
from datetime import datetime
import pytz
# from alpaca_trade_api.entity import Order
# from datetime import datetime
# from dateutil import tz

# APCA_API_BASE_URL = '   '
# os.environ['APCA_API_BASE_URL'] = APCA_API_BASE_URL
# os.environ[config.API_KEY] = config.API_KEY
# os.environ[config.API_KEY] = config.SECRET_KEY
# api = api.REST(config.API_KEY, config.SECRET_KEY, api_version='v2')



class AlpacaService:
    def __init__(self, api_key, api_secret, test_mode=False):
        self.api = api.REST(api_key, api_secret, api_version='v2')
        self.test_mode = test_mode

    def get_clock(self):
        clock = self.api.get_clock()
        return clock

    def read_list():
        data = pd.read_csv("./p.txt", header=None, sep=',')
        data.columns = ["SYMBOL", "HIGH", "LOW", "MULTIPLE", "RISK", "REF"]
        data[["HIGH", "LOW", "MULTIPLE", "REF"]] = data[["HIGH", "LOW", "MULTIPLE", "REF"]].astype(float)
        data["RISK"] = data["RISK"].astype(int)
        return data

    def get_last_price(self,symbol):
        try:
            last_trade = self.api.get_latest_trade(symbol)
            last_price = last_trade.price
            return last_price
        except Exception as e:
            print(f"Error fetching last price for {symbol}: {e}")
            return None

    def is_market_open(self):
        try:
            clock = self.get_clock()
            return clock.is_open
        except Exception as e:
            print(f"Error fetching market status: {e}")
            return False


    def place_order(self,symbol, side, qty, ref):
        last_price = self.get_last_price(symbol)
        if side == 'buy':
            limit_price = last_price + ref
            stop_price = last_price - ref
        elif side == 'sell':
            limit_price = last_price - ref
            stop_price = last_price + ref

        print(f"Last price: {last_price:.2f}, Limit price: {limit_price:.2f}, Stop price: {stop_price:.2f}")

        try:
            self.api.submit_order(
                symbol=symbol,
                side=side,
                type='market',
                qty=qty,
                time_in_force='gtc',
                order_class='bracket',
                take_profit=dict(limit_price=limit_price),
                stop_loss=dict(stop_price=stop_price)
            )
            print(f"Order placed for {qty} shares of {symbol} at market price. Profit target: {limit_price:.2f}, Stop loss: {stop_price:.2f}")

        except Exception as e:
            print(f"Error submitting bracket order for {symbol}: {e}")

    def has_open_positions(self):
        try:
            positions = self.api.list_positions()
            open_positions=len(positions) 
            print(f"Open positions: {open_positions}")
            return len(positions) > 0
        except Exception as e:
            print(f"Error fetching open positions: {e}")
            return False
    

    def is_time_within_trading_hours():
        new_york_tz = pytz.timezone('America/New_York')
        current_time = datetime.now(new_york_tz).time()
        start_time = datetime.strptime('9:45AM', '%I:%M%p').time()
        end_time = datetime.strptime('3:55PM', '%I:%M%p').time()
        
        if start_time <= current_time <= end_time:
            return True
        else:
            return False

# def main():
#     while True:  # This will make your code run 24/7
#         if is_market_open() and is_time_within_trading_hours():
#             while has_open_positions():
#                 print("Waiting for open positions to be closed (checking after every 1mins to avoid python run frequently) )")
#                 time.sleep(1)  
#             data = read_list()
#             for _, row in data.iterrows():
#                 symbol, high, low, multiple, risk, ref = row
#                 last_price = get_last_price(symbol)
#                 print(f"Last price of {symbol}: {last_price}")
#                 if last_price is None:
#                     continue
#                 if last_price > high:
#                     print(f"Buy condition met for {symbol}")
#                     qty = round(risk / ref)
#     #                place_order(symbol, 'buy', qty, ref)
#                     break
#                 if last_price < low:
#                     print(f"Sell condition met for {symbol}")
#                     qty = round(risk / ref)
#     #                place_order(symbol, 'sell', qty, ref)
#                     break
#                 else:
#                     print(f"No conditions met for {symbol}")
#         else:
#             print("Market is closed or it's not trading hours. Waiting for market to open...")
#             time.sleep(60)  # Check every minute if the market is open

                
