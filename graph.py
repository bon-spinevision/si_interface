import customtkinter as ctk
import globals
import asyncio
import os

def button_callback():
    print(f"button pressed {globals.force}")
    label.configure(text=f"Force value: {globals.force} Newtons")

async def graph():
    app = ctk.CTk()
    app.title("Smart Instrument Interface")
    if (os.path.isfile("logo.ico")):
        app.iconbitmap("logo.ico")
        print("ICO FOUND YYYYYY")
    app.geometry("400x150")
    app.grid_rowconfigure((0, 1, 2), weight=1)
    app.grid_columnconfigure((0, 1, 2), weight=1)

    global label
    label = ctk.CTkLabel(app, text=f"Force value: {globals.force} Newtons", font=("Arial", 16))
    label.grid(row=1, column=1, padx=20, pady=20)

    global label_voltage
    label_voltage = ctk.CTkLabel(app, text=f"VOLTAGE value: {globals.force} mV", font=("Arial", 16))
    label_voltage.grid(row=2, column=1, padx=20, pady=20)

    button = ctk.CTkButton(app, text="OFF", command=button_callback, fg_color="red", width=40, height=30, corner_radius=30, hover_color="red")
    button.grid(row=1, column=0, padx=20, pady=20)
    
    previous_force = globals.force
    previous_is_connected = globals.is_connected
    previous_voltage = globals.voltage
    running = True

    def on_close():
        nonlocal running
        running = False
        print("Window closed by user")

    app.protocol("WM_DELETE_WINDOW", on_close)

    try:
        while running:
            if (previous_is_connected != globals.is_connected):
                if (globals.is_connected):
                    button.configure(fg_color="green", hover_color="green", text="ON")
                else:
                    button.configure(fg_color="red", hover_color="red", text="OFF")
                previous_is_connected = globals.is_connected

            if globals.force != previous_force:
                previous_force = globals.force
                label.configure(text=f"Force value: {globals.force} Newtons")
            if (globals != previous_voltage):
                previous_voltage = globals.voltage
                label_voltage.configure(text=f"Voltage value: {globals.voltage} mV")

            if app.winfo_exists():
                app.update()
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Graph process stopped: {e}")
    finally:
        if app.winfo_exists():
            print("Closing GUI...")
            app.destroy()
        else:
            print("GUI already destroyed")