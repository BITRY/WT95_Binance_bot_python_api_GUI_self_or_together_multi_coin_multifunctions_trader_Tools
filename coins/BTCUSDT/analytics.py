import tkinter as tk
from tkinter import ttk, scrolledtext
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from dateutil import parser


class LogAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Log Analyzer")

        self.scroll = scrolledtext.ScrolledText(master, width=100, height=40)
        self.scroll.pack(side=tk.LEFT, expand=True, fill='both')
        self.apply_text_styles()

        self.pnl_frame = tk.Frame(master, width=100)
        self.pnl_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        self.setup_date_range_controls()
        self.load_log()
        self.setup_pnl_value_fields()
        self.display_all_pnl_values()
        self.setup_graph_frame()
        self.plot_pnl_graph()
        self.setup_zoom_buttons()
        self.setup_scroll_buttons()
        self.setup_fullscreen_button()
        self.setup_chart_toggle_button()

    def setup_date_range_controls(self):
        # Setup for terminal filter
        tk.Label(self.pnl_frame, text="Filter logs by date:").pack()
        self.filter_start_date = ttk.Combobox(self.pnl_frame, values=[], width=10)
        self.filter_start_date.pack()
        self.filter_end_date = ttk.Combobox(self.pnl_frame, values=[], width=10)
        self.filter_end_date.pack()
        tk.Button(self.pnl_frame, text="Apply Filter", command=self.filter_logs_by_date).pack()

        # Setup for PNL Calculation
        tk.Label(self.pnl_frame, text="Calculate PNL:").pack()
        self.pnl_start_date = ttk.Combobox(self.pnl_frame, values=[], width=10)
        self.pnl_start_date.pack()
        self.pnl_end_date = ttk.Combobox(self.pnl_frame, values=[], width=10)
        self.pnl_end_date.pack()
        tk.Button(self.pnl_frame, text="Calculate PNL", command=self.calculate_and_plot_pnl).pack()
        self.result_label = tk.Label(self.pnl_frame, text="")
        self.result_label.pack()

        # Bind combobox selection event to update the graph
        self.pnl_start_date.bind("<<ComboboxSelected>>", lambda event: self.plot_chart())
        self.pnl_end_date.bind("<<ComboboxSelected>>", lambda event: self.plot_chart())

    def apply_text_styles(self):
        self.scroll.tag_config('pnl', foreground='dark green')
        self.scroll.tag_config('weight', font=('TkDefaultFont', 10, 'bold'))

    def load_log(self):
        filename = 'HODL_TRADES.log'
        try:
            with open(filename, 'r') as f:
                log_contents = f.read()
                # Store all log entries for filtering based on date selection.
                self.all_log_entries = log_contents.split('\n')
                self.prepare_combobox_values(log_contents)
                # Initial display filter to show all entries
                self.filter_logs_by_date()
        except FileNotFoundError:
            self.scroll.insert(tk.END, "Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error loading log file: {str(e)}\n")

    def display_logs(self, logs):
        self.scroll.delete('1.0', tk.END)
        for line in logs:
            self.insert_with_tags(line + '\n')

    def insert_with_tags(self, line):
        if "PNL=" in line:
            pos = self.scroll.index('end')
            self.scroll.insert('end', line)
            self.scroll.tag_add('pnl', pos, f"{pos} lineend")
        elif "weight=" in line:
            pos = self.scroll.index('end')
            self.scroll.insert('end', line)
            self.scroll.tag_add('weight', pos, f"{pos} lineend")
        else:
            self.scroll.insert('end', line)

    def prepare_combobox_values(self, log_contents):
        date_pattern = re.compile(r"(\d{1,2}-\w{3}-\d{2})")
        dates = sorted(set(match.group(1) for match in date_pattern.finditer(log_contents)), key=lambda x: datetime.strptime(x, '%d-%b-%y'))
        self.filter_start_date['values'] = dates
        self.filter_end_date['values'] = dates
        self.pnl_start_date['values'] = dates
        self.pnl_end_date['values'] = dates
        if dates:
            self.filter_start_date.set(dates[0])
            self.filter_end_date.set(dates[-1])
            self.pnl_start_date.set(dates[0])
            self.pnl_end_date.set(dates[-1])

    def filter_logs_by_date(self):
        # Apply date filtering and then display filtered logs
        start_date = datetime.strptime(self.filter_start_date.get(), '%d-%b-%y')
        end_date = datetime.strptime(self.filter_end_date.get(), '%d-%b-%y')
        filtered_logs = []
        for line in self.all_log_entries:
            match = re.match(r"(\d{2}-\w{3}-\d{2}).*", line)
            if match:
                log_date = datetime.strptime(match.group(1), '%d-%b-%y')
                if start_date <= log_date <= end_date:
                    filtered_logs.append(line)
        self.display_logs(filtered_logs)

    def calculate_and_plot_pnl(self):
        # Calculate PNL based on selected date range
        pnl_sum = self.calculate_pnl()
        if pnl_sum is not None:
            # Plot PNL graph with selected date range
            self.plot_pnl_graph()

    def calculate_pnl(self):
        # Calculate PNL based on selected date range
        pnl_pattern = re.compile(r"(\d{2}-\w{3}-\d{2}).*PNL=([-\d.]+)")
        try:
            start_date = datetime.strptime(self.pnl_start_date.get(), '%d-%b-%y')
            end_date = datetime.strptime(self.pnl_end_date.get(), '%d-%b-%y')
        except ValueError:
            self.scroll.insert(tk.END, "Invalid date format. Please use the format 'DD-Mmm-YY'.\n")
            return None

        pnl_sum = 0.0
        for line in self.all_log_entries:
            match = pnl_pattern.search(line)
            if match:
                log_date = datetime.strptime(match.group(1), '%d-%b-%y')
                pnl_value = float(match.group(2))
                if start_date <= log_date <= end_date:
                    pnl_sum += pnl_value
        return pnl_sum

    def setup_pnl_value_fields(self):
        # Setup PNL value fields
        self.pnl_labels = []
        interval_labels = ["1 hour", "3 hours", "6 hours", "12 hours", "24 hours", "48 hours", "7 days"]
        for interval in interval_labels:
            label = tk.Label(self.pnl_frame, text=f"PNL last {interval}:")
            label.pack()
            self.pnl_labels.append(label)

    def display_all_pnl_values(self):
        # Calculate and display all PNL values
        current_time = datetime.now()
        intervals = [1, 3, 6, 12, 24, 48, 7*24]  # Hours
        for i, interval in enumerate(intervals):
            start_time = current_time - timedelta(hours=interval)
            end_time = current_time
            pnl_value = self.calculate_pnl_for_interval(start_time, end_time)
            self.pnl_labels[i].config(text=f"PNL last {interval} hours: {pnl_value:.2f}")

    def calculate_pnl_for_interval(self, start_time, end_time):
        # Calculate PNL for the specified time interval
        pnl_pattern = re.compile(r"(\d{2}-\w{3}-\d{2}).*PNL=([-\d.]+)")
        pnl_sum = 0.0
        for line in self.all_log_entries:
            match = pnl_pattern.search(line)
            if match:
                log_date = datetime.strptime(match.group(1), '%d-%b-%y')
                pnl_value = float(match.group(2))
                if start_time <= log_date <= end_time:
                    pnl_sum += pnl_value
        return pnl_sum

    def setup_graph_frame(self):
        self.graph_frame = tk.Frame(self.master)  # New frame for the graph
        self.graph_frame.pack(side=tk.RIGHT, fill='both', expand=True)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot_pnl_graph(self):
        pnl_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*PNL=([-\d.]+)")
        pnl_times = []
        pnl_values = []
        real_pnl_values = []  # Real PNL values at each point
        accumulated_pnl = 0.0  # Accumulated PNL over time
        for line in self.all_log_entries:
            match = pnl_pattern.search(line)
            if match:
                log_date = parser.parse(match.group(1))
                pnl_time = mdates.date2num(log_date)
                pnl_value = float(match.group(2))
                accumulated_pnl += pnl_value  # Accumulate PNL
                pnl_times.append(pnl_time)
                pnl_values.append(accumulated_pnl)  # Use accumulated PNL value
                real_pnl_values.append(pnl_value)  # Store real PNL value

        if not pnl_times:
            # Set default x-axis limits if pnl_times is empty
            self.ax.set_xlim(mdates.date2num(datetime.now()) - 1, mdates.date2num(datetime.now()) + 1)
        else:
            self.ax.clear()
            self.ax.plot_date(pnl_times, pnl_values, linestyle='-', label='PNL', color='blue', linewidth=1.5)
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Accumulated PNL')  # Update y-axis label
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
            self.ax.xaxis.set_tick_params(rotation=45)  # Rotate x-axis labels for better visibility
            self.ax.grid(True)
            
            # Add PNL values directly on each point
            for time, value, real_pnl in zip(pnl_times, pnl_values, real_pnl_values):
                self.ax.text(time, value, f"{value:.2f}\n{real_pnl:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)
            
            # Set initial x-axis limits and add more space around the diagram
            self.ax.set_xlim(pnl_times[0] - 0.05, pnl_times[-1] + 0.05)
            plt.subplots_adjust(bottom=0.3)  # Add more space to the bottom
        
        self.canvas.draw()

    def setup_zoom_buttons(self):
        tk.Button(self.pnl_frame, text="+", command=self.zoom_in).pack(side=tk.LEFT)
        tk.Button(self.pnl_frame, text="-", command=self.zoom_out).pack(side=tk.LEFT)

    def zoom_in(self):
        xlim = self.ax.get_xlim()
        delta = (xlim[1] - xlim[0]) * 0.1  # Zoom factor: 10% of current range
        self.ax.set_xlim(xlim[0] + delta, xlim[1] - delta)
        self.canvas.draw()

    def zoom_out(self):
        xlim = self.ax.get_xlim()
        delta = (xlim[1] - xlim[0]) * 0.1  # Zoom factor: 10% of current range
        self.ax.set_xlim(xlim[0] - delta, xlim[1] + delta)
        self.canvas.draw()

    def setup_scroll_buttons(self):
        tk.Button(self.pnl_frame, text="←", command=lambda: self.scroll_x_axis(-1)).pack(side=tk.LEFT)
        tk.Button(self.pnl_frame, text="→", command=lambda: self.scroll_x_axis(1)).pack(side=tk.LEFT)

    def scroll_x_axis(self, direction):
        xlim = self.ax.get_xlim()
        delta = (xlim[1] - xlim[0]) * 0.1 * direction  # Scroll factor: 10% of current range
        self.ax.set_xlim(xlim[0] + delta, xlim[1] + delta)
        self.canvas.draw()
    
    def setup_fullscreen_button(self):
        self.fullscreen_button = tk.Button(self.pnl_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.BOTTOM)

    def toggle_fullscreen(self):
        if self.master.attributes("-fullscreen"):
            self.master.attributes("-fullscreen", False)
        else:
            self.master.attributes("-fullscreen", True)

    def setup_chart_toggle_button(self):
        self.chart_type = tk.StringVar(value="PNL")
        tk.Radiobutton(self.pnl_frame, text="PNL", variable=self.chart_type, value="PNL", command=self.plot_chart).pack(side=tk.BOTTOM)
        tk.Radiobutton(self.pnl_frame, text="ROE", variable=self.chart_type, value="ROE", command=self.plot_chart).pack(side=tk.BOTTOM)
        tk.Radiobutton(self.pnl_frame, text="PosSize", variable=self.chart_type, value="PosSize", command=self.plot_chart).pack(side=tk.BOTTOM)
        tk.Radiobutton(self.pnl_frame, text="ROE_Close", variable=self.chart_type, value="ROE_Close", command=self.plot_chart).pack(side=tk.BOTTOM)
        tk.Radiobutton(self.pnl_frame, text="Combined", variable=self.chart_type, value="Combined", command=self.plot_chart).pack(side=tk.BOTTOM)
        tk.Radiobutton(self.pnl_frame, text="Combined_PlotScalled", variable=self.chart_type, value="Combined_PlotScalled", command=self.plot_chart).pack(side=tk.BOTTOM)
        tk.Radiobutton(self.pnl_frame, text="Combine_ROE + ROEClose + PosSize", variable=self.chart_type, value="Combine_ROE", command=self.plot_chart).pack(side=tk.BOTTOM)


    def plot_chart(self):
        chart_type = self.chart_type.get()
        if chart_type == "PNL":
            self.plot_pnl_graph()
        elif chart_type == "ROE":
            self.plot_roe_graph()
        elif chart_type == "PosSize":
            self.plot_pos_size_graph()
        elif chart_type == "ROE_Close":
            self.plot_roe_close_graph()
        elif chart_type == "Combined":
            self.plot_combined_graph()
        elif chart_type == "Combine_ROE":
            self.plot_combined_Combine_ROE_graph()
        elif chart_type == "Combined_PlotScalled":
            self.plot_combined_graph_plotShow()


    def plot_roe_graph(self):
        filename = 'HODL_INFO.log'
        try:
            with open(filename, 'r') as f:
                log_contents = f.readlines()
                roe_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROE: ([-\d.]+)%")
                roe_times = []
                roe_values = []
                for line in log_contents:
                    match = roe_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_time = mdates.date2num(log_date)
                        roe_value = float(match.group(2))
                        roe_times.append(roe_time)
                        roe_values.append(roe_value)

                self.ax.clear()
                if roe_times:
                    self.ax.plot_date(roe_times, roe_values, 'b-', label='ROE', linewidth=1.5)
                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('ROE (%)')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
                    self.ax.xaxis.set_tick_params(rotation=45)
                    self.ax.grid(True)
                else:
                    self.ax.text(0.5, 0.5, 'No ROE Data Available', ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Log file: {str(e)}\n")


    def determine_line_colors(self, pos_size_values):
        colors = []
        for i in range(len(pos_size_values)):
            current_color = 'orange' if pos_size_values[i] < 0 else 'pink'
            prev_color = 'orange' if pos_size_values[i - 1] < 0 else 'pink' if i > 0 else current_color
            colors.append((prev_color, current_color))
        return colors

    def plot_pos_size_graph(self):
        filename = 'HODL_INFO.log'
        try:
            with open(filename, 'r') as f:
                log_contents = f.readlines()
                pos_size_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*Pos_Size: ([-\d.]+)")
                pos_size_times = []
                pos_size_values = []
                for line in log_contents:
                    match = pos_size_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        pos_size_time = mdates.date2num(log_date)
                        pos_size_value = float(match.group(2))
                        pos_size_times.append(pos_size_time)
                        pos_size_values.append(pos_size_value)

                self.ax.clear()
                if pos_size_times:
                    # Determine line colors based on the sign of PosSize values
                    line_colors = self.determine_line_colors(pos_size_values)

                    # Plot the first point to start the line
                    self.ax.plot_date(pos_size_times[:1], pos_size_values[:1], '-', color=line_colors[0][0], label='PosSize', linewidth=1.5)

                    # Plot the rest of the line segment by segment, changing color where necessary
                    for i in range(1, len(pos_size_times)):
                        if line_colors[i][0] != line_colors[i][1]:
                            # If the color changes, plot the previous segment and start a new line
                            self.ax.plot_date(pos_size_times[i-1:i+1], pos_size_values[i-1:i+1], '-', color=line_colors[i][0], linewidth=1.5)
                        else:
                            # If the color remains the same, continue the line
                            self.ax.plot_date(pos_size_times[i-1:i+1], pos_size_values[i-1:i+1], '-', color=line_colors[i][1], linewidth=1.5)

                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('PosSize')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
                    self.ax.xaxis.set_tick_params(rotation=45)
                    self.ax.grid(True)
                else:
                    self.ax.text(0.5, 0.5, 'No PosSize Data Available', ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
        except FileNotFoundError:
            self.scroll.insert(tk.END, "PosSize Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading PosSize Log file: {str(e)}\n")





    def plot_combined_Combine_ROE_graph(self):
        self.ax.clear()
        self.plot_pos_size_graph() 
        roe_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROE: ([-\d.]+)%")
        roe_times = []
        roe_values = []
        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = roe_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_time = mdates.date2num(log_date)
                        roe_value = float(match.group(2))
                        roe_times.append(roe_time)
                        roe_values.append(roe_value)
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Log file: {str(e)}\n")

        if roe_times:
            self.ax.plot_date(roe_times, roe_values, 'g-', label='ROE', linewidth=1.5)  # Line for ROE
            latest_roe_time = roe_times[-1]
            latest_roe_value = roe_values[-1]
            self.ax.plot_date(latest_roe_time, latest_roe_value, 'go')  # Marker for the latest ROE entry
            self.ax.text(latest_roe_time, latest_roe_value, f" {latest_roe_value:.2f}%", ha='left', va='bottom', fontsize=8, rotation=45)



        # New section for ROE_Close
        roe_close_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROICloseLevel_Valve_ Modification_BUY_ON_START: ([-\d.]+)")
        roe_close_times = []
        roe_close_values = []
        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = roe_close_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_close_time = mdates.date2num(log_date)
                        roe_close_value = float(match.group(2))
                        roe_close_times.append(roe_close_time)
                        roe_close_values.append(roe_close_value)
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Close Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Close Log file: {str(e)}\n")

        if roe_close_times:
            self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)  # Line for ROE Close
            latest_roe_close_time = roe_close_times[-1]
            latest_roe_close_value = roe_close_values[-1]
            self.ax.plot_date(latest_roe_close_time, latest_roe_close_value, 'ro')  # Marker for the latest ROE Close entry
            self.ax.text(latest_roe_close_time, latest_roe_close_value, f" {latest_roe_close_value:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)


        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper left')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        self.ax.xaxis.set_tick_params(rotation=45)
        self.ax.grid(True)
        self.canvas.draw()
        

    def plot_roe_close_graph(self):
        filename = 'HODL_INFO.log'
        try:
            with open(filename, 'r') as f:
                log_contents = f.readlines()
                roe_close_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROICloseLevel_Valve_ Modification_BUY_ON_START: ([-\d.]+)")
                roe_close_times = []
                roe_close_values = []
                for line in log_contents:
                    match = roe_close_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_close_time = mdates.date2num(log_date)
                        roe_close_value = float(match.group(2))
                        roe_close_times.append(roe_close_time)
                        roe_close_values.append(roe_close_value)

                self.ax.clear()
                if roe_close_times:
                    self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)
                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('ROE Close')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
                    self.ax.xaxis.set_tick_params(rotation=45)
                    self.ax.grid(True)
                else:
                    self.ax.text(0.5, 0.5, 'No ROE Close Data Available', ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Close Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Close Log file: {str(e)}\n")



        if roe_close_times:
            self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)

        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper left')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        self.ax.xaxis.set_tick_params(rotation=45)
        self.ax.grid(True)
        self.canvas.draw()





    def plot_combined_graph(self):
        self.ax.clear()
        self.plot_pos_size_graph() 
        pnl_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*PNL=([-\d.]+)")
        pnl_times = []
        pnl_values = []
        real_pnl_values = []  # Real PNL values at each point
        accumulated_pnl = 0.0  # Accumulated PNL over time
        for line in self.all_log_entries:
            match = pnl_pattern.search(line)
            if match:
                log_date = parser.parse(match.group(1))
                pnl_time = mdates.date2num(log_date)
                pnl_value = float(match.group(2))
                accumulated_pnl += pnl_value  # Accumulate PNL
                pnl_times.append(pnl_time)
                pnl_values.append(accumulated_pnl)  # Use accumulated PNL value
                real_pnl_values.append(pnl_value)  # Store real PNL value

        if pnl_times:
            self.ax.plot_date(pnl_times, pnl_values, linestyle='-', label='PNL', color='blue', linewidth=1.5)
            for time, value, real_pnl in zip(pnl_times, pnl_values, real_pnl_values):
                self.ax.text(time, value, f"{value:.2f}\n{real_pnl:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)

        roe_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROE: ([-\d.]+)%")
        roe_times = []
        roe_values = []
        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = roe_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_time = mdates.date2num(log_date)
                        roe_value = float(match.group(2))
                        roe_times.append(roe_time)
                        roe_values.append(roe_value)
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Log file: {str(e)}\n")

        if roe_times:
            self.ax.plot_date(roe_times, roe_values, 'g-', label='ROE', linewidth=1.5)  # Line for ROE
            latest_roe_time = roe_times[-1]
            latest_roe_value = roe_values[-1]
            self.ax.plot_date(latest_roe_time, latest_roe_value, 'go')  # Marker for the latest ROE entry
            self.ax.text(latest_roe_time, latest_roe_value, f" {latest_roe_value:.2f}%", ha='left', va='bottom', fontsize=8, rotation=45)



        # New section for ROE_Close
        roe_close_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROICloseLevel_Valve_ Modification_BUY_ON_START: ([-\d.]+)")
        roe_close_times = []
        roe_close_values = []
        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = roe_close_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_close_time = mdates.date2num(log_date)
                        roe_close_value = float(match.group(2))
                        roe_close_times.append(roe_close_time)
                        roe_close_values.append(roe_close_value)
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Close Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Close Log file: {str(e)}\n")

        if roe_close_times:
            self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)  # Line for ROE Close
            latest_roe_close_time = roe_close_times[-1]
            latest_roe_close_value = roe_close_values[-1]
            self.ax.plot_date(latest_roe_close_time, latest_roe_close_value, 'ro')  # Marker for the latest ROE Close entry
            self.ax.text(latest_roe_close_time, latest_roe_close_value, f" {latest_roe_close_value:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)


        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper left')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        self.ax.xaxis.set_tick_params(rotation=45)
        self.ax.grid(True)
        self.canvas.draw()
        

    def plot_roe_close_graph(self):
        filename = 'HODL_INFO.log'
        try:
            with open(filename, 'r') as f:
                log_contents = f.readlines()
                roe_close_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROICloseLevel_Valve_ Modification_BUY_ON_START: ([-\d.]+)")
                roe_close_times = []
                roe_close_values = []
                for line in log_contents:
                    match = roe_close_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_close_time = mdates.date2num(log_date)
                        roe_close_value = float(match.group(2))
                        roe_close_times.append(roe_close_time)
                        roe_close_values.append(roe_close_value)

                self.ax.clear()
                if roe_close_times:
                    self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)
                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('ROE Close')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
                    self.ax.xaxis.set_tick_params(rotation=45)
                    self.ax.grid(True)
                else:
                    self.ax.text(0.5, 0.5, 'No ROE Close Data Available', ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Close Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Close Log file: {str(e)}\n")



        if roe_close_times:
            self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)

        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper left')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        self.ax.xaxis.set_tick_params(rotation=45)
        self.ax.grid(True)
        self.canvas.draw()



    def plot_combined_graph_plotShow(self):
        plt.clf()  # Clear the current figure
        
        fig, ax1 = plt.subplots()  # Create a new figure with a single subplot


        pnl_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*PNL=([-\d.]+)")
        pnl_times = []
        pnl_values = []
        real_pnl_values = []  # Real PNL values at each point
        accumulated_pnl = 0.0  # Accumulated PNL over time
        for line in self.all_log_entries:
            match = pnl_pattern.search(line)
            if match:
                log_date = parser.parse(match.group(1))
                pnl_time = mdates.date2num(log_date)
                pnl_value = float(match.group(2))
                accumulated_pnl += pnl_value  # Accumulate PNL
                pnl_times.append(pnl_time)
                pnl_values.append(accumulated_pnl)  # Use accumulated PNL value
                real_pnl_values.append(pnl_value)  # Store real PNL value

        if pnl_times:
            ax1.plot_date(pnl_times, pnl_values, linestyle='-', label='PNL', color='blue', linewidth=1.5)
            for time, value, real_pnl in zip(pnl_times, pnl_values, real_pnl_values):
                ax1.text(time, value, f"{value:.2f}\n{real_pnl:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)




        ax1.set_xlabel('Time')
        ax1.set_ylabel('PNL', color='blue')  # Set ylabel color to blue for PNL / ROE
        ax1.legend(loc='upper right')
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        ax1.xaxis.set_tick_params(rotation=45)

        
        



        pos_size_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*Pos_Size: ([-\d.]+)")
        pos_size_times = []
        pos_size_values = []


        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = pos_size_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        pos_size_time = mdates.date2num(log_date)
                        pos_size_value = float(match.group(2))
                        pos_size_times.append(pos_size_time)
                        pos_size_values.append(pos_size_value)

        except FileNotFoundError:
            self.scroll.insert(tk.END, "PosSize Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading PosSize Log file: {str(e)}\n")




        if pos_size_times:
            # Determine line colors based on the sign of PosSize values
            #line_colors = self.determine_line_colors(pos_size_values)
            ax3 = ax1.twinx()  # Create a twin Axes sharing the xaxis
            # Plot the first point to start the line
            # ax3.plot_date(pos_size_times[:1], pos_size_values[:1], '-', color=line_colors[0][0], label='PosSize', linewidth=0.25)



            ax3.plot_date(pos_size_times, pos_size_values, 'magenta', label='PosSize', linewidth=0.5)
            pos_size_times = pos_size_times[-1]
            pos_size_values = pos_size_values[-1]

            ax3.plot_date(pos_size_times, pos_size_values, 'mo')  # Marker for the latest ROE Close entry
            ax3.text(pos_size_times, pos_size_values, f" {pos_size_values:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)


        # Set the scale for ROE and ROE Close


        ax3.set_xlabel('pos_size_times')
      



        ax3.spines["right"].set_position(("outward", 50))  # Increase the distance
        ax3.set_ylabel('PosSize', color='magenta')
        ax3.legend(loc='upper left')
        ax3.tick_params(axis='y', labelcolor='magenta')
        ax3.spines["right"].set_visible(True)
        ax3.spines["right"].set_edgecolor('orange')

        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        ax3.xaxis.set_tick_params(rotation=45)
        ax3.grid(True, which='both',  linewidth=0.5, color='orange')  # Set a different grid color for ax3




        # New section for ROE_Close
        roe_close_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROICloseLevel_Valve_ Modification_BUY_ON_START: ([-\d.]+)")
        roe_close_times = []
        roe_close_values = []
        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = roe_close_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_close_time = mdates.date2num(log_date)
                        roe_close_value = float(match.group(2))
                        roe_close_times.append(roe_close_time)
                        roe_close_values.append(roe_close_value)
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Close Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Close Log file: {str(e)}\n")

        # Plot ROE Close
        if roe_close_times:
            ax4 = ax1.twinx()  # Create a twin Axes sharing the xaxis

            ax4.plot_date(roe_close_times, roe_close_values, 'g-', label='ROE Close', linewidth=1.0)  
            latest_roe_close_time = roe_close_times[-1]
            latest_roe_close_value = roe_close_values[-1]
            ax4.plot_date(latest_roe_close_time, latest_roe_close_value, 'go')  # Marker for the latest ROE Close entry
            ax4.text(latest_roe_close_time, latest_roe_close_value, f" {latest_roe_close_value:.2f}", ha='left', va='bottom', fontsize=8, rotation=45)

        ax4.set_xlabel('Time')
        ax4.legend(loc='upper center')
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        ax4.xaxis.set_tick_params(rotation=45)
        ax4.grid(True, linestyle='-', linewidth=0.5, color='black')  # Set a different grid color for ax3
        


        roe_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROE: ([-\d.]+)%")
        roe_times = []
        roe_values = []
        
        try:
            with open('HODL_INFO.log', 'r') as f:
                log_contents = f.readlines()
                for line in log_contents:
                    match = roe_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_time = mdates.date2num(log_date)
                        roe_value = float(match.group(2))
                        roe_times.append(roe_time)
                        roe_values.append(roe_value)
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Log file: {str(e)}\n")

        # Plot ROE
        if roe_times:

            ax4.plot_date(roe_times, roe_values, 'darkgreen', linestyle='-', label='ROE', linewidth=0.65)  
            latest_roe_time = roe_times[-1]
            latest_roe_value = roe_values[-1]
            ax4.plot_date(latest_roe_time, latest_roe_value, 'go')  # Marker for the latest ROE entry
            ax4.text(latest_roe_time, latest_roe_value, f" {latest_roe_value:.2f}%", ha='left', va='bottom', fontsize=8, rotation=45)



        ax4.set_ylabel('ROE / ROE Close', color='green')  # Set ylabel color to red for ROE / ROE Close

        # Combine ROE and ROE Close data to set proper ylim
        combined_roe_values = roe_values + roe_close_values
        ax4.set_ylim(min(combined_roe_values), max(combined_roe_values) )

        ax4.tick_params(axis='y', labelcolor='green')
        ax4.spines["right"].set_edgecolor('green')



        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        ax4.xaxis.set_tick_params(rotation=45)
        ax4.grid(True, which='both',  linewidth=0.5, color='green')  # Set a different grid color for ax3




        # Show the plot
        plt.show()
        
 

 
 
    def plot_roe_close_graph(self):
        filename = 'HODL_INFO.log'
        try:
            with open(filename, 'r') as f:
                log_contents = f.readlines()
                roe_close_pattern = re.compile(r"(\d{2}-\w{3}-\d{2} \d{2}:\d{2}:\d{2}).*ROICloseLevel_Valve_ Modification_BUY_ON_START: ([-\d.]+)")
                roe_close_times = []
                roe_close_values = []
                for line in log_contents:
                    match = roe_close_pattern.search(line)
                    if match:
                        log_date = parser.parse(match.group(1))
                        roe_close_time = mdates.date2num(log_date)
                        roe_close_value = float(match.group(2))
                        roe_close_times.append(roe_close_time)
                        roe_close_values.append(roe_close_value)

                self.ax.clear()
                if roe_close_times:
                    self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)
                    self.ax.set_xlabel('Time')
                    self.ax.set_ylabel('ROE Close')
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
                    self.ax.xaxis.set_tick_params(rotation=45)
                    self.ax.grid(True)
                else:
                    self.ax.text(0.5, 0.5, 'No ROE Close Data Available', ha='center', va='center', transform=self.ax.transAxes)
                self.canvas.draw()
        except FileNotFoundError:
            self.scroll.insert(tk.END, "ROE Close Log file not found.\n")
        except Exception as e:
            self.scroll.insert(tk.END, f"Error reading ROE Close Log file: {str(e)}\n")



        if roe_close_times:
            self.ax.plot_date(roe_close_times, roe_close_values, 'r-', label='ROE Close', linewidth=1.5)

        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.legend(loc='upper left')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%y %H:%M'))
        self.ax.xaxis.set_tick_params(rotation=45)
        self.ax.grid(True)
        self.canvas.draw()






root = tk.Tk()
app = LogAnalyzer(root)
root.mainloop()

