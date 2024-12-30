import tkinter as tk
from tkinter import *
import os
import subprocess
import time
import signal
import psutil
import importlib.machinery
import threading
import webview
import multiprocessing
from tkinter import ttk
from tkinter import ttk, scrolledtext
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from tkinter import messagebox  

# Create the dictionary to store chart windows and webview processes
chart_windows = {}
webview_processes = {}

#BINANCE-PYTHON-API    HOODLER GUI CREATED By M.Ry



APP_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(APP_DIR, '')

NOW_PID_FILE = 'now.pid'
RESTARTER_PID_FILE = 'restarter.pid'


# Set default coin
default_coin = "BTCUSDT"


# Set path to logs
COINS_PATH = "coins"

current_dir = os.getcwd()  # Declare current_dir as a global variable



# Create the labels and entry fields for variables
var_labels = [
    "Coin",
    "TradeAmount",
    "TradeX",
    "setDOWNstart",
    "StopTrades",
    "TakeProfitFromBUY",
    "TakeProfitFromBUYInitial",
    "TakeProfitFromBUY2",
    "TakeProfitFromSELL",
    "TakeProfitFromSELLInitial",
    "ROICloseLevel",
    "ROICloseLevelInitial",
    "spread1",
    "spread1Initial",
    "PosNotFilledXAddLevel",
    "GrowCount",
    "StartGrowDiff",
    "StartGrowDiffInit",
    "StartGrowDiffAdd",
    "StartGrowDiffAddInit"
]


var_entries = []


var_labels2 = [
    "BUY_TakeProfit_COUNTER",
    "SELL_TakeProfit_COUNTER",
    "BUY_Order_ROI_Switcher_COUNTER",
    "SELL_Order_ROI_Switcher_COUNTER"

]

var_entries2 = []

def get_coin_path(coin):
    return os.path.join(TEMPLATES_DIR, 'coins', coin)


def update_variable_values():
    coin = coin_var.get()
    coins_path = f"coins/{coin}"
    varmove_path = f"{coins_path}/varmove.py"
    varmove_path2 = f"{coins_path}/tradehistory2.py"

    if os.path.exists(varmove_path):
        loader = importlib.machinery.SourceFileLoader('varmove', varmove_path)
        varmove_module = loader.load_module()

        var_values = []
        for var_label in var_labels:
            if hasattr(varmove_module, var_label):
                var_value = getattr(varmove_module, var_label)
                var_values.append(var_value)
            else:
                var_values.append(None)

        # Display or update the variable values in your GUI here
        for entry, value in zip(var_entries, var_values):
            if isinstance(entry, tk.Label):
                entry.config(text=value if value is not None else "")
            else:
                entry.delete(0, tk.END)
                entry.insert(tk.END, value if value is not None else "")

    else:
        print("varmove.py not found")

    if os.path.exists(varmove_path2):
        loader = importlib.machinery.SourceFileLoader('tradehistory2', varmove_path2)
        varmove_module = loader.load_module()

        var_values2 = []
        for var_label in var_labels2:
            if hasattr(varmove_module, var_label):
                var_value = getattr(varmove_module, var_label)
                var_values2.append(var_value)
            else:
                var_values2.append(None)

        # Display or update the variable values in your GUI here
        for entry, value in zip(var_entries2, var_values2):
            if isinstance(entry, tk.Label):
                entry.config(text=value if value is not None else "")
            else:
                entry.delete(0, tk.END)
                entry.insert(tk.END, value if value is not None else "")
                

    else:
        print("varmove.py not found")





def initate_BUY_mintrade():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
        if os.path.isfile(NOW_PID_FILE):
            os.chdir(APP_DIR)
            print('Restarter is already running')
        else:
            # Start the restarter script
            buy_coin2(coin)
            time.sleep(2)
            os.chdir(APP_DIR)

    else:
        return f"Coin directory {coin_path} not found"






def start_script():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
        if os.path.isfile(NOW_PID_FILE):
            os.chdir(APP_DIR)
            print('Restarter is already running')
        else:
            # Start the restarter script
            start_process(RESTARTER_PID_FILE, [f'python3.8', f'restarter.py'])

            time.sleep(2)
            os.chdir(APP_DIR)

    else:
        return f"Coin directory {coin_path} not found"






def start_process(pid_file, command):
    process = subprocess.Popen(command)
    with open(pid_file, 'w') as f:
        f.write(str(process.pid))
    print(f'Started process with PID {process.pid}')


def stop_script():
    stop_process(RESTARTER_PID_FILE)
    stop_process(NOW_PID_FILE)


def stop_process(pid_file):
    coin = coin_var.get()
    try:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
    except FileNotFoundError:
        print(f'Directory {coin_path} not found')
        os.chdir(APP_DIR)

    try:
        with open(pid_file) as f:
            pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            os.remove(pid_file)
            print(f'Stopped process with PID {pid}')
    except FileNotFoundError:
        os.remove(pid_file)
        print(f'No such process, old pid deleted')
    except ProcessLookupError:
        os.remove(pid_file)
        print(f'Process with PID {pid} not found, old pid deleted')
    except Exception as e:
        print(f'An error occurred while stopping the process: {str(e)}')
    finally:
        os.chdir(APP_DIR)




# Track if the user is navigating
is_navigating = False

# Function to handle click events on "next" or "back" buttons
def on_button_click():
    global is_navigating
    is_navigating = True
    # Perform navigation actions here

# Function to handle the end of navigation
def on_navigation_end():
    global is_navigating
    is_navigating = False
    # Start or resume log synchronization process here



# Function to schedule log synchronization
def schedule_sync():
    if not is_navigating:
        refresh_logs()
    # Schedule the next synchronization
    root.after(5000, schedule_sync)






def refresh_logs():
    coin = coin_var.get()
    coins_path = f"coins/{coin}"
    log1_path = f"{coins_path}/HODL_INFO.log"
    log3_path = f"{coins_path}/HODL_TRADES.log"

    try:
        with open(log1_path, "r") as f:
            log1_data = f.readlines()
            log1_box_left.delete("1.0", tk.END)
            log1_box_left.insert(tk.END, "".join(log1_data[-122:][::-1]))



            latest_roe = extract_latest_roe(log1_data)
            latest_roe = extract_latest_roe(log1_data)
            roe_var.set(latest_roe)
            trade_amount = extract_trade_amount(log1_data)
            trade_amount_var.set(trade_amount)
            pos_size = extract_pos_size(log1_data)
            pos_size_var.set(pos_size)
            pos_size_test = extract_pos_size_test(log1_data)
            pos_size_test_var.set(pos_size_test)      
                  
            roiclose_level = extract_roiclose_level(log1_data)
            roiclose_level_var.set(roiclose_level)
            
            roiclose_level_sell = extract_roiclose_level_sell(log1_data)
            roiclose_level_sell_var.set(roiclose_level_sell)
            
            takeprofit_level_buy = extract_takeprofit_level_buy(log1_data)
            takeprofit_level_buy_var.set(takeprofit_level_buy)
            takeprofit_level_sell = extract_takeprofit_level_sell(log1_data)
            takeprofit_level_sell_var.set(takeprofit_level_sell)
            


            
        with open(log3_path, "r") as f:
            log3_data = f.readlines()
            log3_box_left.delete("1.0", tk.END)
            log3_box_left.insert(tk.END, "".join(log3_data[-122:][::-1]))
            # Extract other values from log3_data if needed
            # ...
            


    except FileNotFoundError:
        pass



def extract_latest_roe(log_data):
    roe = ""
    for line in reversed(log_data):
        if "ROE:" in line and "%" in line:
            roe = line.split("ROE:")[1].strip()
            break
    roe = roe.replace("%", "")        
    return roe


def extract_trade_amount(log_data):
    trade_amount = ""
    for line in reversed(log_data):
        if "TradeAmount" in line:
            trade_amount = line.split("TradeAmount")[1].strip()
            break
    return trade_amount


def extract_pos_size(log_data):
    pos_size = ""
    for line in reversed(log_data):
        if "                  Pos_Size:" in line:
            pos_size = line.split("                  Pos_Size:")[1].strip()
            break
    return pos_size


def extract_roiclose_level(log_data):
    roiclose_level = ""
    for line in reversed(log_data):
        if "ROICloseLevel_Valve_ Modification_BUY_ON_START:" in line:
            roiclose_level = line.split("ROICloseLevel_Valve_ Modification_BUY_ON_START:")[1].strip()
            break
    return roiclose_level


def extract_pos_size_test(log_data):
    pos_size_test = ""
    for line in reversed(log_data):
        if "PosSizetest:" in line:
            pos_size_test = line.split("PosSizetest: ")[1].strip()
            break
    return pos_size_test


def extract_roiclose_level_sell(log_data):
    roiclose_level_sell = ""
    for line in reversed(log_data):
        if "ROICloseLevel_Valve_ Modification_SELL_ON_START:" in line:
            roiclose_level_sell = line.split("ROICloseLevel_Valve_ Modification_SELL_ON_START")[1].strip()
            break
    return roiclose_level_sell


def extract_takeprofit_level_buy(log_data):
    takeprofit_level_buy = ""
    for line in reversed(log_data):
        if "Takeprofit_Valve_ Modification_BUY_ON_START:" in line:
            takeprofit_level_buy = line.split("Takeprofit_Valve_ Modification_BUY_ON_START:")[1].strip()
            break
    return takeprofit_level_buy


def extract_takeprofit_level_sell(log_data):
    takeprofit_level_sell = ""
    for line in reversed(log_data):
        if "Takeprofit_Valve_ Modification_SELL_ON_START:" in line:
            takeprofit_level_sell = line.split("Takeprofit_Valve_ Modification_SELL_ON_START:")[1].strip()
            break
    return takeprofit_level_sell


def extract_value_from_log(log_data, keyword):
    value = ""
    for line in reversed(log_data):
        if keyword in line:
            value = line.split(keyword)[1].strip()
            break
    return value






def write_variables(index):
    coin = coin_var.get()
    coins_path = f"coins/{coin}"
    varmove_path = f"{coins_path}/varmove.py"
    varmove_path2 = f"{coins_path}/tradehistory2.py"

    Coin = var_entries[0].get()
    TradeAmount = var_entries[1].get()
    TradeX = var_entries[2].get()
    setDOWNstart = var_entries[3].get()
    StopTrades = var_entries[4].get()
    TakeProfitFromBUY = var_entries[5].get()
    TakeProfitFromBUYInitial = var_entries[6].get()
    TakeProfitFromBUY2 = var_entries[7].get()
    TakeProfitFromSELL = var_entries[8].get()
    TakeProfitFromSELLInitial = var_entries[9].get()
    ROICloseLevel = var_entries[10].get()
    ROICloseLevelInitial = var_entries[11].get()
    spread1 = var_entries[12].get()
    spread1Initial = var_entries[13].get()
    PosNotFilledXAddLevel = var_entries[14].get()
    GrowCount = var_entries[15].get()
    StartGrowDiff = var_entries[16].get()
    StartGrowDiffInit = var_entries[17].get()
    StartGrowDiffAdd = var_entries[18].get()
    StartGrowDiffAddInit = var_entries[19].get()





    file_content = f"""\
Coin = '{Coin}'
TradeAmount = {TradeAmount}
TradeX = {TradeX}
setDOWNstart = {setDOWNstart}
StopTrades = {StopTrades}
TakeProfitFromBUY = {TakeProfitFromBUY}
TakeProfitFromBUYInitial = {TakeProfitFromBUYInitial}
TakeProfitFromBUY2 = {TakeProfitFromBUY2}
TakeProfitFromSELL = {TakeProfitFromSELL}
TakeProfitFromSELLInitial = {TakeProfitFromSELLInitial}
ROICloseLevel = {ROICloseLevel}
ROICloseLevelInitial = {ROICloseLevelInitial}
spread1 = {spread1}
spread1Initial = {spread1Initial}
PosNotFilledXAddLevel = {PosNotFilledXAddLevel}
GrowCount = {GrowCount}
StartGrowDiff = {StartGrowDiff}
StartGrowDiffInit = {StartGrowDiffInit}
StartGrowDiffAdd = {StartGrowDiffAdd}
StartGrowDiffAddInit = {StartGrowDiffAddInit}
"""

    print(f"Writing variables to files - Iteration {index+1}")

    # Define subprocess
    process = subprocess.Popen(["python3.8", "-c", f"with open('{varmove_path}', 'w') as file: file.write('''{file_content}''')"])
    process.wait()

    print(f"Finished writing variables for Iteration {index+1}")

    # If not the last iteration, schedule the next iteration
    if index < 5:
        root.after(1243, write_variables, index+1)  # Schedule the next iteration after 1000 ms (1 second)
    else:
        start_writing_variables.config(state="normal")  # Re-enable the button after all iterations are completed

# Function to start writing variables
def start_writing_variables():
    start_writing_variables.config(state=tk.DISABLED)  # Disable the button while writing variables
    write_variables(0)



# Function to check if a coin has a PID file in its coin folder
def has_pid_file(coin):
    coin_folder = f"coins/{coin}"
    pid_file = f"{coin_folder}/now.pid"
    return os.path.isfile(pid_file)
    


# Function to sell a coin
def sell_coin(coin, trade_amount_entry):
    coin_folder = f"coins/{coin}"
    trading_script = f"{coin_folder}/sell.py"

    # Get the value from the input field
    new_amount = trade_amount_entry.get()

    # Call the set_amount function to update the TradeAmount variable
    set_amount(coin, new_amount)

    # Call the trading script with the sell command
    subprocess.run(["python3.8", trading_script, "sell"])
    update_trade_overview_window()

    threading.Thread(target=lambda: set_amount_safe(coin, new_amount)).start()


    
# Function to buy a coin
def savetrade_amount(coin, trade_amount_entry):
    coin_folder = f"coins/{coin}"
    trading_script = f"{coin_folder}/buy.py"

    # Get the value from the input field
    new_amount = trade_amount_entry.get()

    # Call the set_amount function to update the TradeAmount variable
    set_amount_safe(coin, new_amount)
            
    
    

# Function to set the amount for trading
def set_amount(coin, new_amount):
    coin_folder = f"coins/{coin}"
    trading_script = f"{coin_folder}/varmove.py"

    # Read the contents of varmove.py
    with open(trading_script, "r") as file:
        lines = file.readlines()

    # Find the line with the TradeAmount variable and update its value
    for i, line in enumerate(lines):
        if line.startswith("TradeAmount"):
            lines[i] = f"TradeAmount = {new_amount}\n"
            break

    # Write the modified contents back to varmove.py
    with open(trading_script, "w") as file:
        file.writelines(lines)



# Function to set the amount for trading
def set_amount_safe(coin, new_amount):
    coin_folder = f"coins/{coin}"
    trading_script = f"{coin_folder}/varmove.py"

    # Read the contents of varmove.py
    with open(trading_script, "r") as file:
        lines = file.readlines()

    # Find the line with the TradeAmount variable and update its value
    for i, line in enumerate(lines):
        if line.startswith("TradeAmount"):
            lines[i] = f"TradeAmount = {new_amount}\n"
            break

    # Execute the command multiple times with a 1-second interval
    for _ in range(5):
        # Write the modified contents back to varmove.py
        with open(trading_script, "w") as file:
            file.writelines(lines)
        print("Modified varmove.py")
        time.sleep(1)
        
 
# Function to set new_ROICloseLevel
def ROICloseLevel_safe(coin, new_ROICloseLevel):
    coin_folder = f"coins/{coin}"
    trading_script = f"{coin_folder}/varmove.py"

    # Read the contents of varmove.py
    with open(trading_script, "r") as file:
        lines = file.readlines()

    # Find the line with the TradeAmount variable and update its value
    for i, line in enumerate(lines):
        if line.startswith("ROICloseLevel"):
            lines[i] = f"ROICloseLevel = {new_ROICloseLevel}\n"
            break

    # Execute the command multiple times with a 1-second interval
    for _ in range(5):
        # Write the modified contents back to varmove.py
        with open(trading_script, "w") as file:
            file.writelines(lines)
        print("Modified varmove.py")
        time.sleep(1)       


