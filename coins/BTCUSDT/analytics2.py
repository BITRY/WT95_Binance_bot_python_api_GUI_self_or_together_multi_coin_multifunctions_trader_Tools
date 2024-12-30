import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
from datetime import datetime
import tkinter as tk

class AnalyticsCalculator:
    def __init__(self, log_entries):
        self.all_log_entries = self.parse_log_entries(log_entries)

    def parse_log_entries(self, log_entries):
        parsed_entries = []
        pattern = re.compile(r'(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}) - .+ PNL=([-+]?\d*\.?\d+)')
        for line in log_entries:
            match = pattern.search(line)
            if match:
                log_date = datetime.strptime(match.group(1), '%d-%b-%y %H:%M:%S')
                pnl_value = float(match.group(2))
                parsed_entries.append({'log_date': log_date, 'pnl_value': pnl_value})
        return parsed_entries

    def calculate_and_plot_pnl(self, plot_frame, start_date, end_date, coin_name):
        filtered_events = [event for event in self.all_log_entries if start_date <= event['log_date'] <= end_date]
        if filtered_events:
            pnl_times, pnl_values = self.calculate_cumulative_pnl(filtered_events)
            self.plot_pnl_graph(plot_frame, start_date, end_date, coin_name, pnl_times, pnl_values)
        else:
            self.plot_no_events_graph(plot_frame, start_date, end_date, coin_name)

    def calculate_cumulative_pnl(self, filtered_events):
        pnl_times = [event['log_date'] for event in filtered_events]
        cumulative_pnl = 0.0
        pnl_values = []
        for event in filtered_events:
            cumulative_pnl += event['pnl_value']
            pnl_values.append(cumulative_pnl)
        return pnl_times, pnl_values

    def plot_pnl_graph(self, plot_frame, start_date, end_date, coin_name, pnl_times, pnl_values):
        fig, ax = plt.subplots()
        ax.plot(pnl_times, pnl_values, linestyle='-', label='Cumulative PNL', color='blue', linewidth=1.5)
        ax.set_xlabel('Time')
        ax.set_ylabel('Accumulated PNL')
        ax.set_xticks(pnl_times)
        ax.set_xticklabels([time.strftime('%Y-%m-%d %H:%M:%S') for time in pnl_times], rotation=45)
        ax.grid(True)
        ax.set_title(f'{coin_name} PNL from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
        ax.legend()
        fig.tight_layout()

        for widget in plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_no_events_graph(self, plot_frame, start_date, end_date, coin_name):
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No events', horizontalalignment='center', verticalalignment='center', fontsize=12, transform=ax.transAxes)
        ax.set_title(f'{coin_name} PNL from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}')
        ax.axis('off')

        for widget in plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

