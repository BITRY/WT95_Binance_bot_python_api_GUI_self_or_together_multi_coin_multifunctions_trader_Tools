import tkinter as tk
import asyncio
import threading
from binance import AsyncClient, BinanceSocketManager
import config
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import atexit
from binance import ThreadedWebsocketManager
from varmove import Coin
	
import subprocess


symbol = Coin
# Create the Tkinter window
root = tk.Tk()
root.title("Live Order Book")
root.geometry("625x600")  # Set the window size

# Create a frame to hold the sellers and buyers
order_book_frame = tk.Frame(root, width=700)  # Adjust the width as desired
order_book_frame.grid(row=1, column=0, padx=10, pady=10, sticky="n")

# Create labels for sellers and buyers
seller_label = tk.Label(order_book_frame, text="Sellers")
seller_label.grid(row=0, column=0)

seller_text = tk.Text(order_book_frame, height=20, width=38)  # Adjust width as needed
seller_text.grid(row=1, column=0)

buyer_label = tk.Label(order_book_frame, text="Buyers")
buyer_label.grid(row=2, column=0)

buyer_text = tk.Text(order_book_frame, height=20, width=38)  # Adjust width as needed
buyer_text.grid(row=3, column=0)



# Global variables to store the order book data
asks_data = []
bids_data = []

# Set the font for sellers and buyers
seller_text.tag_configure("seller_font", font=("Arial", 10), foreground="red")
buyer_text.tag_configure("buyer_font", font=("Arial", 10), foreground="green")

# Create a frame to hold the total amounts and median price
summary_frame = tk.Frame(root)
summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Create labels for total amounts and median price
total_seller_label = tk.Label(summary_frame, text="Total Seller Quantity (SUMM of 35):")
total_seller_label.grid(row=0, column=0)

total_seller_amount = tk.StringVar()
total_seller_value = tk.Label(summary_frame, textvariable=total_seller_amount)
total_seller_value.grid(row=0, column=1)

total_buyer_label = tk.Label(summary_frame, text="Total Buyer Quantity (SUMM of 35):")
total_buyer_label.grid(row=1, column=0)

total_buyer_amount = tk.StringVar()
total_buyer_value = tk.Label(summary_frame, textvariable=total_buyer_amount)
total_buyer_value.grid(row=1, column=1)

median_price_label = tk.Label(summary_frame, text="Median Price:")
median_price_label.grid(row=2, column=0)

median_price_value = tk.StringVar()
median_price_display = tk.Label(summary_frame, textvariable=median_price_value)
median_price_display.grid(row=2, column=1)

websocket_connector = None

# Create a global variable for the figure and canvas
fig = plt.Figure(figsize=(4, 2), dpi=100)  # Adjust the figsize as desired
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")

# Configure grid weights to expand the canvas column
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)




def update_window_data(symbol):
    global asks_data, bids_data

    # Clear existing text in seller_text and buyer_text
    seller_text.delete("1.0", tk.END)
    buyer_text.delete("1.0", tk.END)

    # Calculate the total quantity of sellers and buyers (Top 3)
    total_seller = sum(float(ask.split(",")[1].split(":")[1].strip()) for ask in asks_data[:10])
    total_buyer = sum(float(bid.split(",")[1].split(":")[1].strip()) for bid in bids_data[:10])

    # Reverse the order of the seller's data
    reversed_sellers = asks_data[::-1]

    # Insert asks and bids data in seller_text and buyer_text with respective colors
    for ask in reversed_sellers:
        seller_text.insert(tk.END, ask + "\n", "seller_font")  # Use seller_font tag for sellers' text

    for bid in bids_data:
        buyer_text.insert(tk.END, bid + "\n", "buyer_font")  # Use buyer_font tag for buyers' text

    # Calculate the median price from the latest ask and bid
    if asks_data:
        last_ask = float(asks_data[-1].split(",")[0].split(":")[1].strip())
    else:
        last_ask = 0.0

    if bids_data:
        last_bid = float(bids_data[-1].split(",")[0].split(":")[1].strip())
    else:
        last_bid = 0.0

    median_price = (last_ask + last_bid) / 2

    # Update the total quantity and median price labels
    total_seller_amount.set(f"{total_seller:.2f}")
    total_buyer_amount.set(f"{total_buyer:.2f}")
    median_price_value.set(f"{median_price:.2f}")
    
    # Update the plot
    plot_total_amounts(symbol, median_price)
    



