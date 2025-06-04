import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pytz
import threading
import time

# --- Variables globales ---
cronometro_segundos = 0
cronometro_running = False
alarm_time = None
alarm_set = False
selected_timezone = 'UTC-03:00'

# --- Mapeo de zonas horarias ---
timezone_map = {
    'UTC-06:00': 'Etc/GMT+6',
    'UTC-05:00': 'Etc/GMT+5',
    'UTC-03:00': 'Etc/GMT+3',
    'UTC+00:00': 'Etc/GMT-0',
    'UTC+01:00': 'Etc/GMT-1',
    'UTC+03:00': 'Etc/GMT-3'
}

# --- Funciones generales ---
def get_time():
    tz = pytz.timezone(timezone_map[selected_timezone_var.get()])
    return datetime.now(tz)

# --- Reloj ---
def update_clock():
    global alarm_set
    now = get_time()
    time_label.config(text=now.strftime("%I:%M:%S %p"))

    if alarm_set and alarm_time:
        diff = alarm_time - now
        if diff.total_seconds() <= 0:
            alarm_set = False
            messagebox.showinfo("¡Despertador!", "⏰ ¡Hora de levantarse!")
            alarm_status.config(text="")
        else:
            mins = int(diff.total_seconds() // 60)
            alarm_status.config(text=f"Faltan {mins} minutos para que suene el despertador")

    root.after(1000, update_clock)

# --- Cronómetro ---
def toggle_cronometro():
    global cronometro_running
    cronometro_running = not cronometro_running
    if cronometro_running:
        start_btn.config(text="Pausar")
        threading.Thread(target=run_cronometro, daemon=True).start()
    else:
        start_btn.config(text="Iniciar")

def run_cronometro():
    global cronometro_segundos
    while cronometro_running:
        time.sleep(1)
        cronometro_segundos += 1
        update_cronometro_label()

def reset_cronometro():
    global cronometro_segundos
    cronometro_segundos = 0
    update_cronometro_label()

def stop_cronometro():
    global cronometro_running
    cronometro_running = False
    start_btn.config(text="Iniciar")

def update_cronometro_label():
    mins, secs = divmod(cronometro_segundos, 60)
    hrs, mins = divmod(mins, 60)
    cronometro_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")

# --- Despertador ---
def set_alarm():
    global alarm_time, alarm_set
    try:
        hour = int(hour_entry.get())
        minute = int(minute_entry.get())
        ampm = ampm_entry.get()

        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        now = get_time()
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if alarm_time < now:
            alarm_time += timedelta(days=1)

        alarm_set = True
        messagebox.showinfo("Despertador activado", f"Programado para las {alarm_time.strftime('%I:%M %p')}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo configurar el despertador: {e}")

# --- GUI Principal ---
root = tk.Tk()
root.title("TechKinder Clock")
root.geometry("400x500")
root.config(bg='#001633')

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --- Pestaña Reloj ---
clock_tab = tk.Frame(notebook, bg='#001633')
notebook.add(clock_tab, text='Reloj')

selected_timezone_var = tk.StringVar(value=selected_timezone)
ttk.Combobox(clock_tab, values=list(timezone_map.keys()), textvariable=selected_timezone_var, font=("Arial", 14)).pack(pady=10)

time_label = tk.Label(clock_tab, font=("Arial", 40), fg='cyan', bg='#001633')
time_label.pack(pady=20)

# --- Pestaña Cronómetro ---
cronometro_tab = tk.Frame(notebook, bg='#001633')
notebook.add(cronometro_tab, text='Cronómetro')

cronometro_label = tk.Label(cronometro_tab, font=("Arial", 30), fg='green', bg='#001633')
cronometro_label.pack(pady=20)

btn_frame = tk.Frame(cronometro_tab, bg='#001633')
btn_frame.pack()

start_btn = tk.Button(btn_frame, text="Iniciar", command=toggle_cronometro)
start_btn.pack(side='left', padx=5)
tk.Button(btn_frame, text="Resetear", command=reset_cronometro).pack(side='left', padx=5)
tk.Button(btn_frame, text="Stop", command=stop_cronometro).pack(side='left', padx=5)

# --- Pestaña Despertador ---
alarm_tab = tk.Frame(notebook, bg='#001633')
notebook.add(alarm_tab, text='Despertador')

alarm_status = tk.Label(alarm_tab, font=("Arial", 14), fg='white', bg='#001633')
alarm_status.pack(pady=10)

alarm_frame = tk.Frame(alarm_tab, bg='#001633')
alarm_frame.pack()

tk.Label(alarm_frame, text="Hora:", bg='#001633', fg='white').pack(side='left')
hour_entry = ttk.Combobox(alarm_frame, values=[f"{i:02}" for i in range(1, 13)], width=3)
hour_entry.set("07")
hour_entry.pack(side='left')

tk.Label(alarm_frame, text="Min:", bg='#001633', fg='white').pack(side='left')
minute_entry = ttk.Combobox(alarm_frame, values=[f"{i:02}" for i in range(60)], width=3)
minute_entry.set("00")
minute_entry.pack(side='left')

ampm_entry = ttk.Combobox(alarm_frame, values=["AM", "PM"], width=3)
ampm_entry.set("AM")
ampm_entry.pack(side='left')

tk.Button(alarm_frame, text="Activar", command=set_alarm).pack(side='left', padx=10)

# --- Iniciar el reloj ---
update_clock()
root.mainloop()
