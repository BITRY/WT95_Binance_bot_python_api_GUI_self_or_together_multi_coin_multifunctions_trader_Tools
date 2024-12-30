import tkinter as tk
import asyncio
import threading
from binance import AsyncClient, BinanceSocketManager
import config
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import atexit
from binance import ThreadedWebsocketManager
import subprocess
import sys
import datetime
import signal
import psutil
from varmove import Coin
symbol = Coin


# Create a variable to keep track of the subprocess
script_process = None

def start_script(symbol):
    global script_process
    coin_folder = get_coin_folder(symbol)
    if script_process is None:
        # Start the external script (LastestMarketTrades.py)
        script_process = subprocess.Popen(['python3.8', f'{coin_folder}/LastestMarketTrades.py'])
    else:
        print("The script is already running.")

def get_coin_folder(symbol):
    return f"coins/{symbol}"

def display_trade_logs(symbol):
    coin_folder = get_coin_folder(symbol)
    with open(f'{coin_folder}/trade_logs.txt', 'r') as file:
        trade_logs = file.read()

    # Split the trade logs into individual entries
    entries = trade_logs.split('---')

    # Get the latest trade entry
    latest_trade = entries[-2].strip()  # Assuming the last entry is an empty line

    # Extract the Price and Buyer Maker values
    price = float(latest_trade.split('\n')[2].split(': ')[1])
    buyer_maker = latest_trade.split('\n')[4].split(': ')[1]

    # Update the display based on the Buyer Maker value
    if buyer_maker == 'True':
        if price_label["fg"] != 'green':
            # Blink effect for color change (red to green)
            price_label.config(fg='green', font=("Arial", 12))
            root.after(50, lambda: price_label.config(font=("Arial", 15, "bold")))
    else:
        if price_label["fg"] != 'red':
            # Blink effect for color change (green to red)
            price_label.config(fg='red', font=("Arial", 12))
            root.after(50, lambda: price_label.config(font=("Arial", 15, "bold")))

    price_label.config(text=f"{symbol} = {price:.2f} USDT")

    # Update the chart with the latest price
    chart_data.append(price)
    chart.clear()
    chart.plot(chart_data, 'b-')
    update_chart_scale()
    chart_canvas.draw()

    # Schedule the next update after 500ms
    root.after(500, display_trade_logs, symbol)

def update_chart_scale():
    elapsed_time = datetime.datetime.now() - start_time
    seconds = elapsed_time.total_seconds()
    if seconds >= 60:
        minutes = seconds / 60
        chart.set_xlabel("Time (minutes)")
    else:
        chart.set_xlabel("Time (seconds)")


    
    

# Create the Tkinter root
root = tk.Tk()
root.title("Websockets")
root.geometry("700x240")  # Set the window size

# Create a frame on the left side
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=20)



# Label to display the latest Price
price_label = tk.Label(root, text=f"{symbol}: ", font=("Arial", 12))
price_label.pack(side=tk.TOP, anchor=tk.N, pady=1)


# Create a Figure for the chart
fig = Figure(figsize=(8, 3), dpi=100)
chart = fig.add_subplot(111)

# Create a canvas for the chart
chart_canvas = FigureCanvasTkAgg(fig, master=root)
chart_canvas.get_tk_widget().pack(side=tk.LEFT, padx=20, pady=1)

# Create an empty list for storing chart data
chart_data = []

# Track the start time
start_time = datetime.datetime.now()

# Schedule the first update after 500ms
root.after(500, display_trade_logs, symbol)

def stop_script():
    global script_process
    if script_process is not None:
        # Terminate the subprocess
        script_process.kill()
        script_process = None


def on_closing():
    stop_script()  # Terminate the subprocess
    root.destroy()

def on_root_close():
    stop_script()
    root.destroy()

# Bind a single function to the root's close event
root.protocol("WM_DELETE_WINDOW", on_closing)

start_script(symbol)
# Start the Tkinter event loop
root.mainloop()



