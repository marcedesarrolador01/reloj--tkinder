import tkinter as tk
import threading
import time

class Cronometro:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.segundos = 0
        self.historial_tiempos = []

        # Etiqueta principal
        self.label = tk.Label(root, text="00:00:00", font=("Arial", 40, "bold"), fg='#00FF00', bg='#001633')

        # Botones
        self.frame_botones = tk.Frame(root, bg='#001633')
        self.boton_iniciar = tk.Button(self.frame_botones, text="Iniciar", command=self.toggle, bg='#007BFF', fg='white', font=("Arial", 12, "bold"), width=10)
        self.boton_iniciar.pack(side='left', padx=5)

        self.boton_resetear = tk.Button(self.frame_botones, text="Resetear", command=self.resetear, bg='#FFD700', fg='black', font=("Arial", 12, "bold"), width=10)
        self.boton_resetear.pack(side='left', padx=5)

        self.boton_stop = tk.Button(self.frame_botones, text="Stop", command=self.marcar_tiempo, bg='red', fg='white', font=("Arial", 12, "bold"), width=10)
        self.boton_stop.pack(side='left', padx=5)

        # Lista de tiempos registrados
        self.lista_tiempos = tk.Listbox(root, font=("Arial", 12), height=5, bg="#001633", fg="white", highlightthickness=0, borderwidth=0)

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.boton_iniciar.config(text="Pausar")
            threading.Thread(target=self.run, daemon=True).start()
        else:
            self.boton_iniciar.config(text="Iniciar")

    def run(self):
        while self.running:
            time.sleep(1)
            self.segundos += 1
            self.actualizar_label()

    def actualizar_label(self):
        h, s = divmod(self.segundos, 3600)
        m, s = divmod(s, 60)
        self.label.config(text=f"{h:02}:{m:02}:{s:02}")

    def resetear(self):
        self.segundos = 0
        self.actualizar_label()
        self.lista_tiempos.delete(0, tk.END)
        self.historial_tiempos.clear()

    def marcar_tiempo(self):
        if self.segundos > 0:
            h, s = divmod(self.segundos, 3600)
            m, s = divmod(s, 60)
            tiempo = f"{h:02}:{m:02}:{s:02}"
            self.historial_tiempos.append(tiempo)
            self.lista_tiempos.insert(tk.END, tiempo)
        self.running = False
        self.boton_iniciar.config(text="Iniciar")

    def mostrar(self):
        self.label.pack(pady=20)
        self.frame_botones.pack(pady=10)
        self.lista_tiempos.pack(pady=10)

    def ocultar(self):
        self.label.pack_forget()
        self.frame_botones.pack_forget()
        self.lista_tiempos.pack_forget()
