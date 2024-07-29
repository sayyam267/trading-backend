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
            # order = self.client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            # info = self.get_symbol_info(symbol=symbol)
            price = self.get_prices([symbol])
            return price
        except Exception as e:
            print("an exception occured - {}".format(e))
            return format(e)
        
    def create_test_order(self,side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print(f"sending order {order_type} - {side} {quantity} {symbol}")
            order = self.client.create_tesr(symbol=symbol, side=side, type=order_type, quantity=quantity)
            # order = self.check_bank(['USDT'])
            return order
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


    def create__limit_sell_order(self,market, quantity, price):
        """ open a sell order """
        self.client.order_limit_sell(
            symbol=market,
            quantity=quantity,
            price=price)


    def create__limit_buy_order(self,market, quantity, price):
        """ open a buy order """
        self.client.order_limit_buy(
            symbol=market,
            quantity=quantity,
            price=price)


    def get_open_orders(self, symbol):
        """ check if there is open order on a specific market and
        return it or [] if not """
        try:
            order = self.client.get_open_orders(symbol=symbol)
        except ReadTimeout:
            order = "ReadTimeout during check order"
        except ConnectionError:
            order = "ConnectionError during check order"
        except BinanceAPIException:
            order = "BinanceAPIException during check order"
        return order
    
    def check_order_status(self, symbol,order_id):
        """ check if there is open order on a specific market and
        return it or [] if not """
        try:
            status = self.client.get_order(symbol=symbol,orderId=order_id)
            return status
        except ReadTimeout as e:
            error = f"ReadTimeout  {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    
    def cancel_order(self, symbol,order_id):
        """ check if there is open order on a specific market and
        return it or [] if not """
        try:
            status = self.client.cancel_order(symbol=symbol,orderId=order_id)
            return status
        except ReadTimeout as e:
            error = f"ReadTimeout  {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error


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
    
    def get_all_orders(self,symbol):

        """ fget all orders"""
        try:
            orders = self.client.get_all_orders(symbol=symbol)
            return orders
        except ReadTimeout:
            error = "ReadTimeout during check bank"
        except ConnectionError:
            error = "ConnectionError during check bank"
        except BinanceAPIException as e:
            error = f"BinanceAPIException getting all orders, {e}"
        return error
    

    def get_all_tickers(self):
        """ fget all orders"""
        try:
            tickers = self.client.get_all_tickers()
            return tickers
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    def get_exchange_info(self):
        """ get exchange info """
        try:
            info = self.client.get_exchange_info()
            return info
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    
    
    def get_market_depth(self,symbol):
        """ get market depth """
        try:
            depth = self.client.get_order_book(symbol=symbol)
            return depth
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    def get_recent_trades(self,symbol):
        """ get recent trades """
        try:
            trades = self.client.get_recent_trades(symbol=symbol)
            return trades
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    def get_avg_price(self,symbol):
        """ get recent trades """
        try:
            avg_price = self.client.get_avg_price(symbol=symbol)
            return avg_price
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    
    def get_symbol_info(self,symbol):
        """ get symbol info """
        try:
            info = self.client.get_symbol_info(symbol=symbol)
            return info
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    """ Accounts """

    def get_account_info(self):
        """ get account info """
        try:
            info = self.client.get_account()
            return info
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    def get_account_status(self):
        """ get account info """
        try:
            status = self.client.get_account_status()
            return status
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    def get_api_trading_status(self):
        """ get account trading status """
        try:
            status = self.client.get_account_api_trading_status()
            return status
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error
    

    def get_trades(self,symbol):
        """ get account trading status """
        try:
            trades = self.client.get_my_trades(symbol=symbol)
            return trades
        except ReadTimeout as e:
            error = f"ReadTimeout {e}"
        except ConnectionError as e:
            error = f"ConnectionError {e}"
        except BinanceAPIException as e:
            error = f"BinanceAPIException {e}"
        return error

