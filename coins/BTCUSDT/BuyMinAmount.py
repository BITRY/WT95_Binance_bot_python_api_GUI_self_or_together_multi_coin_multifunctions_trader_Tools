from binance.client import Client
import config
import time
import sys

from WinTradeDB_FUNCTIONS import *
import sqlite3

from tradehistory import *
from Request import *
import tradehistory
import Request
from varmove import Coin
from mintrade import min_trade_qty


#BINANCE-PYTHON API HOODLER SCRIPT CREATED By M.R

client = Client(config.api_key, config.api_secret)


quantity = min_trade_qty
symbol = Coin
order_type= "MARKET"


def get_mark_and_average_price(symbol):
    try:
        mark_price_info = client.futures_mark_price(symbol=symbol)
        average_price_info = client.get_avg_price(symbol=symbol)
        
        mark_price = float(mark_price_info['markPrice'])
        average_price = float(average_price_info['price'])
        
        return mark_price, average_price
    
    except Exception as e:
        Tradeslog.warning(f'Error retrieving mark and average price: {str(e)}')
        return None, None


def get_minimum_quantity(symbol, order_type):
    try:
    
        mark_price, average_price = get_mark_and_average_price(symbol)
        
        exchange_info = client.futures_exchange_info()

        symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)

        if symbol_info is None:
            Tradeslog.warning(f"Symbol {symbol} not found in trading rules")
            return None

        filters = symbol_info['filters']
        min_trade_qty = None

        # Find the relevant filters
        price_filter = next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', filters), None)
        lot_size_filter = next(filter(lambda f: f['filterType'] == 'LOT_SIZE', filters), None)
        min_notional_filter = next(filter(lambda f: f['filterType'] == 'MIN_NOTIONAL', filters), None)
        
        if order_type == 'MARKET':
            if min_notional_filter and average_price:
                min_trade_qty = max(float(lot_size_filter['stepSize']),
                                   float(min_notional_filter['notional']) / average_price)
                min_trade_qty = ( min_trade_qty * 165 ) / 100   
                print('Rounded1 '    +str(min_trade_qty ) +    '           min_trade_qty = ' +str(min_trade_qty ))
        elif order_type == 'LIMIT':
            if price and min_notional_filter:
                min_trade_qty = max(float(lot_size_filter['stepSize']),
                                   float(min_notional_filter['notional']) / price)


  
        if min_trade_qty is not None:
            if min_trade_qty > 1 or min_trade_qty == 1:
                min_trade_qty = round(min_trade_qty)
            elif min_trade_qty < 1 and not min_trade_qty < 0.1:
                min_trade_qty = round(min_trade_qty, 1)
            elif min_trade_qty < 0.1 and not min_trade_qty < 0.01:
                min_trade_qty = round(min_trade_qty, 2)
            else:
                min_trade_qty = round(min_trade_qty, 3)

            return min_trade_qty

        Tradeslog.warning(f"Minimum TradeAmount not found for symbol {symbol}")
        return None

    except Exception as e:
        print(f"Error in get_minimum_quantity: {e}")
        return None



def optimazetrade(symbol, quantity):
    try:
        client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side='BUY',
            quantity=quantity
        )
        print("Order executed successfully!")
    except Exception as e:
        error_message = str(e)
        if 'APIError(code=-2019)' in error_message:
            print("Margin is insufficient.")
        else:
            print("An error occurred:", error_message)

min_trade_qty = get_minimum_quantity(symbol, order_type)
optimazetrade(symbol, min_trade_qty)


