from binance import Client
import time
from binance import ThreadedWebsocketManager
from binance import AsyncClient
import asyncio
import tkinter as tk
import asyncio
import threading
from binance import AsyncClient, BinanceSocketManager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import atexit
from binance import ThreadedWebsocketManager
import sys
import io
import subprocess
import config

from varmove import Coin
symbol = Coin
	

# Initialize the Binance API client
client = Client(api_key=config.api_key, api_secret=config.api_secret)



# Create a stream for capturing prints
print_stream = io.StringIO()

# Replace the standard output with the print stream
sys.stdout = print_stream

# Define the symbol and limit for the latest trades

limit = 1
trade_logs = []  # List to store the latest trades

async def process_trades(msg):
    if msg['e'] == 'trade':
        trade = msg['data']
        print(f"Trade ID: {trade['t']}")
        print(f"Symbol: {trade['s']}")
        print(f"Price: {trade['p']}")
        print(f"Quantity: {trade['q']}")
        print(f"Buyer Maker: {trade['m']}")
        print("---")
        
        # Add the trade to the trade_logs list
        trade_logs.append({
            'Trade ID': trade['t'],
            'Symbol': trade['s'],
            'Price': trade['p'],
            'Quantity': trade['q'],
            'Buyer Maker': trade['m']
        })
        
        # Keep only the latest two trades in the trade_logs list
        trade_logs = trade_logs[-limit:]


def get_coin_folder(symbol):
    return f"coins/{symbol}"

async def get_latest_trades(symbol, limit):
    # Create an async client
    client = await AsyncClient.create()

    # Create a socket manager
    bsm = BinanceSocketManager(client)

    # Initialize the trade_socket
    trade_socket = bsm.trade_socket(symbol)
    

    async with trade_socket as socket:
        while True:
            # Wait for a trade event
            trade_event = await socket.recv()

            # Process and print the trade event
            print(f"Trade ID: {trade_event['t']}")
            print(f"Symbol: {trade_event['s']}")
            print(f"Price: {trade_event['p']}")
            print(f"Quantity: {trade_event['q']}")
            print(f"Buyer Maker: {trade_event['m']}")
            print("---")

            # Get the captured prints from the print stream
            
            captured_prints = print_stream.getvalue()
            coin_folder = get_coin_folder(symbol)
            with open(f'{coin_folder}/trade_logs.txt', 'w') as file:
                file.write(captured_prints)

            # Reset the print stream
            print_stream.truncate(0)
            print_stream.seek(0)

    # Close the client session
    await client.close_connection()


def start_websocket_stream(symbol, limit):
    asyncio.run(get_latest_trades(symbol, limit))


start_websocket_stream(symbol, 1)  

