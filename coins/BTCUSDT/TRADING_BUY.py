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


quantity = AMOUNT
symbol = Coin	   	

def optimazetrade(symbol, quantity):
    try:
        client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            side='BUY',
            quantity=quantity
        )
        print("Order BUY executed successfully!")
    except Exception as e:
        error_message = str(e)
        if 'APIError(code=-2019)' in error_message:
            print("Margin is insufficient.")
        else:
            print("An error occurred:", error_message)

optimazetrade(symbol, quantity)

