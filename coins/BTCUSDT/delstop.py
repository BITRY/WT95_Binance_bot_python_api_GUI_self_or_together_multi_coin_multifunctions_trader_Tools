import time
import math
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.enums import *
import decimal
# Import required functions and variables from livego.py
import random
import config
from varmove import *
from pricediff import pricediff
import json



# Create a Binance client
client = Client(config.api_key, config.api_secret)



symbol = Coin

# Global variable to store the last checked trade timestamp
last_checked_timestamp = 0

# This line is where you load your JSON data from the file
with open('order_ids.json', 'r') as file:
    try:
        stop_market_orders = set(json.load(file))
    except json.decoder.JSONDecodeError:
        print("File is empty, no data to load.")
        stop_market_orders = set()  # Initializing to an empty set


def load_order_ids():
    try:
        with open('order_ids.json', 'r') as file:
            content = file.read()
            if content:  # If content is not empty
                return set(json.loads(content))
            else:  # If content is empty
                return set()  # Returns an empty set
    except FileNotFoundError:
        return set()  # Returns an empty set if file does not exist





    
def has_new_trade_occurred(symbol):
    global last_checked_timestamp
    
    # Retrieve the latest trade for the symbol from the Binance API
    trades = client.futures_recent_trades(symbol=symbol, limit=1)
    
    # Check if any trade data was returned
    if len(trades) > 0:
        latest_trade = trades[0]
        trade_timestamp = int(latest_trade['time'])
        
        # Compare the trade timestamp with the last checked timestamp
        if trade_timestamp > last_checked_timestamp:
            # Update the last checked timestamp to the latest trade timestamp
            last_checked_timestamp = trade_timestamp
            return True
    
    return False



# Function to check if a position is open for the symbol
def is_position_open(symbol):
    account_info = client.futures_account()
    positions = account_info['positions']
    for position in positions:
        if position['symbol'] == symbol:
            return True
    return False



def get_entry_price(symbol):
    positions = client.futures_position_information(symbol=symbol)

    for position in positions:
        if position['positionSide'] == 'BOTH' and position['positionAmt'] != '0':
            entry_price = float(position['entryPrice'])
            return entry_price

    return None






def set_stop_limit_order(symbol, stop_limit_order_side, stop_limit_price, quantity):
    # Load stop_market_orders from file
    stop_market_orders = load_order_ids()

    try:
        symbol_info = client.futures_exchange_info()
        quantity_precision = None
        for symbol_data in symbol_info['symbols']:
            if symbol_data['symbol'] == symbol:
                quantity_precision = symbol_data['quantityPrecision']
                break

        if quantity_precision is not None:
            quantity = decimal.Decimal(quantity).quantize(decimal.Decimal('0.' + '0' * quantity_precision), rounding=decimal.ROUND_DOWN)
        else:
            print(f"Symbol information not found for {symbol}")
            return

        order_type = "STOP_MARKET"
        if stop_limit_order_side == "BUY":
            side = SIDE_BUY
        elif stop_limit_order_side == "SELL":
            side = SIDE_SELL
        else:
            print("Invalid stop limit order side")
            return

        if has_new_trade_occurred(symbol):
            response = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                stopPrice=stop_limit_price
            )

            # Add the orderId to the set
            stop_market_orders.add(response['orderId'])

            # Save the order IDs to the file
            with open('order_ids.json', 'w') as file:
                json.dump(list(stop_market_orders), file)

            print("Stop limit order response:", response)
        else:
            print("No new trade occurred. Skipping stop limit order placement.")
    except BinanceAPIException as e:
        print(f"Error placing stop limit order: {e}")

        





