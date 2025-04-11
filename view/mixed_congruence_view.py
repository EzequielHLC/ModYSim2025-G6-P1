import tkinter as tk

class MixedCongruenceView:
    def __init__(self, parent, controller):
        self.controller = controller
        # Se utiliza el mismo fondo claro para uniformidad
        self.frame = tk.Frame(parent, bg="#ECECEC")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # --- Left Frame: Entradas y Botón "Generar" ---
        self.left_frame = tk.Frame(self.frame, bg="#ECECEC")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=20, pady=20)

        # Etiqueta: Semilla (usamos el mismo estilo que en Von Neumann)
        self.seed_label = tk.Label(self.left_frame, text="Semilla", bg="#ECECEC",
                                   font=("Arial", 10, "bold"))
        self.seed_label.pack(anchor="w")

        # Etiqueta: Descripción de la semilla (opcional)
        self.seed_note_label = tk.Label(self.left_frame, text="(Ingrese la semilla)",
                                        bg="#ECECEC", font=("Arial", 8))
        self.seed_note_label.pack(anchor="w")

        # Entrada para la semilla
        self.seed_entry = tk.Entry(self.left_frame, width=15)
        self.seed_entry.pack(anchor="w", pady=5)

        # Etiqueta: Parámetros de generación (A, M, C)
        self.params_label = tk.Label(self.left_frame, text="Parámetros de Generación",
                                     bg="#ECECEC", font=("Arial", 10, "bold"))
        self.params_label.pack(anchor="w", pady=(10, 0))

        # Parámetro A
        self.a_frame = tk.Frame(self.left_frame, bg="#ECECEC")
        self.a_frame.pack(anchor="w", pady=5)
        self.a_label = tk.Label(self.a_frame, text="A:", bg="#ECECEC", font=("Arial", 10))
        self.a_label.pack(side=tk.LEFT)
        self.a_entry = tk.Entry(self.a_frame, width=10)
        self.a_entry.pack(side=tk.LEFT, padx=10)

        # Parámetro M
        self.m_frame = tk.Frame(self.left_frame, bg="#ECECEC")
        self.m_frame.pack(anchor="w", pady=5)
        self.m_label = tk.Label(self.m_frame, text="M:", bg="#ECECEC", font=("Arial", 10))
        self.m_label.pack(side=tk.LEFT)
        self.m_entry = tk.Entry(self.m_frame, width=10)
        self.m_entry.pack(side=tk.LEFT, padx=10)

        # Parámetro C
        self.c_frame = tk.Frame(self.left_frame, bg="#ECECEC")
        self.c_frame.pack(anchor="w", pady=5)
        self.c_label = tk.Label(self.c_frame, text="C:", bg="#ECECEC", font=("Arial", 10))
        self.c_label.pack(side=tk.LEFT)
        self.c_entry = tk.Entry(self.c_frame, width=10)
        self.c_entry.pack(side=tk.LEFT, padx=10)

        # Etiqueta: Cantidad de números a generar
        self.quantity_label = tk.Label(self.left_frame, text="Números a generar",
                                       bg="#ECECEC", font=("Arial", 10, "bold"))
        self.quantity_label.pack(anchor="w", pady=(10, 0))

        # Entrada para la cantidad
        self.quantity_entry = tk.Entry(self.left_frame, width=15)
        self.quantity_entry.pack(anchor="w", pady=5)

        # Botón: Generar
        self.generate_button = tk.Button(self.left_frame, text="Generar", bg="#DCDCDC")
        if hasattr(self.controller, 'on_generate_mixed'):
            self.generate_button.config(command=self.controller.on_generate_mixed)
        self.generate_button.pack(anchor="center", pady=20)

        # --- Right Frame: Resultados ---
        self.right_frame = tk.Frame(self.frame, bg="#ECECEC")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Etiqueta: Lista de números generados
        self.results_label = tk.Label(self.right_frame, text="Lista de Números Generados",
                                      bg="#ECECEC", font=("Arial", 10, "bold"))
        self.results_label.pack(anchor="nw")

        # Cuadro de texto para mostrar los resultados
        self.results_text = tk.Text(self.right_frame, height=15, width=50, wrap="word",
                                    state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