# Function to set the new_ROICloseLevelInitial
def ROICloseLevelInitial_safe(coin, new_ROICloseLevelInitial):
    coin_folder = f"coins/{coin}"
    trading_script = f"{coin_folder}/varmove.py"

    # Read the contents of varmove.py
    with open(trading_script, "r") as file:
        lines = file.readlines()

    # Find the line with the TradeAmount variable and update its value
    for i, line in enumerate(lines):
        if line.startswith("ROICloseLevelInitial"):
            lines[i] = f"ROICloseLevelInitial = {new_ROICloseLevelInitial}\n"
            break

    # Execute the command multiple times with a 1-second interval
    for _ in range(5):
        # Write the modified contents back to varmove.py
        with open(trading_script, "w") as file:
            file.writelines(lines)
        print("Modified varmove.py")
        time.sleep(1)   

            

# Create the trade overview window
overview_window = None



def open_trade_overview_window():
    global overview_window

    # Check if the trade overview window is already open
    if overview_window is not None and overview_window.winfo_exists():
        overview_window.deiconify()  # Restore the window if it was minimized
        return

    # Create a new top-level window
    overview_window = tk.Toplevel(root)
    overview_window.title("Trade Overview")

    # Create a frame to hold the coin information
    coin_frame = tk.Frame(overview_window)
    coin_frame.grid()

    def open_set_coin_variables(coin):
        SetCoinVariables(coin_frame, coin)

    for widget in coin_frame.winfo_children():
        widget.destroy()
        
    def close_open_trade_overview_window():
        overview_window.destroy()

    # Schedule the closing of the window after 10 minutes (600 seconds)
    overview_window.after(600000, close_open_trade_overview_window)
    
    
            

    
    def update_trade_overview_window():
        # Clear the previous content
        for widget in coin_frame.winfo_children():
            widget.destroy()
    
        # Iterate through each coin folder and extract relevant information
        coin_info = []
        for coin in coins_list:
            coin_folder = f"coins/{coin}"
            pid_file = f"{coin_folder}/now.pid"
            # Check if the coin has an active trade (PID file exists)
            if has_pid_file(coin):
                # Read the log data to extract the latest ROE value
                log_file = f"{coin_folder}/HODL_INFO.log"
                
                try:
                    with open(log_file, "r") as file:
                        log_data = file.readlines()
                    latest_roe = extract_latest_roe(log_data)
                    roiclose_level = extract_roiclose_level(log_data)
                    takeprofit_level_buy = extract_takeprofit_level_buy(log_data)
                    takeprofit_level_sell = extract_takeprofit_level_sell(log_data)
                    pos_size = extract_pos_size(log_data)
                    pos_size_test = extract_pos_size_test(log_data)
    
                    tradehistory_file = f"{coin_folder}/tradehistory2.py"
                    loader = importlib.machinery.SourceFileLoader('tradehistory', tradehistory_file)
                    tradehistory_module = loader.load_module()
    
                    # Extract the variable values from the tradehistory module
                    buy_takeprofit_counter = getattr(tradehistory_module, "BUY_TakeProfit_COUNTER", None)
                    sell_takeprofit_counter = getattr(tradehistory_module, "SELL_TakeProfit_COUNTER", None)
                    buy_order_roi_switcher_counter = getattr(tradehistory_module, "BUY_Order_ROI_Switcher_COUNTER", None)
                    sell_order_roi_switcher_counter = getattr(tradehistory_module, "SELL_Order_ROI_Switcher_COUNTER", None)
    
                    varmove_file = f"{coin_folder}/varmove.py"
                    loader = importlib.machinery.SourceFileLoader('varmove', varmove_file)
                    varmove_module = loader.load_module()
    
                    # Extract the variable values from the varmove module
                    spread1 = getattr(varmove_module, "spread1", None)
                    trade_amount = getattr(varmove_module, "TradeAmount", None)
                    ROICloseLevel = getattr(varmove_module, "ROICloseLevel", None)
                    ROICloseLevelInitial = getattr(varmove_module, "ROICloseLevelInitial", None)
    
                    mintrade_file = f"{coin_folder}/mintrade.py"
                    loader = importlib.machinery.SourceFileLoader('mintrade', mintrade_file)
                    mintrade_module = loader.load_module()
    
                    # Extract the variable values from the mintrade module
                    mintrade = getattr(mintrade_module, "min_trade_qty", None)
    
                    lastprice_file = f"{coin_folder}/lastprice.py"
                    loader = importlib.machinery.SourceFileLoader('average_price', lastprice_file)
                    lastprice_module = loader.load_module()
    
                    # Extract the variable values from the lastprice module
                    average_price = getattr(lastprice_module, "average_price", None)
    
                    lastprice_file = f"{coin_folder}/lastprice.py"
                    loader = importlib.machinery.SourceFileLoader('mark_price', lastprice_file)
                    lastprice_module = loader.load_module()
    
                    # Extract the variable values from the lastprice module
                    mark_price = getattr(lastprice_module, "mark_price", None)
    
                    lastprice_file = f"{coin_folder}/lastprice.py"
                    loader = importlib.machinery.SourceFileLoader('PNL', lastprice_file)
                    lastprice_module = loader.load_module()
    
                    # Extract the variable values from the lastprice module
                    PNL = getattr(lastprice_module, "PNL", None)
    
                    # Convert relevant variables to numeric type and round to 2 decimal places
                    latest_roe = 0
                    
                    roiclose_level = round(float(roiclose_level), 2)
                    takeprofit_level_buy = round(float(takeprofit_level_buy), 2)
                    takeprofit_level_sell = round(float(takeprofit_level_sell), 2)
                    pos_size = round(float(pos_size), 2)
                    if pos_size_test:
                        pos_size_test = round(float(pos_size_test), 2)
                    else:
                        # Handle the case when the string is empty
                        pos_size_test = 0.0  # or any other appropriate value
    
                    trade_amount = round(float(trade_amount), 4)                    
                    ROICloseLevel = round(float(ROICloseLevel), 2)                    
                    buy_takeprofit_counter = round(float(buy_takeprofit_counter), 2)
                    sell_takeprofit_counter = round(float(sell_takeprofit_counter), 2)
                    buy_order_roi_switcher_counter = round(float(buy_order_roi_switcher_counter), 2)
                    sell_order_roi_switcher_counter = round(float(sell_order_roi_switcher_counter), 2)
                    spread1 = round(float(spread1), 2)
                    mintrade = round(float(mintrade), 4)
    
                    if average_price is not None:
                        average_price = round(float(average_price), 4)
                    else:
                        average_price = 0.0  
    
                    if mark_price is not None:
                        mark_price = round(float(mark_price), 4)
                    else:
                        mark_price = 0.0  
    
                    if PNL is not None:
                        PNL = round(float(PNL), 4)
                    else:
                        PNL = 0.0  
    
                    # Store the coin information in a tuple
                    coin_info.append((
                        coin, coin, coin, latest_roe, roiclose_level, takeprofit_level_buy, takeprofit_level_sell,
                        pos_size, pos_size_test, trade_amount, buy_takeprofit_counter,
                        sell_takeprofit_counter, buy_order_roi_switcher_counter,
                        sell_order_roi_switcher_counter, spread1, mintrade, average_price, mark_price, PNL, ROICloseLevel, ROICloseLevelInitial, coin, coin))
                except FileNotFoundError:
                    pass
    
        # Sort the coin information based on the coin name in alphabetical order
        coin_info.sort(key=lambda x: x[0])
    
        coin_info_numeric = []
        for row in coin_info:
            numeric_row = []
            for val in row:
                if isinstance(val, str):
                    try:
                        numeric_row.append(float(val))
                    except ValueError:
                        numeric_row.append(0.0)  # Treat non-numeric values as 0
                else:
                    numeric_row.append(val)  # Keep non-string values unchanged
            coin_info_numeric.append(numeric_row)
    
        # Calculate the sums for each column
        column_sums = [sum(filter(lambda x: isinstance(x, (int, float)), column)) for column in zip(*coin_info_numeric)]
   
        # Create a frame for the sum labels
        sum_frame = tk.Frame(overview_window)
        sum_frame.grid(row=len(coin_info) + 1, column=0, columnspan=44, sticky="ew")
        
        # Display the sums for each column separately in the sum frame
        column_labels = [
            "Coin", "NV", "NV", "L_ROE", "R_Close", "TP_Buy", "TP_Sell", "PosSz", "PosSzTest", "TA", "BTPCont", "STPCont",
            "BOrdSwitCount", "SOrdSwitCount", "Sprd1", "MinTr", "AvPrice", "MkPrice", "PNL", "RClosLev", "RClosLevInit",
            "NV", "NV"
        ]  # Adjust column labels according to your data
    
        for col, (label, sum_value) in enumerate(zip(column_labels, column_sums)):
            sum_label_text = "{}: {:.2f}".format(label, sum_value) if sum_value != 0 else "{}: NV".format(label)
            sum_label = tk.Label(sum_frame, text=sum_label_text, font=("Arial", 10, "bold"))
            sum_label.grid(row=0, column=col, sticky="w", padx=1, pady=0.5)  # Display sum labels in the sum frame
     
        # Display the sorted coin information in the trade overview window
        for row, coin_data in enumerate(coin_info):
            # Extract coin data
            coin, coin, coin, latest_roe, roiclose_level, takeprofit_level_buy, takeprofit_level_sell, pos_size, pos_size_test, \
            trade_amount, buy_takeprofit_counter, sell_takeprofit_counter, buy_order_roi_switcher_counter, \
            sell_order_roi_switcher_counter, spread1, mintrade, average_price, mark_price, PNL, ROICloseLevel, \
            ROICloseLevelInitial, coin, coin = coin_data  # Adjust as per your data
    
            small_font = ("Arial", 10)
            small_button_style = {"font": small_font, "padx": 1, "pady": 0.5}
    
            text_color = "#410807"  # Default text color
            text_color2 = "#C41263"  # Default text color
            text_color3 = "#F50721"  # Default text color
    
            # Create labels to display the coin name and relevant information
            coin_label = tk.Button(overview_window, text=coin, fg=text_color, **small_button_style)
            coin_label.grid(row=row, column=0, padx=1, pady=0.5)
            coin_label.bind("<Button-1>", lambda event, coin=coin_label.cget("text"): SetCoinVariables(coin_frame, coin))
    
            coin_label3 = tk.Button(overview_window, text="TRADING", fg=text_color2, **small_button_style)
            coin_label3.grid(row=row, column=1, padx=1, pady=0.5)
            coin_label3.bind("<Button-1>", lambda event, coin=coin_label.cget("text"): TRADING(coin_frame, coin))
    
            coin_label2 = tk.Button(overview_window, text="CHART", fg=text_color3, **small_button_style)
            coin_label2.grid(row=row, column=2, padx=1, pady=0.5)
            coin_label2.bind("<Button-1>", lambda event, coin=coin: open_chart_window(coin))
    
            roe_label = tk.Label(overview_window, text="ROE:", fg=text_color, font=("Arial", 10))
            roe_label.grid(row=row, column=3, padx=1, pady=0.5)
    
            roe_value_label = tk.Label(overview_window, text="{:.2f}".format(latest_roe), font=("Arial", 10, "bold"))
            roe_value_label.grid(row=row, column=4, padx=1, pady=0.5)
    
            PNL_label = tk.Label(overview_window, text="PNL:", fg=text_color, font=("Arial", 10))
            PNL_label.grid(row=row, column=5, padx=1, pady=0.5)
    
            PNL_value_label = tk.Label(overview_window, text="{:.2f}".format(PNL), font=("Arial", 10, "bold"))
            PNL_value_label.grid(row=row, column=6, padx=1, pady=0.5)
    
            roiclose_label = tk.Label(overview_window, text="roecls:", fg=text_color, font=("Arial", 10))
            roiclose_label.grid(row=row, column=7, padx=1, pady=0.5)
    
            roiclose_value_label = tk.Label(overview_window, text="{:.2f}".format(roiclose_level), font=("Arial", 10, "bold"))
            roiclose_value_label.grid(row=row, column=8, padx=1, pady=0.5)
    
            takeprofit_level_buy_label = tk.Label(overview_window, text="TP_lvl_B:", fg=text_color, font=("Arial", 10))
            takeprofit_level_buy_label.grid(row=row, column=9, padx=1, pady=0.5)
    
            takeprofit_level_buy_value_label = tk.Label(overview_window, text="{:.2f}".format(takeprofit_level_buy), font=("Arial", 10, "bold"))
            takeprofit_level_buy_value_label.grid(row=row, column=10, padx=1, pady=0.5)
    
            takeprofit_level_sell_label = tk.Label(overview_window, text="TP_lvl_S:", fg=text_color, font=("Arial", 10))
            takeprofit_level_sell_label.grid(row=row, column=11, padx=1, pady=0.5)
    
            takeprofit_level_sell_value_label = tk.Label(overview_window, text="{:.2f}".format(takeprofit_level_sell), font=("Arial", 10, "bold"))
            takeprofit_level_sell_value_label.grid(row=row, column=12, padx=1, pady=0.5)
    
            pos_size_label = tk.Label(overview_window, text="pos_sz:", fg=text_color, font=("Arial", 10))
            pos_size_label.grid(row=row, column=13, padx=1, pady=0.5)
    
            pos_size_sell_value_label = tk.Label(overview_window, text="{:.2f}".format(pos_size), font=("Arial", 10, "bold"))
            pos_size_sell_value_label.grid(row=row, column=14, padx=1, pady=0.5)
    
            pos_size_test_label = tk.Label(overview_window, text="pos_sz_X:", fg=text_color, font=("Arial", 10))
            pos_size_test_label.grid(row=row, column=15, padx=1, pady=0.5)
    
            pos_size_test_sell_value_label = tk.Label(overview_window, text="{:.2f}".format(pos_size_test), font=("Arial", 10, "bold"))
            pos_size_test_sell_value_label.grid(row=row, column=16, padx=1, pady=0.5)
    
            trade_amount_label = tk.Label(overview_window, text="Amt:", fg=text_color, font=("Arial", 10))
            trade_amount_label.grid(row=row, column=17, padx=1, pady=0.5)
    
            trade_amount_sell_value_label = tk.Label(overview_window, text="{:.2f}".format(trade_amount), font=("Arial", 10, "bold"))
            trade_amount_sell_value_label.grid(row=row, column=18, padx=1, pady=0.5)
    
            buy_takeprofit_counter_label = tk.Label(overview_window, text="B_TP:", fg=text_color, font=("Arial", 10))
            buy_takeprofit_counter_label.grid(row=row, column=19, padx=1, pady=0.5)
    
            buy_takeprofit_counter_value_label = tk.Label(overview_window, text="{:.2f}".format(buy_takeprofit_counter), font=("Arial", 10, "bold"))
            buy_takeprofit_counter_value_label.grid(row=row, column=20, padx=1, pady=0.5)
    
            sell_takeprofit_counter_label = tk.Label(overview_window, text="S_TP:", fg=text_color, font=("Arial", 10))
            sell_takeprofit_counter_label.grid(row=row, column=21, padx=1, pady=0.5)
    
            sell_takeprofit_counter_value_label = tk.Label(overview_window, text="{:.2f}".format(sell_takeprofit_counter), font=("Arial", 10, "bold"))
            sell_takeprofit_counter_value_label.grid(row=row, column=22, padx=1, pady=0.5)
    
            buy_order_roi_switcher_counter_label = tk.Label(overview_window, text="B_ROE:", fg=text_color, font=("Arial", 10))
            buy_order_roi_switcher_counter_label.grid(row=row, column=23, padx=1, pady=0.5)
    
            buy_order_roi_switcher_counter_value_label = tk.Label(overview_window, text="{:.2f}".format(buy_order_roi_switcher_counter), font=("Arial", 10, "bold"))
            buy_order_roi_switcher_counter_value_label.grid(row=row, column=24, padx=1, pady=0.5)
    
            sell_order_roi_switcher_counter_label = tk.Label(overview_window, text="S_ROE:", fg=text_color, font=("Arial", 10))
            sell_order_roi_switcher_counter_label.grid(row=row, column=25, padx=1, pady=0.5)
    
            sell_order_roi_switcher_counter_value_label = tk.Label(overview_window, text="{:.2f}".format(sell_order_roi_switcher_counter), font=("Arial", 10, "bold"))
            sell_order_roi_switcher_counter_value_label.grid(row=row, column=26, padx=1, pady=0.5)
    
            spread1_label = tk.Label(overview_window, text="spr_1:", fg=text_color, font=("Arial", 10))
            spread1_label.grid(row=row, column=27, padx=1, pady=0.5)
    
            spread1_value_label = tk.Label(overview_window, text="{:.2f}".format(spread1), font=("Arial", 10, "bold"))
            spread1_value_label.grid(row=row, column=28, padx=1, pady=0.5)
    
            mintrade_label = tk.Label(overview_window, text="min_t:", fg=text_color, font=("Arial", 10))
            mintrade_label.grid(row=row, column=29, padx=1, pady=0.5)
    
            mintrade_value_label = tk.Label(overview_window, text="{:.2f}".format(mintrade), font=("Arial", 10, "bold"))
            mintrade_value_label.grid(row=row, column=30, padx=1, pady=0.5)
    
            average_price_label = tk.Label(overview_window, text="a_price:", fg=text_color, font=("Arial", 10))
            average_price_label.grid(row=row, column=31, padx=1, pady=0.5)
    
            average_price_value_label = tk.Label(overview_window, text="{:.2f}".format(average_price), font=("Arial", 10, "bold"))
            average_price_value_label.grid(row=row, column=32, padx=1, pady=0.5)
    
            mark_price_label = tk.Label(overview_window, text="m_price:", fg=text_color, font=("Arial", 10))
            mark_price_label.grid(row=row, column=33, padx=1, pady=0.5)
    
            mark_price_value_label = tk.Label(overview_window, text="{:.2f}".format(mark_price), font=("Arial", 10, "bold"))
            mark_price_value_label.grid(row=row, column=34, padx=1, pady=0.5)
            
            coin_label4 = tk.Button(overview_window, text="Live", fg=text_color3,  **small_button_style)
            coin_label4.grid(row=row, column=42, padx=1, pady=0.5)
            coin_label4.bind("<Button-1>", lambda event, coin=coin: Live(coin))   
    
            coin_label5 = tk.Button(overview_window, text="PriceStream", fg=text_color3,  **small_button_style)
            coin_label5.grid(row=row, column=43, padx=1, pady=0.5)
            coin_label5.bind("<Button-1>", lambda event, coin=coin: PriceStream(coin))   
    
            # Create the input field to update the trade amount
            trade_amount_var = tk.StringVar(value="{:.5f}".format(trade_amount))          
           
            trade_amount_entry = tk.Entry(overview_window, textvariable=trade_amount_var, font=("Arial", 10), width=5)
            trade_amount_entry.grid(row=row, column=35, padx=1, pady=0.5)
    
            def buy_coin(coin, trade_amount_entry):
                coin_folder = f"coins/{coin}"
                trading_script = f"{coin_folder}/buy.py"
    
                # Get the value from the input field
                # new_amount = trade_amount_entry.get()
    
                # Call the set_amount function to update the TradeAmount variable
                # set_amount(coin, new_amount)
    
                # Call the trading script with the buy command
                subprocess.run(["python3.8", trading_script, "buy"])
    
                # threading.Thread(target=lambda: set_amount_safe(coin, new_amount)).start()            
    
            buy_button = tk.Button(overview_window, text="Buy", command=lambda c=coin, tae=trade_amount_entry: buy_coin(c, tae), **small_button_style)
            buy_button.grid(row=row, column=36, padx=1, pady=0.5)
    
            def sell_coin(coin, trade_amount_entry):
                coin_folder = f"coins/{coin}"
                trading_script = f"{coin_folder}/sell.py"
    
                # Get the value from the input field
                # new_amount = trade_amount_entry.get()
    
                # Call the set_amount function to update the TradeAmount variable
                # set_amount(coin, new_amount)
    
                # Call the trading script with the sell command
                subprocess.run(["python3.8", trading_script, "sell"])
    
                # threading.Thread(target=lambda: set_amount_safe(coin, new_amount)).start()
                            
            sell_button = tk.Button(overview_window, text="Sell", command=lambda c=coin, tae=trade_amount_entry: sell_coin(c, tae), **small_button_style)
            sell_button.grid(row=row, column=37, padx=1, pady=0.5)  
    
            def save_button(coin, ROICloseLevel_entry):
                # Get the value from the input field
                new_ROICloseLevel = ROICloseLevel_entry.get()
    
                # Call the ROICloseLevel_safe function to update the ROICloseLevel variable
                ROICloseLevel_safe(coin, new_ROICloseLevel)
    
                threading.Thread(target=lambda: ROICloseLevel_safe(coin, new_ROICloseLevel)).start()
    
            ROICloseLevel_var = tk.StringVar(value="{:.0f}".format(ROICloseLevel))
    
            ROICloseLevel_entry = tk.Entry(overview_window, textvariable=ROICloseLevel_var, font=("Arial", 10), width=5)
            ROICloseLevel_entry.grid(row=row, column=38, padx=1, pady=0.5)
            
            save_button = tk.Button(overview_window, text="NewRO", command=lambda c=coin, ROIC=ROICloseLevel_entry: save_button(c, ROIC), **small_button_style)
            save_button.grid(row=row, column=39, padx=1, pady=0.5)       
    
            ROICloseLevelInitial_var = tk.StringVar(value="{:.0f}".format(ROICloseLevelInitial))
    
            ROICloseLevelInitial_entry = tk.Entry(overview_window, textvariable=ROICloseLevelInitial_var, font=("Arial", 10), width=5)
            ROICloseLevelInitial_entry.grid(row=row, column=40, padx=1, pady=0.5)
    
            save_button = tk.Button(overview_window, text="InitRO", command=lambda c=coin, ROICI=ROICloseLevelInitial_entry: save_button(c, ROICI), **small_button_style)
            save_button.grid(row=row, column=41, padx=1, pady=0.5)     
    
        def Live(coin):
            coin_folder = f"coins/{coin}"
            liveorderbook_script = f"{coin_folder}/liveorderbook.py"
            subprocess.Popen(["python3.8", liveorderbook_script, "liveorderbook_script"])
            os.chdir(current_dir)  # Restore the original working directory
    
        def PriceStream(coin):
            coin_folder = f"coins/{coin}"
            pricestream_script = f"{coin_folder}/websocket.py"
            subprocess.Popen(["python3.8", pricestream_script, "pricestream_script"])
            os.chdir(current_dir)  # Restore the original working directory
    
    
        root.after(60000, update_trade_overview_window)  # Refresh every 10 seconds     
    
    # Call the update function initially
    update_trade_overview_window()



                        





