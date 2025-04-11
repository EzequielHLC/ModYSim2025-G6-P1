# from model.database import Database  # Descomentar si se usa la base de datos
from view.main_view import MainView
import math # Importar la función gcd para calcular el máximo común divisor

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
        digit_by_digit_result = ", ".join(", ".join(digit for digit in str(number)) for number in result)
        textbox.insert("end", digit_by_digit_result + "\n")
        textbox.config(state="disabled")
        textbox.see("end")



    def validate_seed_vn(self, seed):
        # Validar que la semilla tenga exactamente 4 dígitos
        if len(seed) != 4 or not seed.isdigit():
            return False
        return True
    
    def validate_mixed_parameters(self, seed, a, m, c):
        # Validar que los parámetros A, M y C sean números enteros positivos
        if not (seed.isdigit() and a.isdigit() and m.isdigit() and c.isdigit()):
            return False
        if (int(seed) <= 0):
            return False
        if (int(a) <= 0 or int(a) % 2 == 0 or int(a) % 3 == 0 or int(a) % 5 == 0):
            return False
        if (int(m) <= 0 or int(m) <= int(a) or int(m) <= int(seed)):
            return False
        if (int(c) <= 0 or int(c) % 2 == 0 or math.gcd(int(c), int(m)) != 1):
            return False
        return True

    def validate_digits(self, n_digits):
        # Validar que la cantidad de dígitos sea un número entero positivo
        if not n_digits.isdigit() or int(n_digits) <= 0 or int(n_digits) > 10000:
            return False
        return True



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


    def mixed_congruence(self, seed, a, m, c, n_digits):
        # Método para generar números aleatorios usando el método de Congruencias Mixtas
        random_numbers = []  # Lista para almacenar los números aleatorios generados
        
        for _ in range(n_digits):
            seed = (a * seed + c) % m  # Aplicar la fórmula de congruencia mixta
            random_numbers.append(seed)  # Agregar el número generado a la lista
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

    def on_generate_mixed(self):
        # Obtener la semilla y los parámetros desde la vista
        seed = self.mixed_congruence_view.seed_entry.get()
        a = self.mixed_congruence_view.a_entry.get()
        m = self.mixed_congruence_view.m_entry.get()
        c = self.mixed_congruence_view.c_entry.get()

        if not self.validate_mixed_parameters(seed, a, m, c):
            self.error_message("Error: Los parámetros A, M y C deben seguir las siguientes reglas:\n" + "A: Debe ser un entero impar, no divisible por 3 o 5.\n" + 
                               "C: Debe ser un entero impar, relativamente primo a M.\n" + 
                               "M: Debe ser un entero positivo, mayor que A y mayor que la Semilla.", self.mixed_congruence_view.results_text)
            return
        if not self.validate_digits(self.mixed_congruence_view.quantity_entry.get()):
            self.error_message("Error: La cantidad de dígitos debe ser un número entero positivo menor a 10000.", self.mixed_congruence_view.results_text)
            return
        
        # Llamar al método de la vista para generar números aleatorios (No suele llegar a ejecutarse por la generacion tan rapida)
        self.loading(self.mixed_congruence_view.results_text)
        self.mixed_congruence_view.generate_button.config(state="disabled")

        # Aquí se llamaría al método de la base de datos para generar los números aleatorios
        random_numbers = self.mixed_congruence(int(seed), int(a), int(m), int(c), int(self.mixed_congruence_view.quantity_entry.get()))
        self.paste_result(random_numbers, self.mixed_congruence_view.results_text)
        self.mixed_congruence_view.generate_button.config(state="normal")