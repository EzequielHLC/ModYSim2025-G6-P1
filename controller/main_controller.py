# from model.database import Database  # Descomentar si se usa la base de datos
from view.main_view import MainView

class MainController:
    def __init__(self):
        #self.model = Database()
        self.view = MainView(self)  # Inicializa la vista principal
        self.von_neumann_view = self.view.von_neumann_view  # Vista Von Neumann
        self.mixed_congruence_view = self.view.mixed_congruence_view  # Vista Congruencias Mixtas
    
    def run(self):
        self.view.run()

    def error_message(self, message, textbox=None):
        # Método para mostrar mensajes de error en la vista
        textbox.config(state="normal")
        textbox.delete(1.0, "end")
        textbox.insert("end", message + "\n")
        textbox.config(state="disabled")
        textbox.see("end")
    
    def validate_seed_vn(self, seed):
        # Validar que la semilla tenga exactamente 4 dígitos
        if len(seed) != 4 or not seed.isdigit():
            return False
        return True
    
    def validate_digits(self, n_digits):
        # Validar que la cantidad de dígitos sea un número entero positivo
        if not n_digits.isdigit() or int(n_digits) <= 0 or int(n_digits) > 10000:
            return False
        return True
    
    def loading(self, textbox):
        # Método para mostrar un mensaje de carga en el textbox
        textbox.config(state="normal")
        textbox.delete(1.0, "end")
        textbox.insert("end", "Generando números...\n")
        textbox.config(state="disabled")
        self.view.root.update()  # Actualizar la vista para mostrar el mensaje de carga

    def paste_result(self, result, textbox):
        # Método para pegar el resultado en el textbox
        textbox.config(state="normal")
        textbox.delete(1.0, "end")
        textbox.insert("end", "Números generados:\n")
        textbox.insert("end", ", ".join(map(str, result)) + "\n")
        textbox.config(state="disabled")
        textbox.see("end")

    def von_neumann(self, seed, n_digits):
        # Método para generar números aleatorios usando el método de Von Neumann

        random_numbers = []  # Lista para almacenar los números aleatorios generados

        for _ in range(n_digits):
            squared = str(int(seed) ** 2).zfill(8)  # Cuadrar la semilla y rellenar con ceros
            mid_digits = squared[2:6]  # Obtener los 4 dígitos del medio

            if str(mid_digits).endswith("00"):
                mid_digits = int(mid_digits) + 13  # Si termina en 00, sumar 13
            random_numbers.append(mid_digits)  # Agregar el número generado a la lista
            seed = mid_digits  # Actualizar la semilla para la siguiente iteración
        return random_numbers  # Retornar la lista de números generados
    
    def on_generate_von_neumann(self):
        # Obtener la semilla y la cantidad de dígitos desde la vista
        seed = self.von_neumann_view.seed_entry.get()
        n_digits = self.von_neumann_view.digits_entry.get()

        # Validar la semilla y la cantidad de dígitos
        if not self.validate_seed_vn(seed):
            self.error_message("Error: La semilla debe tener exactamente 4 dígitos.", self.von_neumann_view.result_textbox)
            return
        if not self.validate_digits(n_digits):
            self.error_message("Error: La cantidad de dígitos debe ser un número entero positivo menor a 10000.", self.von_neumann_view.result_textbox)
            return
        
        # Llamar al método de la vista para generar números aleatorios (No suele llegar a ejecutarse por la generacion tan rapida)
        self.loading(self.von_neumann_view.result_textbox)  # Mostrar mensaje de carga
        self.von_neumann_view.generate_button.config(state="disabled")  # Deshabilitar el botón de generar

        # Aquí se llamaría al método de la base de datos para generar los números aleatorios
        random_numbers = self.von_neumann(seed, int(n_digits))
        self.paste_result(random_numbers, self.von_neumann_view.result_textbox)
        self.von_neumann_view.generate_button.config(state="normal")  # Habilitar el botón de generar nuevamente