# Create the dictionary to store chart windows and webview processes
chart_windows = {}
webview_processes = {}


def open_chart_window(coin):
    # Check if the chart window is already open for the coin

        
    if coin in chart_windows:
        chart_window = chart_windows[coin]
        if chart_window is not None and chart_window.winfo_exists():
            chart_window.deiconify()  # Restore the window if it was minimized
            print(f"Chart window for {coin} already open")
            return
    root.protocol("WM_DELETE_WINDOW", on_chart_window_close)
    symbol = coin
    chart_html = f'''
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_c7e01"></div>
      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {{
        "autosize": true,
        "symbol": "BINANCE:{symbol}",
        "interval": "1",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_c7e01"
      }});
      </script>
    </div>
    <!-- TradingView Widget END -->
    '''

    # Create a separate process for the webview window
    webview_process = multiprocessing.Process(target=create_webview, args=(coin, chart_html))
    webview_process.start()

    # Store the chart window and webview process in the dictionary
    chart_windows[coin] = None  # Placeholder for now
    webview_processes[coin] = webview_process


def create_webview(coin, chart_html):
    # Create a WebView
    webview.create_window(
        title=f"Chart for {coin}",
        html=chart_html,
        width=450,
        height=380,
        resizable=True
    )
    webview.start()


def on_chart_window_close():
    global chart_windows
    global webview_processes

    # Check if the chart windows exist and destroy them
    for coin, chart_window in chart_windows.items():
        if chart_window is not None and chart_window.winfo_exists():
            chart_window.destroy()
            print(f"Chart window for {coin} closed")

    # Clear the chart windows dictionary
    chart_windows = {}

    # Terminate the webview processes if they are running
    for coin, webview_process in webview_processes.items():
        if webview_process and webview_process.is_alive():
            webview_process.terminate()
            webview_process.join()
            print(f"WebView process for {coin} terminated")

    # Clear the webview processes dictionary
    webview_processes = {}





TRADING_variables_window = None  # Declare the global variable



        
coin_info = []  # Define coin_info as a global variable

