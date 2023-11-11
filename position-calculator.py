import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser


def add_entry():
    entry_frame = tk.Frame(entry_container)
    entry_frame.pack(fill='x', padx=5, pady=5)
    entry_price_var = tk.DoubleVar()
    entry_prices_vars.append(entry_price_var)
    tk.Entry(entry_frame, textvariable=entry_price_var).pack(side='left', fill='x', expand=True)
    remove_button = tk.Button(entry_frame, text="X", command=lambda: remove_widget(entry_frame, entry_price_var))
    remove_button.pack(side='left', padx=5)


def remove_widget(widget, var):
    widget.destroy()
    if var in entry_prices_vars:
        entry_prices_vars.remove(var)


def open_link(url):
    webbrowser.open_new_tab(url)


def calculate_positions():
    try:
        account_balance = balance_var.get()
        risk_percentage = risk_var.get()
        leverage = leverage_var.get()
        stop_loss = stop_loss_var.get()

        risk_type = risk_type_var.get()
        position_sizes = []
        total_loss_if_sl_hits = 0

        if risk_type == 'Evenly Divided Entry':
            if len(entry_prices_vars) == 0:
                messagebox.showinfo("Info", "No entry prices provided.")
                return

            average_entry_price = sum(entry_price_var.get() for entry_price_var in entry_prices_vars) / len(entry_prices_vars)
            total_risk_amount = (risk_percentage / 100) * account_balance
            risk_per_unit = abs(average_entry_price - stop_loss)
            total_units = total_risk_amount / risk_per_unit
            units_per_entry = total_units / len(entry_prices_vars)
            position_size = units_per_entry * average_entry_price
            position_sizes = [position_size] * len(entry_prices_vars)
            total_loss_if_sl_hits = total_risk_amount

        elif risk_type == 'Separate Risk Per Entry':
            for entry_price_var in entry_prices_vars:
                entry_price = entry_price_var.get()
                risk_per_unit = abs(entry_price - stop_loss)
                total_risk_amount = (risk_percentage / 100) * account_balance
                units = total_risk_amount / risk_per_unit
                position_size = units * entry_price
                position_sizes.append(position_size)
                individual_loss = units * risk_per_unit
                total_loss_if_sl_hits += individual_loss

        # Display results
        result_text = ""
        for i, size in enumerate(position_sizes, start=1):
            result_text += f"Entry {i}: ${size:.2f}"
            if cornix_mode.get():
                cornix_size = size / leverage
                result_text += f" (Cornix: ${cornix_size:.2f})"
            result_text += "\n"

        total_position_size = sum(position_sizes)

        result_text += f"\nTotal Position Size: ${total_position_size:.2f}"

        if cornix_mode.get():
            cornix_total_size = total_position_size / leverage
            result_text += f" (Cornix: ${cornix_total_size:.2f})"

        result_text += "\n"

        result_text += f"Loss if SL hits: ${total_loss_if_sl_hits:.2f}"

        position_size_result['text'] = result_text

    except Exception as e:
        messagebox.showerror("Error", "An error occurred. Please check your inputs.")


# Initialize variables
entry_prices_vars = []

# Create main window
root = tk.Tk()
root.title("Position Size and Profit Calculator")
root.geometry('400x800')
cornix_mode = tk.BooleanVar()

# Info Section
info_frame = tk.LabelFrame(root, text="Info")
info_frame.pack(fill='x', padx=10, pady=5)

balance_var = tk.DoubleVar()
risk_var = tk.DoubleVar(value=1)
leverage_var = tk.DoubleVar(value=1)

# Account Balance, Risk Percentage, and Leverage
tk.Label(info_frame, text="Account Balance ($):").grid(row=0, column=0, padx=5, pady=5)
balance_entry = tk.Entry(info_frame, textvariable=balance_var)
balance_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(info_frame, text="Risk Percentage (%):").grid(row=1, column=0, padx=5, pady=5)
risk_entry = tk.Entry(info_frame, textvariable=risk_var)
risk_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(info_frame, text="Leverage:").grid(row=2, column=0, padx=5, pady=5)
leverage_entry = tk.Entry(info_frame, textvariable=leverage_var)
leverage_entry.grid(row=2, column=1, padx=5, pady=5)

# Settings Section
settings_frame = tk.LabelFrame(root, text="Settings")
settings_frame.pack(fill='x', padx=10, pady=5)

# Cornix Mode and Entry Type
tk.Label(settings_frame, text="Cornix Mode:").grid(row=0, column=0, padx=5, pady=5)
cornix_toggle = ttk.Checkbutton(settings_frame, text='On/Off', variable=cornix_mode)
cornix_toggle.grid(row=0, column=1, padx=5, pady=5)

risk_type_var = tk.StringVar()
risk_type_options = ['Evenly Divided Entry', 'Separate Risk Per Entry']
tk.Label(settings_frame, text="Entry Type:").grid(row=1, column=0, padx=5, pady=5)
risk_type_menu = ttk.Combobox(settings_frame, textvariable=risk_type_var, values=risk_type_options)
risk_type_menu.grid(row=1, column=1, padx=5, pady=5)
risk_type_menu.current(0)

# Stop Loss Section
stop_loss_var = tk.DoubleVar()
stop_loss_frame = tk.LabelFrame(root, text="Stop Loss")
stop_loss_frame.pack(fill='x', padx=10, pady=5)

tk.Label(stop_loss_frame, text="Stop Loss ($):").grid(row=0, column=0, padx=5, pady=5)
stop_loss_entry = tk.Entry(stop_loss_frame, textvariable=stop_loss_var)
stop_loss_entry.grid(row=0, column=1, padx=5, pady=5)

# Entry Points Section
entry_container = tk.LabelFrame(root, text="Entry Points")
entry_container.pack(fill='both', expand=True, padx=10, pady=5)
add_entry_button = tk.Button(entry_container, text="Add Entry Point", command=add_entry)
add_entry_button.pack(side='top', padx=5, pady=5)

# Calculate Button
calculate_button = tk.Button(root, text="Calculate", command=calculate_positions)
calculate_button.pack(side='top', fill='x', padx=10, pady=10)

# Calculations Result
results_frame = tk.LabelFrame(root, text="Results")  # Using LabelFrame for the border
results_frame.pack(side='top', expand=True, fill='both', padx=10, pady=5)

position_size_result = tk.Label(results_frame, text="Position Sizes:")
position_size_result.pack(side='top', fill='x', padx=5, pady=5)


# Links Section
links_frame = tk.Frame(root)
links_frame.pack(side='bottom', fill='x', anchor='s', padx=10, pady=20)

source_code_link = tk.Label(links_frame, text="Source Code", fg="blue", cursor="hand2")
source_code_link.pack(side='left', padx=10, pady=5)
source_code_link.bind("<Button-1>", lambda e: open_link("https://github.com/sbjohansen/position-size-calculator"))

cornix_link = tk.Label(links_frame, text="Cornix", fg="blue", cursor="hand2")
cornix_link.pack(side='left', padx=10, pady=5)
cornix_link.bind("<Button-1>", lambda e: open_link("https://dashboard.cornix.io/register/896E5A8B"))

root.mainloop()
