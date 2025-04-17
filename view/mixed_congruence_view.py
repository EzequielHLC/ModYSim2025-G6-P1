import tkinter as tk

class MixedCongruenceView:
    # Constants for UI styling
    BG_COLOR = "#ECECEC"
    FONT_BOLD = ("Arial", 10, "bold")
    FONT_NORMAL = ("Arial", 8)
    ENTRY_WIDTH = 15
    TEXTBOX_HEIGHT = 15
    TEXTBOX_WIDTH = 50

    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = self._create_main_frame(parent)
        self.left_frame = None
        self.right_frame = None

        self.left_frame = self._create_left_frame()
        self.right_frame = self._create_right_frame()

        # Expone los elementos de la vista para que puedan ser accedidos desde el controlador
        # Esto permite que el controlador pueda interactuar con los elementos de la vista, como botones y entradas de texto.
        self.view_elements = {
            "seed_entry": self.seed_entry,
            "a_entry": self.a_entry,
            "m_entry": self.m_entry,
            "c_entry": self.c_entry,
            "quantity_entry": self.quantity_entry,
            "generate_button": self.generate_button,
            "test_type": self.test_type,
            "run_test_button": self.run_test_button,
            "test_result_textbox": self.test_result_textbox,
            "result_textbox": self.result_textbox,
        }

    def _create_main_frame(self, parent):
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def _create_left_frame(self):
        left_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=20, pady=20)

        self._add_seed_input(left_frame)
        self._add_parameters_input(left_frame)
        self._add_quantity_input(left_frame)
        self._add_generate_button(left_frame)
        self._add_test_type_selection(left_frame)
        self._add_test_results_textbox(left_frame)

        return left_frame

    def _add_seed_input(self, frame):
        tk.Label(frame, text="Semilla", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w")
        tk.Label(frame, text="(Ingrese la semilla)", bg=self.BG_COLOR, font=self.FONT_NORMAL).pack(anchor="w")
        self.seed_entry = tk.Entry(frame, width=self.ENTRY_WIDTH)
        self.seed_entry.pack(anchor="w", pady=5)

    def _add_parameters_input(self, frame):
        tk.Label(frame, text="Parámetros de Generación", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        self.a_entry = self._create_param_entry("A:", frame)
        self.m_entry = self._create_param_entry("M:", frame)
        self.c_entry = self._create_param_entry("C:", frame)

    def _add_quantity_input(self, frame):
        tk.Label(frame, text="Números a generar", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        self.quantity_entry = tk.Entry(frame, width=self.ENTRY_WIDTH)
        self.quantity_entry.pack(anchor="w", pady=5)

    def _add_generate_button(self, frame):
        self.generate_button = tk.Button(frame, text="Generar", bg="#DCDCDC")
        if hasattr(self.controller, 'on_generate_mixed'):
            self.generate_button.config(command=self.controller.on_generate_mixed)
        self.generate_button.pack(anchor="center", pady=20)

    def _add_test_type_selection(self, frame):
        separator = tk.Frame(frame, height=2, bd=1, relief="sunken", bg="#A9A9A9")
        separator.pack(fill="x", pady=10)

        tk.Label(frame, text="Tipo de Prueba", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        
        self.test_type = tk.StringVar(value="Chi Cuadrado")  # Default value
        self.chi_radio = tk.Radiobutton(frame, text="Chi Cuadrado", variable=self.test_type, value="Chi Cuadrado", bg=self.BG_COLOR, font=self.FONT_NORMAL)
        self.rachas_radio = tk.Radiobutton(frame, text="Rachas", variable=self.test_type, value="Rachas", bg=self.BG_COLOR, font=self.FONT_NORMAL)
        
        self.chi_radio.pack(anchor="w")
        self.rachas_radio.pack(anchor="w")

        self.run_test_button = tk.Button(frame, text="Ejecutar Prueba", bg="#DCDCDC")
        if hasattr(self.controller, 'on_test_mixed'):
            self.run_test_button.config(command=self.controller.on_test_mixed)
        self.run_test_button.pack(anchor="center", pady=20)

    def _add_test_results_textbox(self, frame):
        tk.Label(frame, text="Resultados de Prueba", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        self.test_result_textbox = tk.Text(frame, height=30, width=25, wrap="word", state=tk.DISABLED)
        self.test_result_textbox.pack(fill=tk.BOTH, expand=False, pady=(5, 0))

    def _create_right_frame(self):
        right_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(right_frame, text="Lista de Números Generados", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="nw")
        self.result_textbox = tk.Text(right_frame, height=self.TEXTBOX_HEIGHT, width=self.TEXTBOX_WIDTH, wrap="word", state=tk.DISABLED)
        self.result_textbox.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.save_button = tk.Button(right_frame, text="Guardar", bg="#DCDCDC", state=tk.DISABLED)
        if hasattr(self.controller, 'on_save_results_mixed'):
            self.save_button.config(command=self.controller.on_save_results_mixed)
        self.save_button.pack(anchor="center", pady=10)

        return right_frame

    def _create_param_entry(self, label_text, parent):
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(anchor="w", pady=5)
        label = tk.Label(frame, text=label_text, bg=self.BG_COLOR, font=self.FONT_NORMAL)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=10)
        entry.pack(side=tk.LEFT, padx=10)
        return entry