def TRADING(coin_frame, coin):
    global TRADING_variables_window
    global trade_amount_entry
    global X_Time_Order

    for widget in coin_frame.winfo_children():
        widget.destroy()
        

    # Create a new top-level window
    TRADING_variables_window = tk.Toplevel(root)
    TRADING_variables_window.title("TRADING")

    # Create a frame to hold the coin information
    coin_frame = tk.Frame(TRADING_variables_window)
    coin_frame.pack()


    # Function to handle the ESC key press event
    def on_escape(event):
        TRADING_variables_window.destroy()  # Close the window

    # Bind the on_escape function to the ESC key press event
    TRADING_variables_window.bind("<Escape>", on_escape)

    def close_TRADING_variables_window():
        TRADING_variables_window.destroy()

    # Schedule the closing of the window after 2 minutes (120 seconds)
    TRADING_variables_window.after(300000, close_TRADING_variables_window)

    def update_TRADING():
        # Clear the previous content
        for widget in coin_frame.winfo_children():
            widget.destroy()

        coin_folder = f"coins/{coin}"
        AMOUNT_file = f"{coin_folder}/AMOUNT.py"
        loader = importlib.machinery.SourceFileLoader('AMOUNT', AMOUNT_file)
        AMOUNT_module = loader.load_module()

        # Extract the variable values from the AMOUNT module
        AMOUNT = getattr(AMOUNT_module, "AMOUNT", None)
        X_Time_Order = getattr(AMOUNT_module, "X_Time_Order", None)
        
        pricediff_file = f"{coin_folder}/pricediff.py"
        loader = importlib.machinery.SourceFileLoader('pricediff', pricediff_file)
        pricediff_module = loader.load_module()
        # Extract the variable values from the AMOUNT module
        pricediff = getattr(pricediff_module, "pricediff", None)



        coin_info.clear()  # Clear the coin_info list

        coin_info.append(
            {
                "Coin": str(coin),
                "AMOUNT": AMOUNT,
                "X_Time_Order": X_Time_Order,
                "pricediff": pricediff
            }
        )

        # Function to save the values when Enter key is pressed
        def save_values(event=None):
        
        
            for i, coin_data in enumerate(coin_info):
                coin_data["Coin"] = f"'{coin}'"
                coin_data["AMOUNT"] = trade_amount_entry.get()    
                coin_data["X_Time_Order"] = X_Time_Order_entry.get()              
                coin_folder = f"coins/{coin}"
                AMOUNT_file = f"{coin_folder}/AMOUNT.py"
                with open(AMOUNT_file, 'w') as f:
                    for key, value in coin_info[0].items():
                        if key == "coin":
                            f.write(f"{key} = '{value}'\n")
                        else:
                            f.write(f"{key} = {value}\n")  




   
        # Function to save the values when Enter key is pressed
        def save_valuesScale(event=None):
        
        
            for i, coin_data in enumerate(coin_info):
                coin_data["Coin"] = f"'{coin}'"
                coin_data["AMOUNT"] = AMOUNT_scale.get()
                coin_data["X_Time_Order"] = X_Time_Order_scale.get()
               
                coin_folder = f"coins/{coin}"
                AMOUNT_file = f"{coin_folder}/AMOUNT.py"
                with open(AMOUNT_file, 'w') as f:
                    for key, value in coin_info[0].items():
                        if key == "coin":
                            f.write(f"{key} = '{value}'\n")
                        else:
                            f.write(f"{key} = {value}\n")     



        # Function to save the values when Enter key is pressed
        def save_values_pricediff_Scale(event=None):
                    
   
            for i, coin_data in enumerate(coin_info):
                coin_data["pricediff"] = pricediff_scale.get()

               
                coin_folder = f"coins/{coin}"
                pricediff_file = f"{coin_folder}/pricediff.py"
                with open(pricediff_file, 'w') as f:
                    for key, value in coin_info[0].items():
                        if key == "pricediff":
                            f.write(f"{key} = {value}\n")



        AMOUNT_file = f"{coin_folder}/AMOUNT.py"
        loader = importlib.machinery.SourceFileLoader('AMOUNT', AMOUNT_file)
        AMOUNT_module = loader.load_module()

        # Extract the variable values from the AMOUNT module
        AMOUNT = getattr(AMOUNT_module, "min_trade_qty", None)
        # Extract the variable values from the AMOUNT module
        X_Time_Order = getattr(X_Time_Order, "min_trade_qty", None)


        pricediff_file = f"{coin_folder}/pricediff.py"
        loader = importlib.machinery.SourceFileLoader('pricediff', pricediff_file)
        pricediff_module = loader.load_module()
        # Extract the variable values from the AMOUNT module
        pricediff = getattr(pricediff_module, "pricediff", None)



        mintrade_file = f"{coin_folder}/mintrade.py"
        loader = importlib.machinery.SourceFileLoader('mintrade', mintrade_file)
        mintrade_module = loader.load_module()

        # Extract the variable values from the mintrade module
        mintrade = getattr(mintrade_module, "min_trade_qty", None)
        mintrade = round(float(mintrade), 4)


   
   
                     

        # Display the coin information in the set coin variables window
        row = 0
        for field_name, field_value in coin_info[0].items():
            field_label = tk.Label(coin_frame, text=field_name, font=("Arial", 10, "bold"))
            field_label.grid(row=row, column=0, padx=10, pady=2, sticky="w")

            # Create entry widgets for each field

            if field_name == "AMOUNT":
                trade_amount_entry = tk.Entry(coin_frame, width=10)
                trade_amount_entry.grid(row=row, column=1, padx=10, pady=2, sticky="w")
                trade_amount_entry.insert(0, field_value)
                trade_amount_entry.config(validate="key")
                trade_amount_entry.config(validatecommand=(trade_amount_entry.register(validate_float), "%P"))
                trade_amount_entry.bind("<Return>", save_values)
                row += 1
        
                AMOUNT_scale = tk.Scale(
                    coin_frame,
                    from_=mintrade,
                    to=(mintrade*200) if field_name == "AMOUNT" else 25,
                    resolution = mintrade/2  if field_name == "AMOUNT" else 1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=10,
                )
                AMOUNT_scale.set(float(field_value))
                AMOUNT_scale.grid(row=row, column=1, sticky="w")
                AMOUNT_scale.bind("<ButtonRelease-1>", save_valuesScale)
                row += 1
                

            elif field_name == "X_Time_Order":
                X_Time_Order_entry = tk.Entry(coin_frame, width=10)
                X_Time_Order_entry.grid(row=row, column=1, padx=10, pady=2, sticky="w")
                X_Time_Order_entry.insert(0, field_value)
                X_Time_Order_entry.config(validate="key")
                X_Time_Order_entry.config(validatecommand=(X_Time_Order_entry.register(validate_float), "%P"))
                X_Time_Order_entry.bind("<Return>", save_values)
                row += 1
        
                X_Time_Order_scale = tk.Scale(
                    coin_frame,
                    from_=1,
                    to=25,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                X_Time_Order_scale.set(float(field_value))
                X_Time_Order_scale.grid(row=row, column=1, sticky="w")
                X_Time_Order_scale.bind("<ButtonRelease-1>", save_valuesScale)               
                row += 1                           
                           

            elif field_name == "pricediff":
                pricediff_entry = tk.Entry(coin_frame, width=10)
                pricediff_entry.grid(row=row, column=1, padx=10, pady=2, sticky="w")
                pricediff_entry.insert(0, field_value)
                pricediff_entry.config(validate="key")
                pricediff_entry.config(validatecommand=(pricediff_entry.register(validate_float), "%P"))
                pricediff_entry.bind("<Return>", save_values_pricediff_Scale)
                row += 1
        
                pricediff_scale = tk.Scale(
                    coin_frame,
                    from_=0.00,
                    to=1,
                    resolution=0.01,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=4,
                )
                pricediff_scale.set(float(field_value))
                pricediff_scale.grid(row=row, column=1, padx=10, pady=2, sticky="w")
                pricediff_scale.bind("<ButtonRelease-1>", save_values_pricediff_Scale)               
                row += 1




            def NEWSTOPMARKET_script(coin, pricediff_entry):
                coin_folder = f"coins/{coin}"
                TRADING_script = f"{coin_folder}/stop.py"
                stopmarket_script = f"{coin_folder}/pricediff.py"
                pricediff = pricediff_entry.get()
                pricediff = float(pricediff_entry.get())
     
                # Write the pricediff value to stopmarket_script
                with open(stopmarket_script, "r+") as file:
                    lines = file.readlines()
                    lines.insert(0, f"pricediff = {pricediff}\n")
                    file.seek(0)
                    file.writelines(lines)                    
                    
                subprocess.run(["python3.8", TRADING_script, "stopmarket"])





           # Function to buy a coin
            def TRADING_BUY_script(coin, trade_amount_entry, X_Time_Order):
                coin_folder = f"coins/{coin}"
                TRADING_script = f"{coin_folder}/TRADING_BUY.py"
                TRADING_AMOUNT_script = f"{coin_folder}/AMOUNT.py"
               

                AMOUNT = trade_amount_entry.get()
                X_Time_Order = X_Time_Order.get()
                X_Time_Order = int(X_Time_Order)
                


                # Execute the command multiple times with a 1-second interval
                for _ in range(X_Time_Order):
                    # Call the trading script with the buy command
                    subprocess.run(["python3.8", TRADING_script, "buy"])
                    
                    
                # Read the contents of AMOUNT.py
                with open(TRADING_AMOUNT_script, "r") as file:
                    lines = file.readlines()


        


           # Function to buy a coin
            def TRADING_SELL_script(coin, trade_amount_entry, X_Time_Order ):
                coin_folder = f"coins/{coin}"
                TRADING_script = f"{coin_folder}/TRADING_SELL.py"
                TRADING_AMOUNT_script = f"{coin_folder}/AMOUNT.py"
                
                AMOUNT = trade_amount_entry.get()
                X_Time_Order = X_Time_Order.get()
                X_Time_Order = int(X_Time_Order)

 
                    
                    
                # Execute the command multiple times with a 1-second interval
                for _ in range(X_Time_Order):
                    # Call the trading script with the buy command
                    subprocess.run(["python3.8", TRADING_script, "sell"])


                # Read the contents of AMOUNT.py
                with open(TRADING_AMOUNT_script, "r") as file:
                    lines = file.readlines()

                           

           # Function to buy a coin
            def CLOSEPOSITION_script(coin):
                coin_folder = f"coins/{coin}"
                TRADING_script = f"{coin_folder}/CLOSE.py"

     
                    
                    
                subprocess.run(["python3.8", TRADING_script, "sell"])






    

        STOPMARKET_button = tk.Button(TRADING_variables_window, text="SET_STOP_MARKET", command=lambda c=coin, x=pricediff_entry: NEWSTOPMARKET_script(c, x))
        STOPMARKET_button.pack()


        
        BUY_button = tk.Button(TRADING_variables_window, text="BUY", command=lambda c=coin, tae=trade_amount_entry, x=X_Time_Order_entry: TRADING_BUY_script(c, tae, x))
        BUY_button.pack()
        
        SELL_button = tk.Button(TRADING_variables_window, text="SELL", command=lambda c=coin, tae=trade_amount_entry, x=X_Time_Order_entry: TRADING_SELL_script(c, tae, x))
        SELL_button.pack()        
 

        save_button = tk.Button(TRADING_variables_window, text="Save", command=save_values)
        save_button.pack() 
              
        eee_button = tk.Button(TRADING_variables_window, text="CLOSEPOS", command=lambda c=coin: CLOSEPOSITION_script(c))
        eee_button.pack()
        
              


    # Call the update function initially
    update_TRADING()

    # Schedule the update function every 5 seconds (5000 milliseconds)
    TRADING_variables_window.after(25000, update_TRADING)








        
coin_info = []  # Define coin_info as a global variable

def SetCoinVariables(coin_frame, coin):
    global set_coin_variables_window
    global trade_amount_entry
    global trade_x_entry
    global set_down_start_entry
    global stop_trades_entry
    global take_profit_buy_entry
    global take_profit_buy_initial_entry
    global take_profit_buy2_entry
    global take_profit_sell_entry
    global take_profit_sell_initial_entry
    global roi_close_level_entry
    global roi_close_level_initial_entry
    global spread1_entry
    global spread1Initial_entry
    global PosNotFilledXAddLevel
    global pricediff

    for widget in coin_frame.winfo_children():
        widget.destroy()
        

    # Create a new top-level window
    set_coin_variables_window = tk.Toplevel(root)
    set_coin_variables_window.title("SetCoinVariables")

    # Create a frame to hold the coin information
    coin_frame = tk.Frame(set_coin_variables_window)
    coin_frame.pack()

    for widget in coin_frame.winfo_children():
        widget.destroy()

    # Function to handle the ESC key press event
    def on_escape(event):
        set_coin_variables_window.destroy()  # Close the window

    # Bind the on_escape function to the ESC key press event
    set_coin_variables_window.bind("<Escape>", on_escape)

    def close_set_coin_variables_window():
        set_coin_variables_window.destroy()

    # Schedule the closing of the window after 2 minutes (120 seconds)
    set_coin_variables_window.after(15000, close_set_coin_variables_window)


    def update_SetCoinVariables():
        # Clear the previous content
        for widget in coin_frame.winfo_children():
            widget.destroy()

        coin_folder = f"coins/{coin}"
        varmove_file = f"{coin_folder}/varmove.py"
        loader = importlib.machinery.SourceFileLoader('varmove', varmove_file)
        varmove_module = loader.load_module()

        # Extract the variable values from the varmove module
        TradeAmount = getattr(varmove_module, "TradeAmount", None)
        TradeX = getattr(varmove_module, "TradeX", None)
        setDOWNstart = getattr(varmove_module, "setDOWNstart", None)
        StopTrades = getattr(varmove_module, "StopTrades", None)
        TakeProfitFromBUY = getattr(varmove_module, "TakeProfitFromBUY", None)
        TakeProfitFromBUYInitial = getattr(varmove_module, "TakeProfitFromBUYInitial", None)
        TakeProfitFromBUY2 = getattr(varmove_module, "TakeProfitFromBUY2", None)
        TakeProfitFromSELL = getattr(varmove_module, "TakeProfitFromSELL", None)
        TakeProfitFromSELLInitial = getattr(varmove_module, "TakeProfitFromSELLInitial", None)
        ROICloseLevel = getattr(varmove_module, "ROICloseLevel", None)
        ROICloseLevelInitial = getattr(varmove_module, "ROICloseLevelInitial", None)
        spread1 = getattr(varmove_module, "spread1", None)
        spread1Initial = getattr(varmove_module, "spread1Initial", None)
        PosNotFilledXAddLevel = getattr(varmove_module, "PosNotFilledXAddLevel", None)


        mintrade_file = f"{coin_folder}/mintrade.py"
        loader = importlib.machinery.SourceFileLoader('mintrade', mintrade_file)
        mintrade_module = loader.load_module()

        # Extract the variable values from the mintrade module
        mintrade = getattr(mintrade_module, "min_trade_qty", None)


        pricediff_file = f"{coin_folder}/pricediff.py"
        loader = importlib.machinery.SourceFileLoader('pricediff', pricediff_file)
        pricediff_module = loader.load_module()

        # Extract the variable values from the pricediff module
        pricediff = getattr(pricediff_module, "pricediff", None)


        coin_info.clear()  # Clear the coin_info list

        coin_info.append(
            {
                "Coin": str(coin),
                "TradeAmount": TradeAmount,
                "TradeX": TradeX,
                "setDOWNstart": setDOWNstart,
                "StopTrades": StopTrades,
                "TakeProfitFromBUY": TakeProfitFromBUY,
                "TakeProfitFromBUYInitial": TakeProfitFromBUYInitial,
                "TakeProfitFromBUY2": TakeProfitFromBUY2,
                "TakeProfitFromSELL": TakeProfitFromSELL,
                "TakeProfitFromSELLInitial": TakeProfitFromSELLInitial,
                "ROICloseLevel": ROICloseLevel,
                "ROICloseLevelInitial": ROICloseLevelInitial,
                "spread1": spread1,
                "spread1Initial": spread1Initial,
                "PosNotFilledXAddLevel": PosNotFilledXAddLevel,
                "pricediff": pricediff
            }
        )

        # Function to save the values when Enter key is pressed
        def save_values(event=None):
        
        
            for i, coin_data in enumerate(coin_info):
                coin_data["Coin"] = f"'{coin}'"
                coin_data["TradeAmount"] = trade_amount_entry.get()
                coin_data["TradeX"] = trade_x_entry.get()
                coin_data["setDOWNstart"] = set_down_start_entry.get()
                coin_data["StopTrades"] = stop_trades_entry.get()
                coin_data["TakeProfitFromBUY"] = take_profit_buy_entry.get()
                coin_data["TakeProfitFromBUYInitial"] = take_profit_buy_initial_entry.get()
                coin_data["TakeProfitFromBUY2"] = take_profit_buy2_entry.get()
                coin_data["TakeProfitFromSELL"] = take_profit_sell_entry.get()
                coin_data["TakeProfitFromSELLInitial"] = take_profit_sell_initial_entry.get()
                coin_data["ROICloseLevel"] = roi_close_level_entry.get()
                coin_data["ROICloseLevelInitial"] = roi_close_level_initial_entry.get()
                coin_data["spread1"] = spread1_entry.get()
                coin_data["spread1Initial"] = spread1Initial_entry.get()
                coin_data["PosNotFilledXAddLevel"] = PosNotFilledXAddLevel_entry.get()

                coin_folder = f"coins/{coin}"
                varmove_file = f"{coin_folder}/varmove.py"
                with open(varmove_file, 'w') as f:
                    for key, value in coin_info[0].items():
                        if key == "coin":
                            f.write(f"{key} = '{value}'\n")
                        else:
                            f.write(f"{key} = {value}\n")                          



        # Function to save the values when Enter key is pressed
        def save_valuesScale(event=None):
        
        
            for i, coin_data in enumerate(coin_info):
                coin_data["Coin"] = f"'{coin}'"
                coin_data["TradeAmount"] = trade_amount_scale.get()
                coin_data["TradeX"] = trade_x_scale.get()
                coin_data["setDOWNstart"] = set_down_start_scale.get()
                coin_data["StopTrades"] = stop_trades_scale.get()
                coin_data["TakeProfitFromBUY"] = take_profit_buy_scale.get()
                coin_data["TakeProfitFromBUYInitial"] = take_profit_buy_initial_scale.get()
                coin_data["TakeProfitFromBUY2"] = take_profit_buy2_scale.get()
                coin_data["TakeProfitFromSELL"] = take_profit_sell_scale.get()
                coin_data["TakeProfitFromSELLInitial"] = take_profit_sell_initial_scale.get()
                coin_data["ROICloseLevel"] = roi_close_level_scale.get()
                coin_data["ROICloseLevelInitial"] = roi_close_level_initial_scale.get()
                coin_data["spread1"] = spread1_scale.get()
                coin_data["spread1Initial"] = spread1Initial_scale.get()
                coin_data["PosNotFilledXAddLevel"] = PosNotFilledXAddLevel_scale.get()

               
                coin_folder = f"coins/{coin}"
                varmove_file = f"{coin_folder}/varmove.py"
                with open(varmove_file, 'w') as f:
                    for key, value in coin_info[0].items():
                        if key == "coin":
                            f.write(f"{key} = '{value}'\n")
                        else:
                            f.write(f"{key} = {value}\n") 
                        
                        
                        
                        

        # Function to save the values when Enter key is pressed
        def save_values_pricediff_Scale(event=None):
                    
   
            for i, coin_data in enumerate(coin_info):
                coin_data["pricediff"] = pricediff_scale.get()

               
                coin_folder = f"coins/{coin}"
                pricediff_file = f"{coin_folder}/pricediff.py"
                with open(pricediff_file, 'w') as f:
                    for key, value in coin_info[0].items():
                        if key == "pricediff":
                            f.write(f"{key} = {value}\n")
                        
                           
  
        def start_script():
            coin = coin_var.get()
            if coin:
                coin_path = get_coin_path(coin)
                os.chdir(coin_path)
                if os.path.isfile(NOW_PID_FILE):
                    os.chdir(APP_DIR)
                    print('Restarter is already running')
                else:
                    # Start the restarter script
                    start_process(RESTARTER_PID_FILE, [f'python3.8', f'restarter.py'])

                    time.sleep(2)
                    os.chdir(APP_DIR)

            else:
                return f"Coin directory {coin_path} not found"






        def start_process(pid_file, command):
            process = subprocess.Popen(command)
            with open(pid_file, 'w') as f:
                f.write(str(process.pid))
            print(f'Started process with PID {process.pid}')


        def stop_script():
            stop_process(RESTARTER_PID_FILE)
            stop_process(NOW_PID_FILE)


        def stop_process(pid_file):
            coin = coin_var.get()
            try:
                coin_path = get_coin_path(coin)
                os.chdir(coin_path)
            except FileNotFoundError:
                print(f'Directory {coin_path} not found')
                os.chdir(APP_DIR)

            try:
                with open(pid_file) as f:
                    pid = int(f.read())
                    os.kill(pid, signal.SIGTERM)
                    os.remove(pid_file)
                    print(f'Stopped process with PID {pid}')
            except FileNotFoundError:
                os.remove(pid_file)
                print(f'No such process, old pid deleted')
            except ProcessLookupError:
                os.remove(pid_file)
                print(f'Process with PID {pid} not found, old pid deleted')
            except Exception as e:
                print(f'An error occurred while stopping the process: {str(e)}')
            finally:
                os.chdir(APP_DIR)

   
   
                     

        # Display the coin information in the set coin variables window
        row = 0
        for field_name, field_value in coin_info[0].items():
            field_label = tk.Label(coin_frame, text=field_name, font=("Arial", 10, "bold"))
            field_label.grid(row=row, column=0, padx=0, pady=0, sticky="w")

            # Create entry widgets for each field

            if field_name == "TradeAmount":
                trade_amount_entry = tk.Entry(coin_frame, width=10)
                trade_amount_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
                trade_amount_entry.insert(0, field_value)
                trade_amount_entry.config(validate="key")
                trade_amount_entry.config(validatecommand=(trade_amount_entry.register(validate_float), "%P"))
                trade_amount_entry.bind("<Return>", save_values)
                row += 1
        
                trade_amount_scale = tk.Scale(
                    coin_frame,
                    from_=mintrade,
                    to=(mintrade*50) if field_name == "TradeAmount" else 25,
                    resolution = mintrade if field_name == "TradeAmount" else 1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=10,
                )
                trade_amount_scale.set(float(field_value))
                trade_amount_scale.grid(row=row, column=1, sticky="w")
                trade_amount_scale.bind("<ButtonRelease-1>", save_valuesScale)
                row += 1
                
            elif field_name == "TradeX":
               # trade_x_entry = tk.Entry(coin_frame, width=10)
               # trade_x_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # trade_x_entry.insert(0, field_value)
               # trade_x_entry.config(validate="key")
               # trade_x_entry.config(validatecommand=(trade_x_entry.register(validate_float), "%P"))
               # trade_x_entry.bind("<Return>", save_values)
               # row += 1
        
                trade_x_scale = tk.Scale(
                    coin_frame,
                    from_=1,
                    to=25,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                trade_x_scale.set(float(field_value))
                trade_x_scale.grid(row=row, column=1, sticky="w")
                trade_x_scale.bind("<ButtonRelease-1>", save_valuesScale)
            
            elif field_name == "setDOWNstart":
               # set_down_start_entry = tk.Entry(coin_frame, width=10)
               # set_down_start_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # set_down_start_entry.insert(0, field_value)
               # set_down_start_entry.config(validate="key")
               # set_down_start_entry.config(validatecommand=(set_down_start_entry.register(validate_float), "%P"))
               # set_down_start_entry.bind("<Return>", save_values)
               # row += 1
        
                set_down_start_scale = tk.Scale(
                    coin_frame,
                    from_=-4,
                    to=8,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                set_down_start_scale.set(float(field_value))
                set_down_start_scale.grid(row=row, column=1, sticky="w")
                set_down_start_scale.bind("<ButtonRelease-1>", save_valuesScale)


                
            elif field_name == "StopTrades":
              #  stop_trades_entry = tk.Entry(coin_frame, width=10)
              #  stop_trades_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
              #  stop_trades_entry.insert(0, field_value)
              #  stop_trades_entry.config(validate="key")
              #  stop_trades_entry.config(validatecommand=(stop_trades_entry.register(validate_float), "%P"))
              #  stop_trades_entry.bind("<Return>", save_values)
              #  row += 1
        
                stop_trades_scale = tk.Scale(
                    coin_frame,
                    from_=2,
                    to=12,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                stop_trades_scale.set(float(field_value))
                stop_trades_scale.grid(row=row, column=1, sticky="w")
                stop_trades_scale.bind("<ButtonRelease-1>", save_valuesScale)
                
            elif field_name == "TakeProfitFromBUY":
              #  take_profit_buy_entry = tk.Entry(coin_frame, width=10)
              #  take_profit_buy_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
              #  take_profit_buy_entry.insert(0, field_value)
              #  take_profit_buy_entry.config(validate="key")
              #  take_profit_buy_entry.config(validatecommand=(take_profit_buy_entry.register(validate_float), "%P"))
              #  take_profit_buy_entry.bind("<Return>", save_values)
              #  row += 1
        
                take_profit_buy_scale = tk.Scale(
                    coin_frame,
                    from_=6,
                    to=500,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                take_profit_buy_scale.set(float(field_value))
                take_profit_buy_scale.grid(row=row, column=1, sticky="w")
                take_profit_buy_scale.bind("<ButtonRelease-1>", save_valuesScale)
                
            elif field_name == "TakeProfitFromBUYInitial":
              #  take_profit_buy_initial_entry = tk.Entry(coin_frame, width=10)
              #  take_profit_buy_initial_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
              #  take_profit_buy_initial_entry.insert(0, field_value)
              #  take_profit_buy_initial_entry.config(validate="key")
              #  take_profit_buy_initial_entry.config(validatecommand=(take_profit_buy_initial_entry.register(validate_float), "%P"))
              #  take_profit_buy_initial_entry.bind("<Return>", save_values)
                row += 1
        
                take_profit_buy_initial_scale = tk.Scale(
                    coin_frame,
                    from_=6,
                    to=500,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                take_profit_buy_initial_scale.set(float(field_value))
                take_profit_buy_initial_scale.grid(row=row, column=1, sticky="w")
                take_profit_buy_initial_scale.bind("<ButtonRelease-1>", save_valuesScale)

            elif field_name == "TakeProfitFromBUY2":
               # take_profit_buy2_entry = tk.Entry(coin_frame, width=10)
               # take_profit_buy2_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # take_profit_buy2_entry.insert(0, field_value)
               # take_profit_buy2_entry.config(validate="key")
               # take_profit_buy2_entry.config(validatecommand=(take_profit_buy2_entry.register(validate_float), "%P"))
               # take_profit_buy2_entry.bind("<Return>", save_values)
               # row += 1
        
                take_profit_buy2_scale = tk.Scale(
                    coin_frame,
                    from_=45,
                    to=10000,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                take_profit_buy2_scale.set(float(field_value))
                take_profit_buy2_scale.grid(row=row, column=1, sticky="w")
                take_profit_buy2_scale.bind("<ButtonRelease-1>", save_valuesScale)


            elif field_name == "TakeProfitFromSELL":
              #  take_profit_sell_entry = tk.Entry(coin_frame, width=10)
              #  take_profit_sell_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
              #  take_profit_sell_entry.insert(0, field_value)
              #  take_profit_sell_entry.config(validate="key")
              #  take_profit_sell_entry.config(validatecommand=(take_profit_sell_entry.register(validate_float), "%P"))
              #  take_profit_sell_entry.bind("<Return>", save_values)
              #  row += 1
        
                take_profit_sell_scale = tk.Scale(
                    coin_frame,
                    from_=6,
                    to=500,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                take_profit_sell_scale.set(float(field_value))
                take_profit_sell_scale.grid(row=row, column=1, sticky="w")
                take_profit_sell_scale.bind("<ButtonRelease-1>", save_valuesScale)


            elif field_name == "TakeProfitFromSELLInitial":
              #  take_profit_sell_initial_entry = tk.Entry(coin_frame, width=10)
              #  take_profit_sell_initial_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
              #  take_profit_sell_initial_entry.insert(0, field_value)
              #  take_profit_sell_initial_entry.config(validate="key")
              #  take_profit_sell_initial_entry.config(validatecommand=(take_profit_sell_initial_entry.register(validate_float), "%P"))
              #  take_profit_sell_initial_entry.bind("<Return>", save_values)
              #  row += 1
        
                take_profit_sell_initial_scale = tk.Scale(
                    coin_frame,
                    from_=6,
                    to=500,
                    resolution=0.1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                take_profit_sell_initial_scale.set(float(field_value))
                take_profit_sell_initial_scale.grid(row=row, column=1, sticky="w")
                take_profit_sell_initial_scale.bind("<ButtonRelease-1>", save_valuesScale)


            elif field_name == "ROICloseLevel":
              #  roi_close_level_entry = tk.Entry(coin_frame, width=10)
              #  roi_close_level_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
              #  roi_close_level_entry.insert(0, field_value)
              #  roi_close_level_entry.config(validate="key")
              #  roi_close_level_entry.config(validatecommand=(roi_close_level_entry.register(validate_float), "%P"))
              #  roi_close_level_entry.bind("<Return>", save_values)
              #  row += 1
        
                roi_close_level_scale = tk.Scale(
                    coin_frame,
                    from_=-50,
                    to=-8,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                roi_close_level_scale.set(float(field_value))
                roi_close_level_scale.grid(row=row, column=1, sticky="w")
                roi_close_level_scale.bind("<ButtonRelease-1>", save_valuesScale)

            elif field_name == "ROICloseLevelInitial":
               # roi_close_level_initial_entry = tk.Entry(coin_frame, width=10)
               # roi_close_level_initial_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # roi_close_level_initial_entry.insert(0, field_value)
               # roi_close_level_initial_entry.config(validate="key")
               # roi_close_level_initial_entry.config(validatecommand=(roi_close_level_initial_entry.register(validate_float), "%P"))
               # roi_close_level_initial_entry.bind("<Return>", save_values)
               # row += 1
        
                roi_close_level_initial_scale = tk.Scale(
                    coin_frame,
                    from_=-50,
                    to=-8,
                    resolution=0.1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                roi_close_level_initial_scale.set(float(field_value))
                roi_close_level_initial_scale.grid(row=row, column=1, sticky="w")
                roi_close_level_initial_scale.bind("<ButtonRelease-1>", save_valuesScale)


            elif field_name == "spread1":
               # spread1_entry = tk.Entry(coin_frame, width=10)
               # spread1_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # spread1_entry.insert(0, field_value)
               # spread1_entry.config(validate="key")
               # spread1_entry.config(validatecommand=(spread1_entry.register(validate_float), "%P"))
               # spread1_entry.bind("<Return>", save_values)
               # row += 1
        
                spread1_scale = tk.Scale(
                    coin_frame,
                    from_=5,
                    to=300,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                spread1_scale.set(float(field_value))
                spread1_scale.grid(row=row, column=1, sticky="w")
                spread1_scale.bind("<ButtonRelease-1>", save_valuesScale)

            elif field_name == "spread1Initial":
               # spread1Initial_entry = tk.Entry(coin_frame, width=10)
               # spread1Initial_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # spread1Initial_entry.insert(0, field_value)
               # spread1Initial_entry.config(validate="key")
               # spread1Initial_entry.config(validatecommand=(spread1Initial_entry.register(validate_float), "%P"))
               # spread1Initial_entry.bind("<Return>", save_values)
               # row += 1
        
                spread1Initial_scale = tk.Scale(
                    coin_frame,
                    from_=5,
                    to=300,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                spread1Initial_scale.set(float(field_value))
                spread1Initial_scale.grid(row=row, column=1, sticky="w")
                spread1Initial_scale.bind("<ButtonRelease-1>", save_valuesScale)

            elif field_name == "PosNotFilledXAddLevel":
               # PosNotFilledXAddLevel_entry = tk.Entry(coin_frame, width=10)
               # PosNotFilledXAddLevel_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
               # PosNotFilledXAddLevel_entry.insert(0, field_value)
               # PosNotFilledXAddLevel_entry.config(validate="key")
               # PosNotFilledXAddLevel_entry.config(validatecommand=(PosNotFilledXAddLevel_entry.register(validate_float), "%P"))
               # PosNotFilledXAddLevel_entry.bind("<Return>", save_values)
               # row += 1
        
                PosNotFilledXAddLevel_scale = tk.Scale(
                    coin_frame,
                    from_=4,
                    to=45,
                    resolution=1,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=2,
                )
                PosNotFilledXAddLevel_scale.set(float(field_value))
                PosNotFilledXAddLevel_scale.grid(row=row, column=1, sticky="w")
                PosNotFilledXAddLevel_scale.bind("<ButtonRelease-1>", save_valuesScale)

            elif field_name == "pricediff":
        
                pricediff_scale = tk.Scale(
                    coin_frame,
                    from_=0.00,
                    to=1,
                    resolution=0.01,
                    orient=tk.HORIZONTAL,
                    length=300,
                    digits=4,
                )

                if field_value is not None and isinstance(field_value, (int, float)):
                    pricediff_scale.set(float(field_value))
                    pricediff_scale.grid(row=row, column=1, padx=0, pady=0, sticky="w")
                    pricediff_scale.bind("<ButtonRelease-1>", save_values_pricediff_Scale)   
                else:
                    pricediff_scale.set(0.22)  # Set a default value if field_value is None
                    pricediff_scale.grid(row=row, column=1, padx=0, pady=0, sticky="w")
                    pricediff_scale.bind("<ButtonRelease-1>", save_values_pricediff_Scale)               
                    row += 1 


                
            # Add other fields using the same structure if needed

        
            else:
                field_entry = tk.Entry(coin_frame, width=10)
                field_entry.grid(row=row, column=1, padx=0, pady=0, sticky="w")
                field_entry.insert(0, field_value)
                field_entry.config(validate="key")
                field_entry.config(validatecommand=(field_entry.register(validate_float), "%P"))
                field_entry.bind("<Return>", save_values)
                row += 1
            row += 1
        # Create a Save button
        save_button = tk.Button(set_coin_variables_window, text="Save", command=save_values)
        save_button.pack()

        # Add Start button
        start_button = tk.Button(set_coin_variables_window, text="Start", command=start_script)
        start_button.pack(side=tk.TOP, padx=0, pady=0)

        # Add Stop button
        stop_button = tk.Button(set_coin_variables_window, text="Stop", command=stop_script)
        stop_button.pack(side=tk.TOP, padx=0, pady=0)
        
        


    # Call the update function initially
    update_SetCoinVariables()

    # Schedule the update function every 5 seconds (5000 milliseconds)
    set_coin_variables_window.after(30000, update_SetCoinVariables)





def validate_float(value):
    if value == "":
        return True
    try:
        float_value = float(value)
        return float_value >= 0 and len(value.split(".")[-1]) <= 2
    except ValueError:
        return False



def restart_script_stop(coin):
    restart_stop_process(coin,RESTARTER_PID_FILE)
    restart_stop_process(coin,NOW_PID_FILE)
    

def restart_stop_process(coin,pid_file):
    try:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
    except FileNotFoundError:
        print(f'Directory {coin_path} not found')
        os.chdir(APP_DIR)

    try:
        with open(pid_file) as f:
            pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            os.remove(pid_file)
            print(f'Stopped process with PID {pid}')
    except FileNotFoundError:
        os.remove(pid_file)
        print(f'No such process, old pid deleted')
    except ProcessLookupError:
        os.remove(pid_file)
        print(f'Process with PID {pid} not found, old pid deleted')
    except Exception as e:
        print(f'An error occurred while stopping the process: {str(e)}')
    finally:
        os.chdir(APP_DIR)

def restart_script(coin):
    coin_path = get_coin_path(coin)
    os.chdir(coin_path)
    start_process(RESTARTER_PID_FILE, [f'python3.8', f'restarter.py'])
    time.sleep(2)

def restart_all_active_coins():
    coins_list = ['BNBUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'ARUSDT', 'MATICUSDT', 'LINKUSDT', 'DOTUSDT',
                  'IOTAUSDT', 'LTCUSDT', 'XTZUSDT', 'ADAUSDT', 'XMRUSDT', 'TRXUSDT', 'NEOUSDT', 'DASHUSDT', 'VETUSDT',
                  'ZECUSDT', 'DOGEUSDT', 'ALGOUSDT', 'WAVESUSDT', 'BATUSDT', 'ZILUSDT', 'ONTUSDT', 'FILUSDT', 'OMGUSDT',
                  'COMPUSDT', 'SNXUSDT', 'AAVEUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MKRUSDT', 'CRVUSDT', 'KSMUSDT',
                  'YFIUSDT', 'GRTUSDT', 'BALUSDT', 'MANAUSDT', 'ENJUSDT', 'SANDUSDT', '1INCHUSDT', 'BANDUSDT', 'LRCUSDT',
                  'ETHUSDT', 'BTCUSDT']


    for coin in coins_list:
        if has_pid_file(coin):
            restart_script_stop(coin)
            time.sleep(0.25)
            restart_script(coin)
            time.sleep(0.25)
            os.chdir(APP_DIR)  # Change back to the main application directory
            
            

def stop_all_active_coins():
    coins_list = ['BNBUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'ARUSDT', 'MATICUSDT', 'LINKUSDT', 'DOTUSDT',
                  'IOTAUSDT', 'LTCUSDT', 'XTZUSDT', 'ADAUSDT', 'XMRUSDT', 'TRXUSDT', 'NEOUSDT', 'DASHUSDT', 'VETUSDT',
                  'ZECUSDT', 'DOGEUSDT', 'ALGOUSDT', 'WAVESUSDT', 'BATUSDT', 'ZILUSDT', 'ONTUSDT', 'FILUSDT', 'OMGUSDT',
                  'COMPUSDT', 'SNXUSDT', 'AAVEUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MKRUSDT', 'CRVUSDT', 'KSMUSDT',
                  'YFIUSDT', 'GRTUSDT', 'BALUSDT', 'MANAUSDT', 'ENJUSDT', 'SANDUSDT', '1INCHUSDT', 'BANDUSDT', 'LRCUSDT',
                  'ETHUSDT', 'BTCUSDT']


    for coin in coins_list:
        if has_pid_file(coin):
            restart_script_stop(coin)
            time.sleep(1.25)
            os.chdir(APP_DIR)  # Change back to the main application directory
    


           
           

def buy_coin2(coin):

    coin_path = get_coin_path(coin)
    os.chdir(coin_path)
   
    trading_script = f"{coin_path}/BuyMinAmount.py"


    # Call the trading script with the buy command
    subprocess.run(["python3.8", trading_script, "buy"])
    
    
    

def sell_coin2(coin):
    coin_path = get_coin_path(coin)
    os.chdir(coin_path)
   
    trading_script2 = f"{coin_path}/SellMinAmount.py"


    # Call the trading script with the buy command
    subprocess.run(["python3.8", trading_script2, "sell"])







def start_all_minAmountBuy():
    coins_list = ['BNBUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'ARUSDT', 'MATICUSDT', 'LINKUSDT', 'DOTUSDT',
                  'IOTAUSDT', 'LTCUSDT', 'XTZUSDT', 'ADAUSDT', 'XMRUSDT', 'TRXUSDT', 'NEOUSDT', 'DASHUSDT', 'VETUSDT',
                  'ZECUSDT', 'DOGEUSDT', 'ALGOUSDT', 'WAVESUSDT', 'BATUSDT', 'ZILUSDT', 'ONTUSDT', 'FILUSDT', 'OMGUSDT',
                  'COMPUSDT', 'SNXUSDT', 'AAVEUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MKRUSDT', 'CRVUSDT', 'KSMUSDT',
                  'YFIUSDT', 'GRTUSDT', 'BALUSDT', 'MANAUSDT', 'ENJUSDT', 'SANDUSDT', '1INCHUSDT', 'BANDUSDT', 'LRCUSDT',
                  'ETHUSDT', 'BTCUSDT']



    for coin in coins_list:
        if has_pid_file(coin):
            os.chdir(APP_DIR)  # Change back to the main application directory
        else:                
            restart_script(coin)
            time.sleep(4)
            buy_coin2(coin)
            time.sleep(0.25)
            os.chdir(APP_DIR)  # Change back to the main application directory
            
            
def start_all_minAmountSell():
    coins_list = ['BNBUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'ARUSDT', 'MATICUSDT', 'LINKUSDT', 'DOTUSDT',
                  'IOTAUSDT', 'LTCUSDT', 'XTZUSDT', 'ADAUSDT', 'XMRUSDT', 'TRXUSDT', 'NEOUSDT', 'DASHUSDT', 'VETUSDT',
                  'ZECUSDT', 'DOGEUSDT', 'ALGOUSDT', 'WAVESUSDT', 'BATUSDT', 'ZILUSDT', 'ONTUSDT', 'FILUSDT', 'OMGUSDT',
                  'COMPUSDT', 'SNXUSDT', 'AAVEUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MKRUSDT', 'CRVUSDT', 'KSMUSDT',
                  'YFIUSDT', 'GRTUSDT', 'BALUSDT', 'MANAUSDT', 'ENJUSDT', 'SANDUSDT', '1INCHUSDT', 'BANDUSDT', 'LRCUSDT',
                  'ETHUSDT', 'BTCUSDT']

    
    for coin in coins_list:
        if has_pid_file(coin):
            os.chdir(APP_DIR)  # Change back to the main application directory
        else:                
            restart_script(coin)
            time.sleep(2)
            sell_coin2(coin)
            time.sleep(0.25)
            os.chdir(APP_DIR)  # Change back to the main application directory
            

    
   
def update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial):
    varmove_file = os.path.join(coin_folder, "varmove.py")

    with open(varmove_file, "r") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        if "ROICloseLevel" in line:
            line = f"ROICloseLevel = {roicloselevel}\n"
        elif "ROICloseLevelInitial" in line:
            line = f"ROICloseLevelInitial = {roicloselevelinitial}\n"
        updated_lines.append(line)

    with open(varmove_file, "w") as f:
        f.writelines(updated_lines)

def update_for_all_Active_ROE(roicloselevel, roicloselevelinitial):
    coins_list = ['BNBUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'ARUSDT', 'MATICUSDT', 'LINKUSDT', 'DOTUSDT',
                  'IOTAUSDT', 'LTCUSDT', 'XTZUSDT', 'ADAUSDT', 'XMRUSDT', 'TRXUSDT', 'NEOUSDT', 'DASHUSDT', 'VETUSDT',
                  'ZECUSDT', 'DOGEUSDT', 'ALGOUSDT', 'WAVESUSDT', 'BATUSDT', 'ZILUSDT', 'ONTUSDT', 'FILUSDT', 'OMGUSDT',
                  'COMPUSDT', 'SNXUSDT', 'AAVEUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MKRUSDT', 'CRVUSDT', 'KSMUSDT',
                  'YFIUSDT', 'GRTUSDT', 'BALUSDT', 'MANAUSDT', 'ENJUSDT', 'SANDUSDT', '1INCHUSDT', 'BANDUSDT', 'LRCUSDT',
                  'ETHUSDT', 'BTCUSDT']
                  




    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)  
    for coin in coins_list:
        if has_pid_file(coin):
            coin_folder = f"coins/{coin}"
            update_coin_variables(coin_folder, roicloselevel, roicloselevelinitial)
            time.sleep(1)    
            
            

def check_last_log_timestamp(coin):
    coin_folder = f"coins/{coin}"
    log_file = f"{coin_folder}/HODL_INFO.log"
    if not os.path.exists(log_file):
        return False  # Log file doesn't exist

    try:
        last_modified = os.path.getmtime(log_file)
        current_time = time.time()
        time_diff = current_time - last_modified

        if time_diff <= 180:  # Check if the time difference is within 1 minute
            return True  # Log file is updated within the time window

    except:
        return False  # Error occurred while checking the log file

    return False  # Log file is not updated within the time window


def check_last_log_timestamp_running_led(coin):
    coin_folder = f"coins/{coin}"
    log_file = f"{coin_folder}/HODL_INFO.log"
    if not os.path.exists(log_file):
        return False  # Log file doesn't exist

    try:
        last_modified = os.path.getmtime(log_file)
        current_time = time.time()
        time_diff = current_time - last_modified

        if time_diff <= 90:  # Check if the time difference is within 1 minute
            return True  # Log file is updated within the time window

    except:
        return False  # Error occurred while checking the log file

    return False  # Log file is not updated within the time window

    

def coin_auto_restart():
    coins_list = ['BNBUSDT', 'BCHUSDT', 'ETCUSDT', 'XRPUSDT', 'EOSUSDT', 'ARUSDT', 'MATICUSDT', 'LINKUSDT', 'DOTUSDT',
                  'IOTAUSDT', 'LTCUSDT', 'XTZUSDT', 'ADAUSDT', 'XMRUSDT', 'TRXUSDT', 'NEOUSDT', 'DASHUSDT', 'VETUSDT',
                  'ZECUSDT', 'DOGEUSDT', 'ALGOUSDT', 'WAVESUSDT', 'BATUSDT', 'ZILUSDT', 'ONTUSDT', 'FILUSDT', 'OMGUSDT',
                  'COMPUSDT', 'SNXUSDT', 'AAVEUSDT', 'SUSHIUSDT', 'UNIUSDT', 'MKRUSDT', 'CRVUSDT', 'KSMUSDT',
                  'YFIUSDT', 'GRTUSDT', 'BALUSDT', 'MANAUSDT', 'ENJUSDT', 'SANDUSDT', '1INCHUSDT', 'BANDUSDT', 'LRCUSDT',
                  'ETHUSDT', 'BTCUSDT']


    for coin in coins_list:
        if has_pid_file(coin) and not check_last_log_timestamp(coin):
            restart_script_stop(coin)
            time.sleep(0.25)
            restart_script(coin)
            time.sleep(0.25)
            os.chdir(APP_DIR)  # Change back to the main application directory
    root.after(3000, coin_auto_restart)  # Refresh every 2 seconds



def check_state_led():
    coin = coin_var.get()
    isrunning = 0  # Initialize status variable

    if has_pid_file(coin) and check_last_log_timestamp_running_led(coin):
        isrunning = 1  # Set status to 1 if the coin requires restart
        os.chdir(APP_DIR)  # Change back to the main application directory
    else:
        print(f"{coin} isnt Running!")

    # Update LED status based on isrunning
    if isrunning:
        status_led.config(bg="green")
    else:
        status_led.config(bg="red")

    root.after(5000, check_state_led)  # Refresh every 55 seconds




def update_labels():
    if not is_navigating:
        for coin, label in coin_labels.items():
            if has_pid_file(coin) and check_last_log_timestamp(coin):
                label.config(bg="green")
            else:
                label.config(bg="red")
        root.after(5000, update_labels)





def update_dropdown():
    coin_menu = coin_dropdown.nametowidget(coin_dropdown.menuname)
    for index, coin in enumerate(coins_list):
        if has_pid_file(coin) and not check_last_log_timestamp(coin):
            coin_menu.entryconfig(index, foreground="black")
        else:
            coin_menu.entryconfig(index, foreground="red" if not check_last_log_timestamp(coin) else "green")
    on_coin_selected()

    root.after(5000, update_dropdown)  # Refresh every 2 minutes



def on_coin_selected(*args):
    update_variable_values()
       
# Create the GUI
root = tk.Tk()
root.geometry("1550x1024")
root.title("Log Viewer")

# Create a main container frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create the frame for the log text boxes
log_frame = tk.Frame(main_frame)
log_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the frame for the options
options_frame = tk.Frame(log_frame)
options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# Create the frame for the options
options_frame2 = tk.Frame(log_frame)
options_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

changeside_frame = tk.Frame(log_frame)
changeside_frame.pack(side=tk.LEFT,padx=2, pady=0)

# Create the first log frames
log1_frame = Frame(log_frame)
log1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# Create the first log text box with scrollbar
log1_scrollbar = tk.Scrollbar(log1_frame)
log1_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log1_box_left = tk.Text(log1_frame, height=25, font=("Arial", 9), yscrollcommand=log1_scrollbar.set)
log1_box_left.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
log1_scrollbar.config(command=log1_box_left.yview)

# Create the second log frame
log3_frame = Frame(log_frame)
log3_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# Create the second log text box with scrollbar
log3_scrollbar = tk.Scrollbar(log3_frame)
log3_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log3_box_left = tk.Text(log3_frame, height=25, font=("Arial", 9), yscrollcommand=log3_scrollbar.set)
log3_box_left.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
log3_scrollbar.config(command=log3_box_left.yview)



from importlib import import_module  # Importing the import_module function
import os
from tkcalendar import Calendar

# Flag to control plot visibility
plot_visible = False

# Create a frame to hold the plot
plot_frame = Frame(log_frame)
plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)



# Global variables to store the selected dates
start_date = None
end_date = None

# Function to open a new window for selecting the date range
def open_date_selection_window():
    def save_dates_and_close():
        global start_date, end_date
        start_date = cal_start.selection_get()
        end_date = cal_end.selection_get()
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        print(f"Selected start date: {start_datetime}")
        print(f"Selected end date: {end_datetime}")
        date_selection_window.destroy()

    date_selection_window = tk.Toplevel(root)
    date_selection_window.title("Select Date Range")

    cal_frame = Frame(date_selection_window)
    cal_frame.pack(padx=10, pady=10)

    cal_start_label = tk.Label(cal_frame, text="Start Date:")
    cal_start_label.pack(side=tk.LEFT, padx=5)

    global cal_start
    cal_start = Calendar(cal_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_start.pack(side=tk.LEFT, padx=5)

    cal_end_label = tk.Label(cal_frame, text="End Date:")
    cal_end_label.pack(side=tk.LEFT, padx=5)

    global cal_end
    cal_end = Calendar(cal_frame, selectmode='day', date_pattern='yyyy-mm-dd')
    cal_end.pack(side=tk.LEFT, padx=5)

    button_frame = Frame(date_selection_window)
    button_frame.pack(pady=10)

    confirm_button = ttk.Button(button_frame, text="Confirm", command=save_dates_and_close)
    confirm_button.pack(side=tk.LEFT, padx=5)

    cancel_button = ttk.Button(button_frame, text="Cancel", command=date_selection_window.destroy)
    cancel_button.pack(side=tk.LEFT, padx=5)

def call_analytics_script():
    global start_date, end_date
    if not start_date or not end_date:
        messagebox.showwarning("Date Range Not Selected", "Please select a date range first.")
        return

    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    log_file_path = os.path.join(coin_folder, 'HODL_TRADES.log')
    varmove_file_path = os.path.join(coin_folder, 'varmove.py')

    # Read the Coin variable from varmove.py
    try:
        with open(varmove_file_path, 'r') as file:
            content = file.read()
            match = re.search(r"Coin\s*=\s*['\"](.+?)['\"]", content)
            if match:
                coin_name = match.group(1)
            else:
                print(f"Coin variable not found in '{varmove_file_path}'.")
                return
    except FileNotFoundError:
        print(f"varmove.py file '{varmove_file_path}' not found.")
        return

    try:
        with open(log_file_path, 'r') as file:
            all_log_entries = file.readlines()
    except FileNotFoundError:
        print(f"Log file '{log_file_path}' not found.")
        return

    print("Current working directory:", os.getcwd())
    module_path = f"coins.{coin}.analytics2"
    print("Trying to import from:", module_path)

    try:
        module = import_module(module_path)
        AnalyticsCalculator = module.AnalyticsCalculator
    except ModuleNotFoundError:
        print(f"Module '{module_path}' not found.")
        return

    try:
        calculator = AnalyticsCalculator(all_log_entries)
    except Exception as e:
        print(f"Failed to create AnalyticsCalculator instance: {e}")
        return

    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    calculator.calculate_and_plot_pnl(plot_frame, start_datetime, end_datetime, coin_name)

def hide_plot():
    global plot_visible
    plot_visible = False
    for widget in plot_frame.winfo_children():
        widget.destroy()
    plot_frame.pack_forget()

def toggle_plot():
    global plot_visible
    if plot_visible:
        hide_plot()
    else:
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        call_analytics_script()
        plot_visible = True



def reolad_toggle_plot():
    global plot_visible
    if plot_visible:
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        call_analytics_script()
        plot_visible = True





# Create a button to call the analytics script and display plot
#call_analytics_button = ttk.Button(root, text="Call Analytics Script", command=toggle_plot)
#call_analytics_button.pack(side=tk.TOP, padx=5, pady=5)

# Create a frame to hold the calendars and button
#control_frame = Frame(root)
#control_frame.pack(side=tk.TOP, padx=5, pady=5)

# Create a button to open the date selection window
# date_selection_button = ttk.Button(control_frame, text="Select Date Range", command=open_date_selection_window)
# date_selection_button.pack(side=tk.LEFT, padx=5, pady=5)






# Define a variable to keep track of the current coin index
current_coin_index = 0


# Function to handle the "Next" button click
def next_coin():
    if len(coins_list) == 0:
        print("No coins available")
        return

    def find_next_coin():
        global current_coin_index
        index = current_coin_index
        while True:
            index = (index + 1) % len(coins_list)
            coin = coins_list[index]
            if check_last_log_timestamp(coin):
                current_coin_index = index
                coin_var.set(coin)
                check_state_led()
                #getAccountBalance()
                #update_getAccountBalance()
                break

    threading.Thread(target=find_next_coin).start()

# Function to handle the "Previous" button click
def previous_coin():
    if len(coins_list) == 0:
        print("No coins available")
        return

    def find_previous_coin():
        global current_coin_index
        index = current_coin_index
        while True:
            index = (index - 1) % len(coins_list)
            coin = coins_list[index]
            if check_last_log_timestamp(coin):
                current_coin_index = index
                coin_var.set(coin)
                check_state_led()
                #getAccountBalance()
                #update_getAccountBalance()
                break

    threading.Thread(target=find_previous_coin).start()


# Function to update trade status
def update_trade_status():

    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    log1_path = f"{coin_folder}/HODL_INFO.log"
    try:
        with open(log1_path, "r") as f:
            log1_data = f.readlines()
            latest_roe = extract_latest_roe(log1_data)
            roe_var.set(latest_roe)
             # display_trade_status(float(latest_roe))  # Convert to float before passing
    except FileNotFoundError:
        roe_var.set("N/A")
         # display_trade_status(0)  # Pass 0 as default ROE
    root.after(6000, update_trade_status)  # Refresh every 2 seconds



def display_trade_status(roe):
    text_color = "#000000"  # Default text color
    if roe >= 0 and roe < 30 :
            color = "#00ffff"
            text_color = "#000000"  
    if roe >= 30 and roe < 50 :
            color = "#00ffbf"
            text_color = "#000000"  
    if roe >= 50 and roe < 90 :
            color = "#00ff7f"
            text_color = "#FFFFFF"  
    if roe >= 90 and roe < 50000 :
            color = "#00b30e"
            text_color = "#000000"   
    if roe < 0 and roe > -30 :
            color = "#ffe7ed"
            text_color = "#000000"  
    if roe <= -30 and roe > -50 :
            color = "#ff677f"
            text_color = "#000000"  
    if roe <= -50 and roe > -90 :
            color = "#ff3454"
            text_color = "#000000"  
    if roe <= -90 and roe > -5000 :
            color = "#e70024"
            text_color = "#000000"  

    # Update the label with the trade status and color
    status_label.config(text=f"Trade Status: {roe}%", bg=color, fg=text_color, font=("Arial", 16))


getAccount_PID_FILE = 'getAccount_PID_FILE.pid'

def getAccountBalance():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
        # Start the restarter script
        start_process(getAccount_PID_FILE, [f'python3.8', f'accountbalance.py'])
        time.sleep(1)
        os.chdir(APP_DIR)   


# Function to extract the latest balance from log data
def extract_lastest_balance(log1_data):
    for line in log1_data:
        if line.startswith("latest_balance"):
            parts = line.split("=")
            if len(parts) == 2:
                return parts[1].strip()

    return None


# Function to update trade status
def update_getAccountBalance():



    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    log1_path = f"{coin_folder}/FuturesBalanceVars.log"
    try:
        with open(log1_path, "r") as f:
            log1_data = f.readlines()
            lastest_balance = extract_lastest_balance(log1_data)
            balance_var.set(lastest_balance)
            lastest_balance_status(float(lastest_balance))  # Convert to float before passing
    except FileNotFoundError:
        balance_var.set("N/A")
        lastest_balance_status(0)  # Pass 0 as default lastest_balance


def lastest_balance_status(balance):
    text_color = "#000000"  # Default text color
    # Update the label with the trade status and color
    balancestatus_label.config(text=f"M-Futures Account Balance: {balance}USDT", fg=text_color, font=("Arial", 16))





def run_analytics():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
        subprocess.Popen(["python3.8", "analytics.py"])
        time.sleep(1)
        os.chdir(APP_DIR)


# Create a label for trade status
#status_label = tk.Label(root, text="Trade Status: N/A", font=("Arial", 16, "bold"))
#status_label.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)




# Create a label for ACCOUNT BALANCE
#balancestatus_label = tk.Label(root, text="M-Futures Account Balance: N/A", font=("Arial", 16, "bold"))
#balancestatus_label.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)







coin_frame = tk.Frame(root)
coin_frame.pack(side=tk.LEFT, padx=2, pady=2)


# Create dropdown list for coins
coins_str = """BNBUSDT BCHUSDT ETCUSDT XRPUSDT EOSUSDT ARUSDT MATICUSDT LINKUSDT DOTUSDT IOTAUSDT LTCUSDT XTZUSDT ADAUSDT XMRUSDT TRXUSDT NEOUSDT DASHUSDT VETUSDT ZECUSDT DOGEUSDT ALGOUSDT WAVESUSDT BATUSDT ZILUSDT ONTUSDT FILUSDT OMGUSDT COMPUSDT SNXUSDT AAVEUSDT SUSHIUSDT UNIUSDT MKRUSDT CRVUSDT KSMUSDT YFIUSDT GRTUSDT BALUSDT MANAUSDT ENJUSDT SANDUSDT 1INCHUSDT BANDUSDT LRCUSDT ETHUSDT BTCUSDT"""
coins_list = sorted(coins_str.split())


default_coin = coins_list[0]

coin_var = tk.StringVar(value=default_coin)
coin_var.trace("w", on_coin_selected)
coin_dropdown = tk.OptionMenu(coin_frame, coin_var, *coins_list)
coin_dropdown.pack(anchor=tk.W, padx=2, pady=2)

# Create "Next" and "Previous" buttons, and Close button
next_button = tk.Button(coin_frame, text="Next", command=next_coin, width=70, height=1)
next_button.pack(anchor=tk.W, padx=2, pady=2)

previous_button = tk.Button(coin_frame, text="Previous", command=previous_coin, width=70, height=1)
previous_button.pack(anchor=tk.W, padx=2, pady=2)



status_label = tk.Label(coin_frame, text="Status:")
status_label.pack()

# Create status LED label
status_led = tk.Label(coin_frame, width=70, height=1)
status_led.pack()


# Create frame for labels
label_frame = tk.Frame(coin_frame)
label_frame.pack()

# Create status LED labels
coin_labels = {}
for i, coin in enumerate(coins_list):
    label_name = tk.Label(label_frame, text=coin, width=12, bg="lightgrey", font=("Arial", 7))
    label_name.grid(row=i // 6, column=i % 6 * 2, padx=0 , pady=0, sticky="n")
    label_status = tk.Label(label_frame, width=2, bg="red", relief="solid")
    label_status.grid(row=i // 6, column=i % 6 * 2 + 1, padx=0, pady=0, sticky="n")
    coin_labels[coin] = label_status


Buy_Initiate_with_Mintrade_button = None  # Define the button as a global variable

def on_coin_selected(*args):
    selected_coin = coin_var.get()
    if Buy_Initiate_with_Mintrade_button:  # Check if the button is initialized
        Buy_Initiate_with_Mintrade_button.config(text="Start " + selected_coin + " with minTrade Amount BUY")

# Rest of your code...

# Create "Start" button
Buy_Initiate_with_Mintrade_button = tk.Button(coin_frame, text="Start " + default_coin + " with minTrade Amount BUY", command=initate_BUY_mintrade, width=70, height=1)
Buy_Initiate_with_Mintrade_button.pack(anchor=tk.W, padx=2, pady=2)

# Bind the coin selection event
coin_var.trace("w", on_coin_selected)



# Add Start button
start_button = tk.Button(coin_frame, text="Start", command=start_script, width=70, height=1)
start_button.pack(anchor=tk.W, padx=1, pady=1)

# Add Stop button
stop_button = tk.Button(coin_frame, text="Stop", command=stop_script, width=70, height=1)
stop_button.pack(anchor=tk.W, padx=1, pady=1)


# Create "Trade Overview" button
trade_overview_button = tk.Button(coin_frame, text="Trade Overview", command=open_trade_overview_window, width=70, height=1)
trade_overview_button.pack(anchor=tk.W, padx=1, pady=1)

# Create the "Analytics" button
trade_overview_button = tk.Button(coin_frame, text="Analytics", command=run_analytics, width=70, height=1)
trade_overview_button.pack(anchor=tk.W, padx=1, pady=1)

# Add a button for restarting all active coins
restart_button = tk.Button(coin_frame, text="Restart All Active Coins", command=restart_all_active_coins, width=70, height=1)
restart_button.pack(anchor=tk.W, padx=1, pady=1)

# Add a button for stopping all active coins
stop_all_button = tk.Button(coin_frame, text="Stop All Active Coins", command=stop_all_active_coins, width=70, height=1)
stop_all_button.pack(anchor=tk.W, padx=1, pady=1)

# Add a button for stopping all active coins
start_all_minAmountBuy_button = tk.Button(coin_frame, text="Start all Coin with minTrade Amount BUY", width=70, height=1)
start_all_minAmountBuy_button.pack(anchor=tk.W, padx=1, pady=1)

# Add a button for stopping all active coins
start_all_minAmountSell_button = tk.Button(coin_frame, text="Start all Coin with minTrade Amount SELL", width=70, height=1)
start_all_minAmountSell_button.pack(anchor=tk.W, padx=1, pady=1)






# Call the function to start updating the dropdown menu state
update_dropdown()





# Create the frame for displaying and modifying variables
var_frame = Frame(root)
var_frame.pack(side=tk.LEFT, padx=2, pady=0)

# Define the StringVar variables
roe_var = StringVar()
balance_var = StringVar()
trade_amount_var = StringVar()
pos_size_var = StringVar()
roiclose_level_var = StringVar()
pos_size_test_var = StringVar()
roiclose_level_sell_var = StringVar()
takeprofit_level_buy_var = StringVar()
takeprofit_level_sell_var = StringVar()

# Create a list of labels and value labels
labels = [
    ("ROE:", roe_var),
    ("Trade Amount:", trade_amount_var),
    ("Pos Size:", pos_size_var),
    ("ROICloseLevel:", roiclose_level_var),
    ("PosSizetest:", pos_size_test_var),
    ("ROICloseLevel Sell:", roiclose_level_sell_var),
    ("TakeprofitLevel Buy:", takeprofit_level_buy_var),
    ("TakeprofitLevel Sell:", takeprofit_level_sell_var)
]

# Create the labels and value labels in a grid layout
for i, (label_text, var) in enumerate(labels):
    label = tk.Label(var_frame, text=label_text, font=("Arial", 10, "bold"))
    label.grid(row=i, column=0, sticky="nw", padx=2, pady=0)

    value_label = tk.Label(var_frame, textvariable=var, font=("Arial", 10, "bold"))
    value_label.grid(row=i, column=1, sticky="nw", padx=2, pady=0)


# Create the labels and entry fields and place them in the top left frame
for i, var_label in enumerate(var_labels):
    label = tk.Label(var_frame, text=var_label)
    label.grid(row=i, column=3, sticky="nw")

    entry = tk.Entry(var_frame)
    entry.grid(row=i, column=4)

    var_entries.append(entry)


# Create the save button and place it in the top left frame
start_writing_variables = tk.Button(var_frame, text="Start Writing Variables", command=start_writing_variables)
start_writing_variables.grid(row=len(var_labels), column=0, columnspan=2, pady=(10, 0))




    
    





def update_pricediff(event=None):
    pricediff_var.set(pricediff_entry.get())
    save_instructions()





def update_nextamount(event=None):
    nextamount_var.set(nextamount_entry.get())
    save_instructions()
def update_timeframe(event=None):
    timeframe_var.set(timeframe_entry.get())
    save_instructions()
def update_max_switches(event=None):
    max_switches_var.set(max_switches_entry.get())
    save_instructions()
def update_RoiCloseAdd(event=None):
    RoiCloseAdd_var.set(RoiCloseAdd_entry.get())
    save_instructions()
def update_spreadAdd(event=None):
    spreadAdd_var.set(spreadAdd_entry.get())
    save_instructions()
def update_HRoeInit(event=None):
    HRoeInit_var.set(HRoeInit_entry.get())
    save_instructions()
def update_HRoeAddDiff(event=None):
    HRoeAddDiff_var.set(HRoeAddDiff_entry.get())
    save_instructions()
def update_HRoeDiff(event=None):
    HRoeDiff_var.set(HRoeDiff_entry.get())
    save_instructions()
def update_TriggerPoint(event=None):
    TriggerPoint_var.set(TriggerPoint_entry.get())
    save_instructions()









def save_instructions():
    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    instructpath = f"{coin_folder}/instrct.py"
    with open(instructpath, "w") as f:
        f.write(f"changeside={changeside_var.get()}\n")
        f.write(f"nextamount={nextamount_var.get()}\n")
        f.write(f"timeframe={timeframe_var.get()}\n")
        f.write(f"max_switches={max_switches_var.get()}\n")
        f.write(f"RoiCloseAdd={RoiCloseAdd_var.get()}\n")
        f.write(f"spreadAdd={spreadAdd_var.get()}\n")
        f.write(f"HRoeInit={HRoeInit_var.get()}\n")
        f.write(f"HRoeAddDiff={HRoeAddDiff_var.get()}\n")
        f.write(f"HRoeDiff={HRoeDiff_var.get()}\n")
        f.write(f"TriggerPoint={TriggerPoint_var.get()}\n")




changeside_var = tk.IntVar()
nextamount_var = tk.DoubleVar()
timeframe_var = tk.DoubleVar()
max_switches_var = tk.DoubleVar()
RoiCloseAdd_var = tk.DoubleVar()
spreadAdd_var = tk.DoubleVar()
HRoeInit_var = tk.DoubleVar()
HRoeAddDiff_var = tk.DoubleVar()
HRoeDiff_var = tk.DoubleVar()
TriggerPoint_var = tk.DoubleVar()


changeside_label = tk.Label(changeside_frame, text=f"Change Side Flag: {changeside_var.get()}")
changeside_label.pack(side=tk.TOP, padx=2, pady=0)

changeside_true_button = tk.Button(changeside_frame, text="True", command=lambda: set_changeside(1))
changeside_true_button.pack(side=tk.TOP, padx=2, pady=0)

changeside_false_button = tk.Button(changeside_frame, text="False", command=lambda: set_changeside(0))
changeside_false_button.pack(side=tk.TOP, padx=2, pady=0)


nextamount_frame = tk.Frame(changeside_frame)
nextamount_frame.pack(side=tk.TOP,padx=2, pady=0)

nextamount_label = tk.Label(nextamount_frame, text=f"Next Amount: {nextamount_var.get()}")
nextamount_label.pack(side=tk.TOP, padx=2, pady=0)

nextamount_entry = tk.Entry(nextamount_frame, textvariable=nextamount_var)
nextamount_entry.pack(side=tk.TOP, padx=2, pady=0)
nextamount_entry.bind("<FocusOut>", update_nextamount)


timeframe_frame = tk.Frame(changeside_frame)
timeframe_frame.pack(side=tk.TOP,padx=2, pady=0)

timeframe_label = tk.Label(timeframe_frame, text=f"timeframe: {timeframe_var.get()}")
timeframe_label.pack(side=tk.TOP, padx=2, pady=0)

timeframe_entry = tk.Entry(timeframe_frame, textvariable=timeframe_var)
timeframe_entry.pack(side=tk.TOP, padx=2, pady=0)
timeframe_entry.bind("<FocusOut>", update_timeframe)


max_switches_frame = tk.Frame(changeside_frame)
max_switches_frame.pack(side=tk.TOP,padx=2, pady=0)

max_switches_label = tk.Label(max_switches_frame, text=f"max_switches: {max_switches_var.get()}")
max_switches_label.pack(side=tk.TOP, padx=2, pady=0)

max_switches_entry = tk.Entry(max_switches_frame, textvariable=max_switches_var)
max_switches_entry.pack(side=tk.TOP, padx=2, pady=0)
max_switches_entry.bind("<FocusOut>", update_max_switches)


RoiCloseAdd_frame = tk.Frame(changeside_frame)
RoiCloseAdd_frame.pack(side=tk.TOP,padx=2, pady=0)

RoiCloseAdd_label = tk.Label(RoiCloseAdd_frame, text=f"RoiCloseAdd: {RoiCloseAdd_var.get()}")
RoiCloseAdd_label.pack(side=tk.TOP, padx=2, pady=0)

RoiCloseAdd_entry = tk.Entry(RoiCloseAdd_frame, textvariable=RoiCloseAdd_var)
RoiCloseAdd_entry.pack(side=tk.TOP, padx=2, pady=0)
RoiCloseAdd_entry.bind("<FocusOut>", update_RoiCloseAdd)


spreadAdd_frame = tk.Frame(changeside_frame)
spreadAdd_frame.pack(side=tk.TOP,padx=2, pady=0)

spreadAdd_label = tk.Label(spreadAdd_frame, text=f"spreadAdd: {spreadAdd_var.get()}")
spreadAdd_label.pack(side=tk.TOP, padx=2, pady=0)

spreadAdd_entry = tk.Entry(spreadAdd_frame, textvariable=spreadAdd_var)
spreadAdd_entry.pack(side=tk.TOP, padx=2, pady=0)
spreadAdd_entry.bind("<FocusOut>", update_spreadAdd)


HRoeInit_frame = tk.Frame(changeside_frame)
HRoeInit_frame.pack(side=tk.TOP,padx=2, pady=0)

HRoeInit_label = tk.Label(HRoeInit_frame, text=f"HRoeInit: {HRoeInit_var.get()}")
HRoeInit_label.pack(side=tk.TOP, padx=2, pady=0)

HRoeInit_entry = tk.Entry(HRoeInit_frame, textvariable=HRoeInit_var)
HRoeInit_entry.pack(side=tk.TOP, padx=2, pady=0)
HRoeInit_entry.bind("<FocusOut>", update_HRoeInit)


HRoeAddDiff_frame = tk.Frame(changeside_frame)
HRoeAddDiff_frame.pack(side=tk.TOP,padx=2, pady=0)

HRoeAddDiff_label = tk.Label(HRoeAddDiff_frame, text=f"HRoeAddDiff: {HRoeAddDiff_var.get()}")
HRoeAddDiff_label.pack(side=tk.TOP, padx=2, pady=0)

HRoeAddDiff_entry = tk.Entry(HRoeAddDiff_frame, textvariable=HRoeAddDiff_var)
HRoeAddDiff_entry.pack(side=tk.TOP, padx=2, pady=0)
HRoeAddDiff_entry.bind("<FocusOut>", update_HRoeAddDiff)


HRoeDiff_frame = tk.Frame(changeside_frame)
HRoeDiff_frame.pack(side=tk.TOP,padx=2, pady=0)

HRoeDiff_label = tk.Label(HRoeDiff_frame, text=f"HRoeDiff: {HRoeDiff_var.get()}")
HRoeDiff_label.pack(side=tk.TOP, padx=2, pady=0)

HRoeDiff_entry = tk.Entry(HRoeDiff_frame, textvariable=HRoeDiff_var)
HRoeDiff_entry.pack(side=tk.TOP, padx=2, pady=0)
HRoeDiff_entry.bind("<FocusOut>", update_HRoeDiff)


TriggerPoint_frame = tk.Frame(changeside_frame)
TriggerPoint_frame.pack(side=tk.TOP,padx=2, pady=0)

TriggerPoint_label = tk.Label(TriggerPoint_frame, text=f"TriggerPoint: {TriggerPoint_var.get()}")
TriggerPoint_label.pack(side=tk.TOP, padx=2, pady=0)

TriggerPoint_entry = tk.Entry(TriggerPoint_frame, textvariable=TriggerPoint_var)
TriggerPoint_entry.pack(side=tk.TOP, padx=2, pady=0)

# Bind FocusOut event to update nextamount
TriggerPoint_entry.bind("<FocusOut>", update_TriggerPoint)






# Save Instructions Button
save_button = tk.Button(changeside_frame, text="Save Instructions", command=save_instructions)
save_button.pack(pady=10)






STATE_FILE = "optionsstate.py"


# Function to save the current state to a file
def save_state():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
        with open(STATE_FILE, 'w') as f:
            f.write(f"option1 = {option1.get()}\n")
            f.write(f"option2 = {option2.get()}\n")
            f.write(f"option3 = {option3.get()}\n")
            f.write(f"option4 = {option4.get()}\n")
            f.write(f"option5 = {option5.get()}\n")
            f.write(f"option6 = {option6.get()}\n")
            f.write(f"option7 = {option7.get()}\n")
            f.write(f"option8 = {option8.get()}\n")
            f.write(f"option9 = {option9.get()}\n")
            f.write(f"option10 = {option10.get()}\n")
            f.write(f"option11 = {option11.get()}\n")
        os.chdir(APP_DIR)

def load_state():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        os.chdir(coin_path)
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                code = f.read()
                local_vars = {}
                exec(code, {}, local_vars)
                option1.set(local_vars.get('option1', False))
                option2.set(local_vars.get('option2', False))
                option3.set(local_vars.get('option3', False))
                option4.set(local_vars.get('option4', False))
                option5.set(local_vars.get('option5', False))
                option6.set(local_vars.get('option6', False))
                option7.set(local_vars.get('option7', False))
                option8.set(local_vars.get('option8', False))
                option9.set(local_vars.get('option9', False))
                option10.set(local_vars.get('option10', False))
                option11.set(local_vars.get('option11', False))                
        os.chdir(APP_DIR)


# Function to display the state of all options
def display_selected():
    state = f"""
    Option 1: {'On' if option1.get() else 'Off'}
    Option 2: {'On' if option2.get() else 'Off'}
    Option 3: {'On' if option3.get() else 'Off'}
    Option 4: {'On' if option4.get() else 'Off'}
    Option 5: {'On' if option5.get() else 'Off'}
    Option 6: {'On' if option6.get() else 'Off'}
    Option 7: {'On' if option7.get() else 'Off'}
    Option 8: {'On' if option8.get() else 'Off'}
    Option 9: {'On' if option9.get() else 'Off'}
    Option 10: {'On' if option10.get() else 'Off'}
    Option 11: {'On' if option11.get() else 'Off'}
    """
    save_state()

# Function to update check button states based on loaded variables
def update_check_buttons():
    option1.set(globals().get('option1', False) if isinstance(globals().get('option1'), bool) else False)
    option2.set(globals().get('option2', False) if isinstance(globals().get('option2'), bool) else False)
    option3.set(globals().get('option3', False) if isinstance(globals().get('option3'), bool) else False)
    option4.set(globals().get('option4', False) if isinstance(globals().get('option4'), bool) else False)
    option5.set(globals().get('option5', False) if isinstance(globals().get('option5'), bool) else False)
    option6.set(globals().get('option6', False) if isinstance(globals().get('option6'), bool) else False)
    option7.set(globals().get('option7', False) if isinstance(globals().get('option7'), bool) else False)
    option8.set(globals().get('option8', False) if isinstance(globals().get('option8'), bool) else False)
    option9.set(globals().get('option9', False) if isinstance(globals().get('option9'), bool) else False)
    option10.set(globals().get('option10', False) if isinstance(globals().get('option10'), bool) else False)
    option11.set(globals().get('option11', False) if isinstance(globals().get('option11'), bool) else False)


# Initialize variables to hold the state of each check button
option1 = tk.BooleanVar(value=False)
option2 = tk.BooleanVar(value=False)
option3 = tk.BooleanVar(value=False)
option4 = tk.BooleanVar(value=False)
option5 = tk.BooleanVar(value=False)
option6 = tk.BooleanVar(value=False)
option7 = tk.BooleanVar(value=False)
option8 = tk.BooleanVar(value=False)
option9 = tk.BooleanVar(value=False)
option10 = tk.BooleanVar(value=False)
option11 = tk.BooleanVar(value=False)


def SetStopMarket():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        original_dir = os.getcwd()  # Save the current directory
        if os.path.exists(coin_path):  # Check if the coin path exists
            os.chdir(coin_path)  # Change to the coin directory

        try:
            TRADING_script = "stop.py"

            # Check if the stop.py script exists in the coin directory
            if os.path.exists(TRADING_script):
                # Run the subprocess
                subprocess.run(["python3.8", TRADING_script, "stopmarket"], check=True)
            else:
                print(f"{TRADING_script} does not exist in {coin_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            os.chdir(APP_DIR)



def DelStopMarket():
    coin = coin_var.get()
    if coin:
        coin_path = get_coin_path(coin)
        original_dir = os.getcwd()  # Save the current directory
        if os.path.exists(coin_path):  # Check if the coin path exists
            os.chdir(coin_path)  # Change to the coin directory

        try:
            TRADING_script = "delstop.py"

            # Check if the stop.py script exists in the coin directory
            if os.path.exists(TRADING_script):
                # Run the subprocess
                subprocess.run(["python3.8", TRADING_script, "delstopmarket"], check=True)
            else:
                print(f"{TRADING_script} does not exist in {coin_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            os.chdir(APP_DIR)




# Load the initial state
load_state()

# Update check button states based on loaded variables
update_check_buttons()

close_button = tk.Button(options_frame, text="CloseGUI", command=root.quit)
close_button.pack(anchor=tk.W, padx=1, pady=1)


# Create a label to display the state of each option
selected_label = ttk.Label(options_frame, text="Selected modes for that M-FUTURES Coin:")
selected_label.pack(anchor='w', padx=10, pady=10)

# Create check buttons in the options frame
check_button1 = ttk.Checkbutton(options_frame, text="AutoBuyMoreGrower", variable=option1, command=display_selected)
check_button1.pack(anchor='w', padx=10, pady=5)

check_button2 = ttk.Checkbutton(options_frame, text="AutoSellMoreGrower", variable=option2, command=display_selected)
check_button2.pack(anchor='w', padx=10, pady=5)

check_button3 = ttk.Checkbutton(options_frame, text="Enable BUY", variable=option3, command=display_selected)
check_button3.pack(anchor='w', padx=10, pady=5)

check_button4 = ttk.Checkbutton(options_frame, text="Enable SELL", variable=option4, command=display_selected)
check_button4.pack(anchor='w', padx=10, pady=5)

check_button5 = ttk.Checkbutton(options_frame, text="Invert Trade if ROICloseLevel is reached (normal True)", variable=option5, command=display_selected)
check_button5.pack(anchor='w', padx=10, pady=5)

check_button6 = ttk.Checkbutton(options_frame, text="Take Profit", variable=option6, command=display_selected)
check_button6.pack(anchor='w', padx=10, pady=5)

check_button7 = ttk.Checkbutton(options_frame, text="SmallHoldMUCHROI", variable=option7, command=display_selected)
check_button7.pack(anchor='w', padx=10, pady=5)

check_button8 = ttk.Checkbutton(options_frame, text="onlyGoToMin", variable=option8, command=display_selected)
check_button8.pack(anchor='w', padx=10, pady=5)

check_button9 = ttk.Checkbutton(options_frame, text="smallholdsmallroiAddXEnable", variable=option9, command=display_selected)
check_button9.pack(anchor='w', padx=10, pady=5)

check_button10 = ttk.Checkbutton(options_frame, text="setStopMarketHardSwich", variable=option10, command=display_selected)
check_button10.pack(anchor='w', padx=10, pady=5)

check_button11 = ttk.Checkbutton(options_frame, text="cleanLogsforCoin", variable=option11, command=display_selected)
check_button11.pack(anchor='w', padx=10, pady=5)

# Your STOPMARKET button setup
SetStopMarket_button = tk.Button(options_frame, text="SetStopMarket", command=SetStopMarket)
SetStopMarket_button.pack(anchor='w', padx=10, pady=5)

# Your STOPMARKET button setup
DelStopMarket_button = tk.Button(options_frame, text="DelStopMarket", command=DelStopMarket)
DelStopMarket_button.pack(anchor='w', padx=10, pady=5)



pricediff_var = tk.DoubleVar()


pricediff_frame = tk.Frame(options_frame)
pricediff_frame.pack(anchor='w', padx=10, pady=5)

pricediff_label = tk.Label(options_frame, text=f"Pricediff for StopM in %: {pricediff_var.get()}")
pricediff_label.pack(anchor='w', padx=10, pady=5)







def display_latest_restarts():
    # Catch coin
    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    
    # Change to the coin's directory
    os.chdir(coin_folder)
    
    # Initialize variables
    restart_lines = []
    
    try:
        # Read the logfile and find the latest restart events
        with open('restartlog.txt', 'r') as logfile:
            lines = logfile.readlines()
            for line in reversed(lines):
                if "Process not running, restarting" in line:
                    restart_lines.append(line.strip())
                    if len(restart_lines) == 5:
                        break
    except FileNotFoundError:
        restart_lines = None
    
    # Display the latest restart times in the Tkinter frame
    for widget in lastrestart_frame.winfo_children():
        widget.destroy()
    
    if restart_lines:
        for restart_line in restart_lines:
            restart_label = tk.Label(lastrestart_frame, text=restart_line)
            restart_label.pack()
    else:
        no_restart_label = tk.Label(lastrestart_frame, text="No restartlog.txt file found.")
        no_restart_label.pack()
    
    os.chdir(current_dir)  # Restore the original working directory



from tkinter import filedialog

def open_varmove_file():
    # Catch coin
    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    
    # Path to the varmove.py file
    varmove_file_path = os.path.join(coin_folder, 'varmove.py')
    
    # Open a new Tkinter window for editing the file
    editor_window = Toplevel(root)
    editor_window.title(f"Editing {varmove_file_path}")
    
    # Set the size of the editor window
    editor_window.geometry("600x400")
    
    # Get the main window's position and size
    root.update_idletasks()
    main_window_width = root.winfo_width()
    main_window_height = root.winfo_height()
    main_window_x = root.winfo_x()
    main_window_y = root.winfo_y()
    
    # Calculate the position for the editor window to center it on the main window's screen
    width = 600
    height = 400
    x = main_window_x + (main_window_width // 2) - (width // 2)
    y = main_window_y + (main_window_height // 2) - (height // 2)
    editor_window.geometry(f'{width}x{height}+{x}+{y}')
    
    text_widget = Text(editor_window, wrap='word')
    text_widget.pack(expand=1, fill='both')
    
    scrollbar = Scrollbar(editor_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    
    # Load the content of the file into the Text widget
    with open(varmove_file_path, 'r') as file:
        text_widget.insert('1.0', file.read())
    
    def save_and_close():
        with open(varmove_file_path, 'w') as file:
            file.write(text_widget.get('1.0', 'end-1c'))
        editor_window.destroy()
    
    def save_as():
        save_as_path = filedialog.asksaveasfilename(initialdir=os.path.join(coin_folder, 'examples'),
                                                    defaultextension=".py",
                                                    filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if save_as_path:
            with open(save_as_path, 'w') as file:
                file.write(text_widget.get('1.0', 'end-1c'))
    
    # Add a "Close and Save" button
    save_button = Button(editor_window, text="Close and Save", command=save_and_close)
    save_button.pack(side=LEFT, padx=10, pady=5)

    # Add a "Save As" button
    save_as_button = Button(editor_window, text="Save As", command=save_as)
    save_as_button.pack(side=RIGHT, padx=10, pady=5)


def open_pricediff_file():
    # Catch coin
    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    
    # Path to the pricediff.py file
    pricediff_file_path = os.path.join(coin_folder, 'pricediff.py')
    
    # Open a new Tkinter window for editing the file
    editor_window = Toplevel(root)
    editor_window.title(f"Editing {pricediff_file_path}")
    
    # Set the size of the editor window
    editor_window.geometry("600x400")
    
    # Get the main window's position and size
    root.update_idletasks()
    main_window_width = root.winfo_width()
    main_window_height = root.winfo_height()
    main_window_x = root.winfo_x()
    main_window_y = root.winfo_y()
    
    # Calculate the position for the editor window to center it on the main window's screen
    width = 600
    height = 400
    x = main_window_x + (main_window_width // 2) - (width // 2)
    y = main_window_y + (main_window_height // 2) - (height // 2)
    editor_window.geometry(f'{width}x{height}+{x}+{y}')
    
    text_widget = Text(editor_window, wrap='word')
    text_widget.pack(expand=1, fill='both')
    
    scrollbar = Scrollbar(editor_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    
    # Load the content of the file into the Text widget
    with open(pricediff_file_path, 'r') as file:
        text_widget.insert('1.0', file.read())
    
    def save_and_close():
        with open(pricediff_file_path, 'w') as file:
            file.write(text_widget.get('1.0', 'end-1c'))
        editor_window.destroy()
    
    # Add a "Close and Save" button
    save_button = Button(editor_window, text="Close and Save", command=save_and_close)
    save_button.pack(pady=5)



# Create a LabelFrame for the latest restart times
lastrestart_frame = LabelFrame(root, text="Last Restart Events")
lastrestart_frame.pack(padx=1, pady=1, fill="both", expand="no")

# Add a button to open varmove.py
open_varmove_button = tk.Button(root, text="EditMainLogic(varmove.py)", command=open_varmove_file)
open_varmove_button.pack(padx=1, pady=10)

# Add a button to open varmove.py
open_pricediff_button = tk.Button(root, text="EditStopMarketPriceDiff%(pricediff.py)", command=open_pricediff_file)
open_pricediff_button.pack(padx=1, pady=10)

def load_instructions():
    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    instructpath = f"{coin_folder}/instrct.py"
    load_state()
    try:
        spec = importlib.util.spec_from_file_location("instrct", instructpath)
        instrct = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(instrct)
        changeside_var.set(getattr(instrct, "changeside", 0))
        nextamount_var.set(getattr(instrct, "nextamount", 0))
        timeframe_var.set(getattr(instrct, "timeframe", 0))
        max_switches_var.set(getattr(instrct, "max_switches", 0))
        RoiCloseAdd_var.set(getattr(instrct, "RoiCloseAdd", 0))
        spreadAdd_var.set(getattr(instrct, "spreadAdd", 0))
        HRoeInit_var.set(getattr(instrct, "HRoeInit", 0))
        HRoeAddDiff_var.set(getattr(instrct, "HRoeAddDiff", 0))
        HRoeDiff_var.set(getattr(instrct, "HRoeDiff", 0))
        TriggerPoint_var.set(getattr(instrct, "TriggerPoint", 0))


    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        # You may want to set default values here
        pass


def load_instructions2():
    coin = coin_var.get()
    coin_folder = f"coins/{coin}"
    instructpath = f"{coin_folder}/pricediff.py"
    load_state()
    try:
        spec = importlib.util.spec_from_file_location("instrct", instructpath)
        instrct = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(instrct)
        pricediff_var.set(getattr(instrct, "pricediff", 0))
    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        # You may want to set default values here
        pass

def set_changeside(value):
    changeside_var.set(value)
    save_instructions()


def display_current_values():
    load_instructions()
    load_instructions2()
    pricediff_label.config(text=f"Pricediff for StopM in %: {pricediff_var.get()}")
    changeside_label.config(text=f"Change Side Flag: {changeside_var.get()}")
    nextamount_label.config(text=f"Next Amount: {nextamount_var.get()}")
    timeframe_label.config(text=f"timeframe: {timeframe_var.get()}")
    max_switches_label.config(text=f"max_switches: {max_switches_var.get()}")
    RoiCloseAdd_label.config(text=f"RoiCloseAdd: {RoiCloseAdd_var.get()}")
    spreadAdd_label.config(text=f"spreadAdd: {spreadAdd_var.get()}")
    HRoeInit_label.config(text=f"HRoeInit: {HRoeInit_var.get()}")
    HRoeAddDiff_label.config(text=f"HRoeAddDiff: {HRoeAddDiff_var.get()}")
    HRoeDiff_label.config(text=f"HRoeDiff: {HRoeDiff_var.get()}")
    TriggerPoint_label.config(text=f"TriggerPoint: {TriggerPoint_var.get()}")





def save_and_display():
    save_instructions()
    display_current_values()


def on_coin_selected(*args):
    load_instructions()
    save_and_display()
    reolad_toggle_plot()
    display_latest_restarts()

# Bind the on_coin_selected function to the coin_var trace
coin_var.trace("w", on_coin_selected)





# Read the variables from varmove.py


# Refresh the logs
schedule_sync()
 #update_trade_status()
coin_auto_restart()
check_state_led()
update_labels()  # Initial update of labels
root.protocol("WM_DELETE_WINDOW", on_chart_window_close)



root.mainloop()

