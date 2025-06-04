import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Despertador:
    def __init__(self, root, get_time_func):
        self.root = root
        self.get_time = get_time_func
        self.frame = tk.Frame(self.root, bg='#001633')
        self.alarmas = []
        self.alarmas_mostradas = set()

        # Hora actual
        self.lbl_hora_actual = tk.Label(self.frame, font=("Arial", 40, "bold"), fg="#00BFFF", bg="#001633")
        self.lbl_hora_actual.pack(pady=10)

        # Selector de hora/minutos y AM/PM
        selector_frame = tk.Frame(self.frame, bg='#001633')
        selector_frame.pack(pady=10)

        self.hour_var = tk.StringVar(value="07")
        self.minute_var = tk.StringVar(value="00")
        self.ampm_var = tk.StringVar(value="AM")

        self.hour_spin = tk.Spinbox(selector_frame, from_=1, to=12, width=5, font=("Arial", 18),
                                    textvariable=self.hour_var, format="%02.0f", state="readonly")
        self.minute_spin = tk.Spinbox(selector_frame, from_=0, to=59, width=5, font=("Arial", 18),
                                      textvariable=self.minute_var, format="%02.0f", state="readonly")
        self.ampm_spin = tk.Spinbox(selector_frame, values=("AM", "PM"), width=5, font=("Arial", 18),
                                    textvariable=self.ampm_var, state="readonly")

        self.hour_spin.pack(side="left", padx=5)
        self.minute_spin.pack(side="left", padx=5)
        self.ampm_spin.pack(side="left", padx=5)

        # Botón guardar
        tk.Button(self.frame, text="Guardar", command=self.guardar_alarma,
                  font=("Arial", 14), bg="#00BFFF", fg="white").pack(pady=10)

        # Lista de alarmas
        self.lista_frame = tk.Frame(self.frame, bg='#001633')
        self.lista_frame.pack(pady=10)

    def mostrar(self):
        self.frame.pack(pady=20)
        self.actualizar_hora_actual()

    def ocultar(self):
        self.frame.pack_forget()

    def actualizar_hora_actual(self):
        ahora = self.get_time()
        self.lbl_hora_actual.config(text=ahora.strftime("%I:%M:%S %p"))
        self.frame.after(1000, self.actualizar_hora_actual)

    def guardar_alarma(self):
        hora = self.hour_var.get()
        minuto = self.minute_var.get()
        ampm = self.ampm_var.get()
        hora_str = f"{int(hora):02}:{int(minuto):02} {ampm}"

        var_activa = tk.BooleanVar(value=True)

        frame_alarma = tk.Frame(self.lista_frame, bg='#001633')
        frame_alarma.pack(anchor='w', pady=2)

        tk.Label(frame_alarma, text=hora_str, font=("Arial", 14), fg="white", bg="#001633").pack(side="left", padx=10)
        tk.Checkbutton(frame_alarma, variable=var_activa, text="Activar", fg="white", bg="#001633",
                       font=("Arial", 12), selectcolor="#001633", activebackground="#001633",
                       activeforeground="white").pack(side="left")

        self.alarmas.append((hora_str, var_activa))

    def verificar_alarma(self, ahora):
        hora_actual = ahora.strftime("%I:%M %p")
        for hora_str, activa_var in self.alarmas:
            if activa_var.get() and hora_str == hora_actual and hora_str not in self.alarmas_mostradas:
                self.alarmas_mostradas.add(hora_str)
                desactivar = messagebox.askyesno("Alarma", f"¡Despierta! Son las {hora_str}\n¿Deseás desactivar esta alarma?")
                if desactivar:
                    activa_var.set(False)
                self.root.after(60000, lambda h=hora_str: self.alarmas_mostradas.discard(h))  # Limpia la marca tras 1 min
