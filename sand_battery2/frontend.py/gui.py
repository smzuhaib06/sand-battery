import tkinter as tk
from tkinter import ttk
import requests
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import time

# Globals for plotting
voltages = []
currents = []
timestamps = []

# URL of the backend (Raspberry Pi hosting FastAPI)
BASE_URL = "http://192.168.67.3:8000"

def send_command(gpio, value):
    try:
        response = requests.post(f"{BASE_URL}/control", data={"gpio": gpio, "value": '1' if value else '0'})
        print(response.json())
    except Exception as e:
        print("Command Error:", e)

def fetch_data():
    while True:
        try:
            sensor = requests.get(f"{BASE_URL}/data").json()

            voltage_var.set(f"Voltage: {sensor['voltage']} V")
            current_var.set(f"Current: {sensor['current']} mA")
            power_var.set(f"Power: {sensor['power']} mW")
            status_var.set(f"Status: {sensor['status']}")

            # Update graph
            voltages.append(sensor['voltage'])
            currents.append(sensor['current'])
            timestamps.append(time.strftime("%H:%M:%S"))
            if len(voltages) > 20:
                voltages.pop(0)
                currents.pop(0)
                timestamps.pop(0)

            update_graph()

        except Exception as e:
            voltage_var.set("Voltage: Error")
            current_var.set("Current: Error")
            power_var.set("Power: Error")
            status_var.set("Status: Error")
        time.sleep(2)

def update_graph():
    ax.clear()
    ax.plot(timestamps, voltages, label="Voltage (V)", color="orange", linewidth=2)
    ax.plot(timestamps, currents, label="Current (mA)", color="blue", linewidth=2)
    ax.legend()
    ax.set_xticklabels(timestamps, rotation=45, ha='right')
    ax.set_title("Live Sensor Data")
    ax.set_xlabel("Time")
    ax.set_ylabel("Values")
    ax.grid(True)
    canvas.draw()

# UI Setup
root = tk.Tk()
root.title("Sand Battery Control Panel")
root.geometry("800x600")

style = ttk.Style()
style.theme_use('clam')

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Sensor Labels
voltage_var = tk.StringVar()
current_var = tk.StringVar()
power_var = tk.StringVar()
status_var = tk.StringVar()

for var in [voltage_var, current_var, power_var, status_var]:
    ttk.Label(frame, textvariable=var, font=('Arial', 12, 'bold')).pack(pady=2)

# Control Buttons
btn_frame = ttk.Frame(frame, padding=10)
btn_frame.pack(pady=10)

ttk.Button(btn_frame, text="Switch to Grid", width=20, command=lambda: send_command("grid", True)).grid(row=0, column=0, padx=10, pady=5)
ttk.Button(btn_frame, text="Switch to Sand Battery", width=20, command=lambda: send_command("sand", True)).grid(row=0, column=1, padx=10, pady=5)
ttk.Button(btn_frame, text="Turn Load ON", width=20, command=lambda: send_command("load", True)).grid(row=1, column=0, padx=10, pady=5)
ttk.Button(btn_frame, text="Activate Heater", width=20, command=lambda: send_command("heater", True)).grid(row=1, column=1, padx=10, pady=5)
ttk.Button(btn_frame, text="Turn All OFF", width=42, command=lambda: [send_command(pin, False) for pin in ["grid", "sand", "load", "heater"]]).grid(row=2, column=0, columnspan=2, pady=10)

# Matplotlib chart
fig, ax = plt.subplots(figsize=(7, 3))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Start background thread for live data
threading.Thread(target=fetch_data, daemon=True).start()

root.mainloop()
