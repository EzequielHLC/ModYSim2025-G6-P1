import tkinter as tk
from tkinter import ttk

from view.von_neuman_view import VonNeumannView
from view.mixed_congruence_view import MixedCongruenceView

class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Programa - Generadores de Números Aleatorios")
        self.root.geometry("900x800")

        # Se usa el widget "Notebook" para la navegación por pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña Von Neumann 
        self.vn_frame = tk.Frame(self.notebook)
        self.notebook.add(self.vn_frame, text="Von Neumann")
        self.von_neumann_view = VonNeumannView(self.vn_frame, self.controller)

        # Pestaña Mixed Congruences 
        self.mc_frame = tk.Frame(self.notebook)
        self.notebook.add(self.mc_frame, text="Congruencias Mixtas")
        self.mixed_congruence_view = MixedCongruenceView(self.mc_frame, self.controller)

    def run(self):
        self.root.mainloop()
