import requests
import json
import hashlib
import hmac
import time
import datetime
import sys
import os

# Binance API credentials
api_key = "Yours"
api_secret = "Yours"

# API endpoint URLs
base_url = 'https://fapi.binance.com'
endpoint = '/fapi/v2/account'


# Generate a signature
def generate_signature(data):
    query_string = '&'.join([f"{k}={v}" for k, v in data.items()])
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Create request headers
def create_headers(query_params):
    headers = {
        'X-MBX-APIKEY': api_key
    }
    return headers

# Send request to Binance API
def send_request(url, query_params):
    headers = create_headers(query_params)
    response = requests.get(url, headers=headers, params=query_params)
    return response.json()

# Get USDT balance in mfutures account
def get_usdt_balance():
    # Generate a timestamp for the request
    timestamp = int(time.time() * 1000)

    # Create query parameters
    query_params = {
        'timestamp': timestamp
    }

    # Generate the signature
    query_params['signature'] = generate_signature(query_params)

    # Send the request
    response = send_request(base_url + endpoint, query_params)

    # Find USDT balance
    balances = response['assets']
    usdt_asset = next((asset for asset in balances if asset['asset'] == 'USDT'), None)

    if usdt_asset:
        usdt_balance = usdt_asset['marginBalance']
        latest_balance = usdt_balance

        # Save usdt_balance to file
        with open("FuturesBalanceVars.log", "w") as file:
            file.write(f"latest_balance = {latest_balance}")

        return usdt_balance

# Function to save balance history
def save_balance_history():
    # Get the current timestamp and human-readable date
    current_timestamp = int(time.time())
    current_date = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")

    # Retrieve the latest balance
    usdt_balance = get_usdt_balance()

    # Prepare the new entry
    new_entry = f"{current_timestamp},{usdt_balance},{current_date}\n"

    # Read the existing entries from the log file
    with open("balancehistory.log", "r") as file:
        existing_entries = file.read()

    # Write the new entry followed by the existing entries
    with open("balancehistory.log", "w") as file:
        file.write(new_entry)
        file.write(existing_entries)




# Function to calculate the absolute difference between line 1 and line 5
def calculate_moving_average(lines):
    line_1_parts = lines[0].strip().split(",")
    line_5_parts = lines[4].strip().split(",")

    if len(line_1_parts) >= 2 and len(line_5_parts) >= 2:
        balance_1 = float(line_1_parts[1])
        balance_5 = float(line_5_parts[1])
        moving_average = abs(balance_1 - balance_5)
    else:
        moving_average = 0.0

    return moving_average

# Main program
if __name__ == '__main__':
    usdt_balance = get_usdt_balance()
    if usdt_balance is not None:
        print(f"USDT Balance: {usdt_balance}")
    else:
        print("Failed to retrieve USDT balance.")

    # Start the save_balance_history() function in a separate thread or process
    # This will continuously save the balance to the log file every 2 minutes
    # You can use libraries like threading or multiprocessing for this purpose
    save_balance_history()

    # Read the balance history file
    with open("balancehistory.log", "r") as file:
        balance_history = file.readlines()

    
    moving_average_10min = calculate_moving_average(balance_history[:5])
    




    # Save the moving average balances to the usdt_balance_diff_calc.log file
    with open("usdt_balance_diff_calc.log", "w") as file:
        file.write(f"10min = {moving_average_10min}\n")




    # Start the script in a loop to run every 2 minutes
    while True:
        python_executable = sys.executable
        os.system(f"{python_executable} BalanceHistory.py")  

        # Sleep for 2 minutes
        time.sleep(120)

