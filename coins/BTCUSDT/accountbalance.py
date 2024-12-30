import requests
import json
import hashlib
import hmac
import time
import config

# Binance API credentials
api_key=config.api_key
api_secret =config.api_secret


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

# Main program
if __name__ == '__main__':
    usdt_balance = get_usdt_balance()
    if usdt_balance is not None:
        print(f"USDT Balance: {usdt_balance}")
    else:
        print("Failed to retrieve USDT balance.")

