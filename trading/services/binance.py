from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from requests.exceptions import ReadTimeout, ConnectionError

class BinanceService:
    def __init__(self, api_key, api_secret, test_mode=False):
        self.client = Client(api_key, api_secret)
        self.test_mode = test_mode

    def create_order(self,side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print(f"sending order {order_type} - {side} {quantity} {symbol}")
            order = self.client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        
    def create_test_order(self,side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print(f"sending order {order_type} - {side} {quantity} {symbol}")
            order = self.client.create_test_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            print('order details',order)
        except Exception as e:
            print("an exception occured - {}".format(e))
            return False
        
    def get_prices(self,markets):
        """ request api to return the current prices for the 3 markets """
        try:
            prices = {}
            for ticker in self.client.get_all_tickers():
                if ticker['symbol'] in markets:
                    prices[ticker['symbol']] = float(ticker['price'])
        except ReadTimeout:
            prices = "ReadTimeout during check rentability"
        except ConnectionError:
            prices = "ConnectionError during check rentability"
        except BinanceAPIException:
            prices = "BinanceAPIException during check rentability"
        return prices


    def open_sell_order(self,market, quantity, price):
        """ open a sell order """
        self.client.order_limit_sell(
            symbol=market,
            quantity=quantity,
            price=price)


    def open_buy_order(self,market, quantity, price):
        """ open a buy order """
        self.client.order_limit_buy(
            symbol=market,
            quantity=quantity,
            price=price)


    def check_order(self, market):
        """ check if there is open order on a specific market and
        return it or [] if not """
        try:
            order = self.client.get_open_orders(symbol=market)
        except ReadTimeout:
            order = "ReadTimeout during check order"
        except ConnectionError:
            order = "ConnectionError during check order"
        except BinanceAPIException:
            order = "BinanceAPIException during check order"
        return order


    def check_bank(self, currencies):
        """ found balances available for the client """
        try:
            balances = self.client.get_account()['balances']
            bank = {}
            for currency in balances:
                if currency["asset"] in currencies:
                    bank[currency["asset"]] = float(currency["free"])
        except ReadTimeout:
            bank = "ReadTimeout during check bank"
        except ConnectionError:
            bank = "ConnectionError during check bank"
        except BinanceAPIException:
            bank = "BinanceAPIException during check bank"
        return bank