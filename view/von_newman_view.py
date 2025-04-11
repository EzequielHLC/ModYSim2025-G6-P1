import tkinter as tk

class VonNeumannView:
    BG_COLOR = "#ECECEC"
    FONT_BOLD = ("Arial", 10, "bold")
    FONT_NORMAL = ("Arial", 8)
    ENTRY_WIDTH = 15
    TEXTBOX_HEIGHT = 15
    TEXTBOX_WIDTH = 50

    def __init__(self, parent, controller):
        self.controller = controller
        self.frame = self._create_main_frame(parent)
        self.left_frame = self._create_left_frame()
        self.right_frame = self._create_right_frame()

    def _create_main_frame(self, parent):
        frame = tk.Frame(parent, bg=self.BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True)
        return frame

    def _create_left_frame(self):
        left_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=20, pady=20)

        self._add_seed_input(left_frame)
        self._add_digits_input(left_frame)
        self._add_generate_button(left_frame)

        return left_frame

    def _add_seed_input(self, frame):
        tk.Label(frame, text="Semilla", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w")
        tk.Label(frame, text="(La semilla debe tener 4 dígitos)", bg=self.BG_COLOR, font=self.FONT_NORMAL).pack(anchor="w")
        self.seed_entry = tk.Entry(frame, width=self.ENTRY_WIDTH)
        self.seed_entry.pack(anchor="w", pady=5)

    def _add_digits_input(self, frame):
        tk.Label(frame, text="Números a generar", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="w", pady=(10, 0))
        self.digits_entry = tk.Entry(frame, width=self.ENTRY_WIDTH)
        self.digits_entry.pack(anchor="w", pady=5)

    def _add_generate_button(self, frame):
        self.generate_button = tk.Button(frame, text="Generar", bg="#DCDCDC")
        if hasattr(self.controller, 'on_generate_von_neumann'):
            self.generate_button.config(command=self.controller.on_generate_von_neumann)
        self.generate_button.pack(anchor="center", pady=20)

    def _create_right_frame(self):
        right_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(right_frame, text="Lista de Números Generados", bg=self.BG_COLOR, font=self.FONT_BOLD).pack(anchor="nw")
        self.result_textbox = tk.Text(right_frame, height=self.TEXTBOX_HEIGHT, width=self.TEXTBOX_WIDTH, wrap="word", state=tk.DISABLED)
        self.result_textbox.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        return right_frame
