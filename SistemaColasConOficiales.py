import tkinter as tk
from tkinter import ttk
import random

class CustomerQueueSimulation:
    def __init__(self):
        self.sistema = SistemaColas()
        self.sistema.oficiales = [OficialAtencionCliente(f"Oficial{i + 1}") for i in range(3)]

    def run_simulation(self):
        for _ in range(10):
            self.sistema.llegada_cliente()
            self.sistema.asignar_oficial()

class SistemaColas:
    def __init__(self):
        self.cola = []
        self.oficiales = []
        self.clientes_atendidos = 0

    def llegada_cliente(self):
        ticket = random.randint(1, 100)
        prioridad = random.choice(['alta', 'media', 'baja'])
        self.cola.append((ticket, prioridad))

    def asignar_oficial(self):
        if self.cola:
            ticket, prioridad = self.cola.pop(0)
            oficial = random.choice(self.oficiales)
            oficial.atender_cliente(ticket, prioridad)
            self.clientes_atendidos += 1

    def informe_rendimiento(self):
        total_clientes = self.clientes_atendidos
        promedio_por_oficial = total_clientes / len(self.oficiales)
        return f"Total de clientes atendidos: {total_clientes}\n" \
               f"Promedio de clientes por oficial: {promedio_por_oficial}"

class OficialAtencionCliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes_atendidos = 0

    def atender_cliente(self, ticket, prioridad):
        print(f"{self.nombre} atiende al cliente con ticket {ticket} (Prioridad: {prioridad})")
        self.clientes_atendidos += 1

    def informe_rendimiento(self):
        return f"{self.nombre} atendió a {self.clientes_atendidos} clientes"

class SimuladorInterfaz(tk.Tk):
    def __init__(self):
        super().__init__()

        self.sistema = SistemaColas()
        self.sistema.oficiales = [OficialAtencionCliente("Oficial1"), OficialAtencionCliente("Oficial2"), OficialAtencionCliente("Oficial3")]

        self.title("Simulador de Colas - Teoria de la Simulacion LV")
        self.resizable(0, 0)
        self.geometry("800x400")

        # Officials Entry
        self.oficiales_label = tk.Label(self, text="Número de Oficiales:", font=("Poppins", 12, "bold"))
        self.oficiales_label.pack(pady=5)

        self.oficiales_entry = tk.Entry(self, font=("Poppins", 12))
        self.oficiales_entry.pack(pady=5)

        self.btn_agregar_oficiales = tk.Button(self, text="Agregar Oficiales", command=self.agregar_oficiales, bg="blue", fg="white", font=("Poppins", 12))
        self.btn_agregar_oficiales.pack(pady=5)

        # Remove Officials Entry
        self.remover_oficiales_label = tk.Label(self, text="Número de Oficiales a Eliminar:", font=("Poppins", 12, "bold"))
        self.remover_oficiales_label.pack(pady=5)

        self.remover_oficiales_entry = tk.Entry(self, font=("Poppins", 12))
        self.remover_oficiales_entry.pack(pady=5)

        self.btn_remover_oficiales = tk.Button(self, text="Eliminar Oficiales", command=self.remover_oficiales, bg="red", fg="white", font=("Poppins", 12))
        self.btn_remover_oficiales.pack(pady=5)

        # Simulation Button
        self.btn_simular = tk.Button(self, text="Simular", command=self.simular, bg="green", fg="white", font=("Poppins", 12))
        self.btn_simular.pack(pady=5)

        # Results Display
        self.resultado_text = tk.Text(self, wrap=tk.WORD, height=10, width=50)
        self.resultado_text.pack(side=tk.LEFT, padx=10)

        # Customer Queue Display
        self.cola_frame = ttk.Frame(self)
        self.cola_frame.pack(side=tk.LEFT, padx=10)

        self.cola_label = tk.Label(self.cola_frame, text="Cola de Clientes", font=("Poppins", 12, "bold"))
        self.cola_label.pack()

        self.cola_tree = ttk.Treeview(self.cola_frame, columns=("Ticket", "Prioridad"), show="headings", height=5)
        self.cola_tree.heading("Ticket", text="Ticket")
        self.cola_tree.heading("Prioridad", text="Prioridad")
        self.cola_tree.column("Ticket", width=100)
        self.cola_tree.column("Prioridad", width=100)
        self.cola_tree.pack()
        self.configure(bg="lightblue")

    def simular(self):
        # Clear widgets
        self.resultado_text.delete(1.0, tk.END)
        self.cola_tree.delete(*self.cola_tree.get_children())

        # Simulation of customer arrivals during a day
        for _ in range(10):
            self.sistema.llegada_cliente()
            self.actualizar_cola()

        # Simulation of service during a day
        for _ in range(10):
            self.sistema.asignar_oficial()
            self.actualizar_cola()

        # Update the result label
        resultado = self.sistema.informe_rendimiento()
        for oficial in self.sistema.oficiales:
            resultado += "\n" + oficial.informe_rendimiento()

        self.resultado_text.insert(tk.END, resultado)

    def actualizar_cola(self):
        for ticket, prioridad in self.sistema.cola:
            color = "red" if prioridad == "alta" else "green" if prioridad == "baja" else "yellow"
            self.cola_tree.insert("", "end", values=(ticket, prioridad), tags=(color,))
            self.cola_tree.tag_configure(color, background=color)

    def agregar_oficiales(self):
        try:
            num_oficiales = int(self.oficiales_entry.get())
            nuevos_oficiales = [OficialAtencionCliente(f"Oficial{i + 1}") for i in range(len(self.sistema.oficiales), len(self.sistema.oficiales) + num_oficiales)]
            self.sistema.oficiales.extend(nuevos_oficiales)
            self.resultado_text.insert(tk.END, f"Agregados {num_oficiales} nuevos oficiales.\n")
        except ValueError:
            self.resultado_text.insert(tk.END, "Ingrese un número válido de oficiales.\n")

    def remover_oficiales(self):
        try:
            num_oficiales = int(self.remover_oficiales_entry.get())
            if num_oficiales > len(self.sistema.oficiales):
                self.resultado_text.insert(tk.END, "No hay suficientes oficiales para eliminar.\n")
            else:
                oficiales_eliminados = self.sistema.oficiales[-num_oficiales:]
                self.sistema.oficiales = self.sistema.oficiales[:-num_oficiales]
                self.resultado_text.insert(tk.END, f"Eliminados {num_oficiales} oficiales: {', '.join([oficial.nombre for oficial in oficiales_eliminados])}.\n")
        except ValueError:
            self.resultado_text.insert(tk.END, "Ingrese un número válido de oficiales a eliminar.\n")


if __name__ == "__main__":
    app = SimuladorInterfaz()
    app.mainloop()
