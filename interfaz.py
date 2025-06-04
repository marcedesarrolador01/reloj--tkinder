import tkinter as tk
from tkinter import ttk, messagebox
import pytz
from datetime import datetime

from cronometro import Cronometro
from despertador import Despertador

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("TechKinder Clock")
        self.root.config(bg='#001633')
        self.root.geometry("500x600")

        self.timezones = ['UTC-06:00', 'UTC-05:00', 'UTC-03:00', 'UTC+00:00', 'UTC+01:00', 'UTC+03:00']
        self.selected_timezone = tk.StringVar(value='UTC-03:00')

        self.timezone_map = {
            'UTC-06:00': 'Etc/GMT+6',
            'UTC-05:00': 'Etc/GMT+5',
            'UTC-03:00': 'Etc/GMT+3',
            'UTC+00:00': 'Etc/GMT-0',
            'UTC+01:00': 'Etc/GMT-1',
            'UTC+03:00': 'Etc/GMT-3'
        }

        # Encabezado de navegación
        header = tk.Frame(self.root, bg='#002b66')
        header.pack(fill='x')

        tk.Button(header, text="Reloj", command=self.show_clock,
                  fg='#FFD700', bg='#002b66', font=("Arial", 14, "bold"), border=0).pack(side='left', padx=10, pady=10)
        tk.Button(header, text="Despertador", command=self.show_alarm,
                  fg='white', bg='#002b66', font=("Arial", 14), border=0).pack(side='left', padx=10)
        tk.Button(header, text="Cronómetro", command=self.show_cronometro,
                  fg='white', bg='#002b66', font=("Arial", 14), border=0).pack(side='left', padx=10)

        # === Reloj (hora, segundos, AM/PM en una fila) ===
        self.frame_reloj = tk.Frame(self.root, bg='#001633')
        self.time_label = tk.Label(self.frame_reloj, font=("Arial", 60, "bold"), fg='#00BFFF', bg='#001633')
        self.seconds_label = tk.Label(self.frame_reloj, font=("Arial", 60, "bold"), fg='#FFD700', bg='#001633')
        self.ampm_label = tk.Label(self.frame_reloj, font=("Arial", 30, "bold"), fg='#FFD700', bg='#001633')

        self.time_label.pack(side='left')
        self.seconds_label.pack(side='left', padx=(10, 0))
        self.ampm_label.pack(side='left', padx=(10, 0))

        self.frame_reloj.pack(pady=40)

        # Zona horaria debajo del reloj
        self.timezone_menu = ttk.Combobox(self.root, values=self.timezones,
                                          textvariable=self.selected_timezone, font=("Arial", 14))
        self.timezone_menu.pack(pady=10)

        # Componentes externos
        self.cronometro = Cronometro(self.root)
        self.despertador = Despertador(self.root, self.get_time)

        self.update_clock()

    def get_time(self):
        tz_name = self.timezone_map[self.selected_timezone.get()]
        return datetime.now(pytz.timezone(tz_name))

    def update_clock(self):
        now = self.get_time()
        self.time_label.config(text=now.strftime("%I:%M"))
        self.seconds_label.config(text=now.strftime("%S"))
        self.ampm_label.config(text=now.strftime("%p"))

        self.despertador.verificar_alarma(now)

        self.root.after(1000, self.update_clock)

    def show_clock(self):
        self.frame_reloj.pack(pady=40)
        self.timezone_menu.pack(pady=10)
        self.cronometro.ocultar()
        self.despertador.ocultar()

    def show_cronometro(self):
        self.frame_reloj.pack_forget()
        self.timezone_menu.pack_forget()
        self.cronometro.mostrar()
        self.despertador.ocultar()

    def show_alarm(self):
        self.frame_reloj.pack_forget()
        self.timezone_menu.pack_forget()
        self.cronometro.ocultar()
        self.despertador.mostrar()
