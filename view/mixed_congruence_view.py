import tkinter as tk

class MixedCongruenceView:
    # Esta clase define la vista para el generador de números aleatorios de Congruencias Mixtas.
    # Defino las constantes para los colores y fuentes que se utilizarán en la interfaz gráfica.
    # Estas constantes se utilizan para mantener la consistencia en el diseño de la interfaz.
    # Me ahorro codigo al definirlas aquí y no repetirlas en cada widget.
    BG_COLOR = "#ECECEC"
    FONT_BOLD = ("Arial", 10, "bold")
    FONT_NORMAL = ("Arial", 8)
    ENTRY_WIDTH = 15
    TEXTBOX_HEIGHT = 15
    TEXTBOX_WIDTH = 50

    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = tk.Frame(parent, bg=self.BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self._create_left_frame()
        self._create_right_frame()

    def _create_left_frame(self):
        self.left_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=20, pady=20)

        self._create_label(self.left_frame, "Semilla", self.FONT_BOLD).pack(anchor="w")
        self._create_label(self.left_frame, "(Ingrese la semilla)", self.FONT_NORMAL).pack(anchor="w")
        self.seed_entry = self._create_entry(self.left_frame, self.ENTRY_WIDTH)
        self.seed_entry.pack(anchor="w", pady=5)

        self._create_label(self.left_frame, "Parámetros de Generación", self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        self.a_entry = self._create_param_entry("A:", self.left_frame)
        self.m_entry = self._create_param_entry("M:", self.left_frame)
        self.c_entry = self._create_param_entry("C:", self.left_frame)

        self._create_label(self.left_frame, "Números a generar", self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        self.quantity_entry = self._create_entry(self.left_frame, self.ENTRY_WIDTH)
        self.quantity_entry.pack(anchor="w", pady=5)

        self.generate_button = tk.Button(self.left_frame, text="Generar", bg="#DCDCDC")
        if hasattr(self.controller, 'on_generate_mixed'):
            self.generate_button.config(command=self.controller.on_generate_mixed)
        self.generate_button.pack(anchor="center", pady=20)

    def _create_right_frame(self):
        self.right_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._create_label(self.right_frame, "Lista de Números Generados", self.FONT_BOLD).pack(anchor="nw")
        self.results_text = tk.Text(self.right_frame, height=self.TEXTBOX_HEIGHT, width=self.TEXTBOX_WIDTH, wrap="word", state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def _create_label(self, parent, text, font):
        return tk.Label(parent, text=text, bg=self.BG_COLOR, font=font)

    def _create_entry(self, parent, width):
        return tk.Entry(parent, width=width)

    def _create_param_entry(self, label_text, parent):
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(anchor="w", pady=5)
        label = self._create_label(frame, label_text, self.FONT_NORMAL)
        label.pack(side=tk.LEFT)
        entry = self._create_entry(frame, 10)
        entry.pack(side=tk.LEFT, padx=10)
        return entry