def plot_total_amounts(symbol, median_price):
    # Clear the previous plot
    ax.clear()

    # Define the labels and values for the bar chart
    labels = ['Total Buyer Amount', 'Total Seller Amount']
    values = [float(total_buyer_amount.get()), float(total_seller_amount.get())]

    # Create a bar chart
    ax.bar(labels, values)

    # Add labels and title to the chart
    ax.set_xlabel(f'LIVE WEBSOCKET DATA for {symbol}')
    ax.set_ylabel('Amount')
    ax.set_title('Total Buyer and Seller Amounts')
    # Add the median price to the plot
    ax.text(0.5, 1.05, f"Median Price: {median_price:.2f}", transform=ax.transAxes, ha='right')

    # Adjust the position above the title
    ax.title.set_position([0.5, 1.15])

    # Redraw the canvas
    canvas.draw()



def receive_websocket_data(depth, symbol):
    global asks_data, bids_data

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    twm = ThreadedWebsocketManager(api_key=config.api_key, api_secret=config.api_secret)
    twm.start()

    def process_message(msg):
        if "asks" in msg and "bids" in msg:
            asks = msg["asks"]
            bids = msg["bids"]

            # Format the asks and bids data
            formatted_asks = [f"Price: {ask[0]}, Quantity: {ask[1]}" for ask in asks]
            formatted_bids = [f"Price: {bid[0]}, Quantity: {bid[1]}" for bid in bids]

            # Update the order book data
            global asks_data, bids_data
            asks_data = formatted_asks
            bids_data = formatted_bids

            # Call update_window_data() directly to update the Tkinter window
            update_window_data(symbol)

    # Start the depth socket
    twm.start_depth_socket(callback=process_message, symbol=symbol, depth=depth)

    # Join the websocket manager
    twm.join()

@atexit.register
def close_connector():
    global websocket_connector
    if websocket_connector and not websocket_connector.closed:
        asyncio.get_event_loop().run_until_complete(websocket_connector.close())

async def fetch_order_book_task():
    while True:
        await _fetch_order_book()
        await asyncio.sleep(0.1)

async def fetch_order_book_task():
    global websocket_connector

    while True:
        client = await AsyncClient.create(api_key=config.api_key, api_secret=config.api_secret)

        try:
            # Fetch the order book data
            order_book = await client.get_order_book(symbol=symbol, limit=35)

            if "asks" in order_book and "bids" in order_book:
                asks = order_book["asks"]
                bids = order_book["bids"]

                # Format the asks and bids data
                formatted_asks = [f"Price: {ask[0]}, Quantity: {ask[1]}" for ask in asks]
                formatted_bids = [f"Price: {bid[0]}, Quantity: {bid[1]}" for bid in bids]

                # Update the order book data
                global asks_data, bids_data
                asks_data = formatted_asks
                bids_data = formatted_bids

                # Update the Tkinter window data
                update_window_data(symbol)

        except Exception as e:
            print(f"Error fetching order book: {e}")

        # Close the connection
        if client:
            await client.close_connection()

        # Sleep for 2 seconds before fetching the order book again
        await asyncio.sleep(2)

@atexit.register
def close_connector():
    global websocket_connector
    if websocket_connector and not websocket_connector.closed:
        asyncio.get_event_loop().run_until_complete(websocket_connector.close())

def start_task():
    threading.Thread(target=asyncio.run, args=(fetch_order_book_task(),)).start()

def start_websocket_stream(depth):
    threading.Thread(target=receive_websocket_data, args=(depth,symbol)).start()
    


# Call the function to start the WebSocket stream with depth 20
start_websocket_stream(20)
    

# Set the font for small text
seller_text.tag_configure("small_font", font=("Arial", 10))
buyer_text.tag_configure("small_font", font=("Arial", 10))







# Start the Tkinter event loop
root.mainloop()

