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
from AMOUNT import AMOUNT

#BINANCE-PYTHON API HOODLER SCRIPT CREATED By M.Ry

client = Client(config.api_key, config.api_secret)



symbol = Coin	   	



order_type= "MARKET"
PosFastClose= 0

max_retries = 3
delay = 2

BUYOrderActive = 0
SELLOrderActive = 0
PositionSize = 0

min_trade_qty = 0
buyactive = 0
sellactive = 0

quantity = PositionSize
symbol = Coin


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
            print(f"Symbol {symbol} not found in trading rules")
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
                min_trade_qty = ( min_trade_qty * 115  ) /100
                print('min_trade_qty: '+str(min_trade_qty))   
        elif order_type == 'LIMIT':
            if price and min_notional_filter:
                min_trade_qty = max(float(lot_size_filter['stepSize']),
                                   float(min_notional_filter['notional']) / price)
                min_trade_qty = ( min_trade_qty * 115  ) /100
                print('min_trade_qty: '+str(min_trade_qty))   
        if min_trade_qty is not None:
            return min_trade_qty
            print("min_trade_qty API RESULE = None")            
        
        print(f"Minimum quantity not found for symbol {symbol}")
        return None
        
    except Exception as e:
        print(f'Error retrieving minimum quantity: {str(e)}')
        return None

    # GET PositionSize

def GETPositionSize(symbol):
    for _ in range(max_retries):
        try:
            OpenOrders = client.futures_coin_account_balance(symbol=symbol)
            time.sleep(0.2)
            account = client.futures_account()
            break  # If the API call is successful, break out of the loop
        except Exception as e:
            print("An error occurred while fetching account information:", str(e))
            time.sleep(delay)
            pass

    else:
        print("Max retries exceeded. Failed to fetch account information.")

    PositionSize = 0

    for b2 in account['positions']:
        if b2['symbol'] == symbol:
            PositionSize = float(b2['positionAmt'])


            

    print('Pos_Size:' + str(PositionSize))
    time.sleep(0.1)


    if PositionSize == 0:
        buyactive = 0
        sellactive = 0


    if PositionSize < 0:
        buyactive = 0
        sellactive = 1
        print('sellactive:' + str(sellactive))
    if PositionSize > 0:
        buyactive = 1
        sellactive = 0
        print('buyactive:' + str(buyactive))

    PositionSize=abs(PositionSize)
    quantity = int(PositionSize)

    if sellactive == 1 and buyactive == 0:
        optimazetrade(symbol, PositionSize)
    if sellactive == 0 and buyactive == 1:
        reducetrade(symbol, PositionSize)


def optimazetrade(symbol, quantity):
    try:
        client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side='BUY',
            quantity=quantity,
            reduceOnly=True
        )
        print("Order BUY executed successfully!")
    except Exception as e:
        error_message = str(e)
        if 'APIError(code=-2019)' in error_message:
            print("Margin is insufficient.")
        else:
            print("An error occurred:", error_message)






            
def reducetrade(symbol, quantity):
    try:
        client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side='SELL',
            quantity=quantity,
            reduceOnly=True
        )
        print("Order executed successfully!")
    except Exception as e:
        error_message = str(e)
        if 'APIError(code=-2019)' in error_message:
            print("Margin is insufficient.")
        else:
            print("An error occurred:", error_message)            
            









get_minimum_quantity(symbol, order_type)


GETPositionSize(symbol)






