def delete_all_stop_market_orders(symbol):
    # Iterate over the stop_market_orders set and delete the orders
    deleted_orders = 0
    for orderId in list(stop_market_orders):  # We convert the set to a list to avoid RuntimeError
        try:
            client.futures_cancel_order(symbol=symbol, orderId=orderId)
            stop_market_orders.remove(orderId)  # Remove the orderId from the set
            deleted_orders += 1
            print(f"Deleted stop market order with ID: {orderId}")
        except BinanceAPIException as e:
            if e.code == -2011:
                print(f"Error deleting stop market order: Order {orderId} not found or already processed.")
                stop_market_orders.remove(orderId)  # Remove the orderId from the set anyway
            else:
                print(f"Error deleting stop market order: {e}")

    if deleted_orders == 0:
        print("No existing stop market orders found.")
    else:
        print(f"Deleted {deleted_orders} stop market orders for symbol {symbol}")

    # Save the order IDs to the file
    with open('order_ids.json', 'w') as file:
        json.dump(list(stop_market_orders), file)








# Function to get the price filters for the symbol
def get_symbol_price_filters(symbol):
    symbol_info = client.futures_exchange_info()
    for info in symbol_info['symbols']:
        if info['symbol'] == symbol:
            return info['filters']
    return None

# Function to get the price filter step size for the symbol
def get_price_filter_step_size(filters):
    for f in filters:
        if f['filterType'] == 'PRICE_FILTER':
            return float(f['tickSize'])
    return None



# Function to check if a stop market order with the same order ID already exists
def check_existing_stop_market_order(stop_market_orders, order_id):
    # Retrieve all open orders
    open_orders = client.futures_get_open_orders(symbol=symbol)

    # Check if any of the open orders match the given order ID and order type
    for order in open_orders:
        if order['orderId'] == order_id and order['type'] == 'STOP_MARKET':
            return True  # Stop market order with the same order ID already exists

    return False  # No stop market order with the same order ID exists



# Main function to execute the script
def main():
    order_id = None

    # Load stop_market_orders from file
    stop_market_orders = load_order_ids()

    # Check if a position is open for the symbol
    print("Checking if a position is open...")
    if is_position_open(symbol):
        print("Position is open.")

        # Get the actual position size and side
        account_info = client.futures_account()
        positions = account_info['positions']
        position_size = 0
        position_side = None

        for position in positions:
            if position['symbol'] == symbol:
                position_size = float(position['positionAmt'])
                if position_size > 0:
                    position_side = SIDE_BUY
                elif position_size < 0:
                    position_side = SIDE_SELL
                break

        if position_side and position_size != 0:
            print(f"Position side: {position_side}")
            print(f"Position size: {position_size}")

            # Get the entry price for the open position
            bought_price = get_entry_price(symbol)

            if bought_price is not None:
                print(f"Bought price: {bought_price}")

                # Calculate the stop limit order price based on the pricediff variable
                pricediff_percentage = pricediff / 100  # Adjust the divisor as needed
                stop_limit_price = bought_price - (bought_price * pricediff_percentage) if position_side == SIDE_BUY else bought_price + (bought_price * pricediff_percentage)

                # Get the price filters for the symbol
                symbol_filters = get_symbol_price_filters(symbol)
                if symbol_filters is not None:
                    # Get the price filter step size
                    price_filter_step_size = get_price_filter_step_size(symbol_filters)
                    if price_filter_step_size is not None:
                        # Calculate the rounded stop limit order price
                        rounded_price = math.floor(stop_limit_price / price_filter_step_size) * price_filter_step_size
                        stop_limit_price = rounded_price
                        print(f"Stop limit order price: {stop_limit_price}")

                        # Round the stop limit order price to 8 decimal places
                        stop_limit_price = round(stop_limit_price, 8)

                        # Set the quantity based on the position size
                        quantity = abs(position_size) * 1.10

                        # Set the stop limit order side
                        stop_limit_order_side = SIDE_SELL if position_side == SIDE_BUY else SIDE_BUY

                        # Check if a stop market order with the same order ID already exists
                        existing_order = check_existing_stop_market_order(stop_market_orders, order_id)

                        if not existing_order:
                            # Place the stop limit order
                            print("Placing stop limit order...")
                            delete_all_stop_market_orders(symbol)

                        else:
                            print("Stop market order already exists.")

                    else:
                        print("Unable to determine price filter step size.")
                else:
                    print("Unable to determine symbol price filters.")
            else:
                print("Unable to determine bought price.")

        else:
            print("Unable to determine position side or size.")
    else:
        print("Position is not open.")


# Call the main function
main()
