# from model.database import Database  # Descomentar si se usa la base de datos
from view.main_view import MainView
from view.message_box import MessageBox
import math # Importar la función gcd para calcular el máximo común divisor

class MainController:
    def __init__(self):
        # self.model = Database()
        self.view = MainView(self)  # Inicializa la vista principal
        self.von_neumann_view = self.view.von_neumann_view  # Vista Von Neumann
        self.mixed_congruence_view = self.view.mixed_congruence_view  # Vista Congruencias Mixtas
    
    def run(self):
        #if self.model.connection is None:
            # Si la conexión a la base de datos es exitosa, se inicia la vista
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

    def run_chi_square_test(self, view):
        # Obtener los números generados desde la vista
        numbers = view.result_textbox.get("1.0", "end-1c").split(",")
        numbers = [int(num.strip()) for num in numbers if num.strip().isdigit()]
        if len(numbers) == 0:
            MessageBox.show_error("Error", "No se han generado números válidos para realizar la prueba.")
            view.chi_radio.config(fg="black")
            return
        
        # Calcular la frecuencia esperada
        expected_freq = len(numbers) / 10  # Frecuencia esperada para cada dígito (0-9)

        for i in range(len(numbers)):
            numbers[i] = int(numbers[i]) % 10
        # Calcular la frecuencia observada
        observed_freq = [0] * 10
        for num in numbers:
            observed_freq[num] += 1
        
        # Calcular el estadístico de Chi Cuadrado
        chi_square_statistic = sum((obs - expected_freq) ** 2 / expected_freq for obs in observed_freq)

        # Grados de libertad
        degrees_of_freedom = len(observed_freq) - 1
        #valor crítico para el nivel de significancia del 5%
        critical_value = 16.919  # Valor crítico para Chi Cuadrado con 9 grados de libertad y alpha = 0.05
        # Comparar el estadístico con el valor crítico
        if chi_square_statistic < critical_value:
            result = True
        else:
            result = False
        return result  # Retornar el resultado de la prueba
        

    def run_rachas_test(self, view):
        """
        Ejecuta el Test de Rachas sobre la última lista de enteros generados.
        Usa las fórmulas teóricas correctas para bits independientes con p=0.5.
        """

        # 1) Obtener la última lista generada de números enteros
        numbers = getattr(self, 'last_generated', [])  # Si no existe, retorna una lista vacía

        # Validar que haya números disponibles para analizar
        if not numbers:
            MessageBox.show_error("Error", "No se han generado números válidos para realizar la prueba.")
            view.rachas_radio.config(fg="black")  # Restablece el color del botón de la vista si falla
            return

        # 2) Convertir todos los valores a enteros (por si llegaron como strings)
        numbers = [int(n) for n in numbers]

        # 3) Calcular cuántos bits como mínimo se necesitan para representar el número más grande
        max_val = max(numbers)                         # Busca el valor máximo en la lista
        bit_length = max_val.bit_length() or 1         # .bit_length() devuelve la cantidad de bits necesarios
                                                   # Si max_val es 0, devuelve 1 por defecto para evitar errores

        # 4) Convertir cada número a binario y concatenarlos en una sola cadena de bits
        bitstring = "".join(format(num, f"0{bit_length}b") for num in numbers)
        n = len(bitstring)  # Total de bits generados

        # 5) Contar las "rachas": una racha es un cambio de bit (de 0 a 1 o de 1 a 0)
        runs_observed = 1  # Siempre hay al menos una racha
        for i in range(1, n):
            if bitstring[i] != bitstring[i-1]:  # Si el bit actual es distinto al anterior, hay un cambio (nueva racha)
                runs_observed += 1

        # 6) Calcular el valor esperado (mu) y la desviación estándar (std_deviation) para una secuencia aleatoria de bits con p = 0.5
        mu = 1 + (n - 1) / 2                           # Valor esperado de rachas
        variance = (n * (n - 2)) / (4 * (n - 1)) if n > 1 else 0  # Varianza (evita división por cero)
        std_deviation = math.sqrt(variance) if variance > 0 else 0  # Desviación estándar

        # 7) Calcular el estadístico Z para comparar la cantidad de rachas observadas con la esperada
        z = (runs_observed - mu) / std_deviation if std_deviation != 0 else float('inf')

        # === Sección de depuración para ver valores de la prueba en consola (usado solo con propositos de evaluación del comportamiento del test)===
        print("=== DEBUG TEST DE RACHAS ===")
        print(f"bit_length: {bit_length}")          # Cuántos bits se usaron por número
        print(f"total bits (n): {n}")               # Total de bits analizados
        print(f"rachas observadas: {runs_observed}")# Cuántas rachas se detectaron
        print(f"mu (esperado): {mu:.4f}")           # Valor esperado de rachas
        print(f"std_deviation: {std_deviation:.4f}")# Desviación estándar
        print(f"Z: {z:.4f}")                        # Estadístico Z calculado
        print("=======================")

        # 8) Decisión final: se acepta la hipótesis de aleatoriedad si |Z| <= 1.96 (nivel de confianza 95%)
        if std_deviation == 0:
            MessageBox.show_error("Error", "Secuencia de bits demasiado corta para realizar el Test de Rachas.")
            return 

        return abs(z) <= 1.96  # Devuelve True si pasa el test, False si no lo pasa


    def on_generate_von_neumann(self):
        # Obtener la semilla y la cantidad de dígitos desde la vista
        seed = self.von_neumann_view.seed_entry.get()
        n_digits = self.von_neumann_view.digits_entry.get()

        # Validar la semilla y la cantidad de dígitos
        if not self.validate_seed_vn(seed):
            self.last_generated = []
            self.error_message("Error: La semilla debe tener exactamente 4 dígitos.", self.von_neumann_view.result_textbox)
            return
        if not self.validate_digits(n_digits):
            self.last_generated = []  
            self.error_message("Error: La cantidad de dígitos debe ser un número entero positivo menor a 10000.", self.von_neumann_view.result_textbox)
            return
        
        # Llamar al método de la vista para generar números aleatorios (No suele llegar a ejecutarse por la generacion tan rapida)
        self.loading(self.von_neumann_view.result_textbox)  # Mostrar mensaje de carga
        self.von_neumann_view.generate_button.config(state="disabled")  # Deshabilitar el botón de generar

        # Aquí se llamaría al método de la base de datos para generar los números aleatorios
        random_numbers = self.von_neumann(seed, int(n_digits))
        self.last_generated = random_numbers

        self.paste_result(random_numbers, self.von_neumann_view.result_textbox)
        self.von_neumann_view.generate_button.config(state="normal")  # Habilitar el botón de generar nuevamente

    def on_generate_mixed(self):
        # Obtener la semilla y los parámetros desde la vista
        seed = self.mixed_congruence_view.seed_entry.get()
        a = self.mixed_congruence_view.a_entry.get()
        m = self.mixed_congruence_view.m_entry.get()
        c = self.mixed_congruence_view.c_entry.get()

        if not self.validate_mixed_parameters(seed, a, m, c):
            self.last_generated = []
            self.error_message("Error: Los parámetros A, M y C deben seguir las siguientes reglas:\n" + "A: Debe ser un entero impar, no divisible por 3 o 5.\n" + 
                               "C: Debe ser un entero impar, relativamente primo a M.\n" + 
                               "M: Debe ser un entero positivo, mayor que A y mayor que la Semilla.", self.mixed_congruence_view.result_textbox)
            return
        if not self.validate_digits(self.mixed_congruence_view.quantity_entry.get()):
            self.last_generated = []
            self.error_message("Error: La cantidad de dígitos debe ser un número entero positivo menor a 10000.", self.mixed_congruence_view.result_textbox)
            return
        
        # Llamar al método de la vista para generar números aleatorios (No suele llegar a ejecutarse por la generacion tan rapida)
        self.loading(self.mixed_congruence_view.result_textbox)
        self.mixed_congruence_view.generate_button.config(state="disabled")

        # Aquí se llamaría al método de la base de datos para generar los números aleatorios
        random_numbers = self.mixed_congruence(int(seed), int(a), int(m), int(c), int(self.mixed_congruence_view.quantity_entry.get()))
        self.last_generated = random_numbers
        
        self.paste_result(random_numbers, self.mixed_congruence_view.result_textbox)
        self.mixed_congruence_view.generate_button.config(state="normal")

    def on_run_test(self, view):
        # Obtener el tipo de prueba seleccionada
        test_type = view.test_type.get()
        if test_type == "Chi Cuadrado":
            result = self.run_chi_square_test(view)
            if result == True:
                MessageBox.show_info("Resultado", "La prueba Chi Cuadrado ha pasado.")
                view.chi_radio.config(fg="green")
            if result == False:
                MessageBox.show_error("Resultado", "La prueba Chi Cuadrado no ha pasado.")
                view.chi_radio.config(fg="black")
        elif test_type == "Rachas":
            result = self.run_rachas_test(view)
            if result == True:
                MessageBox.show_info("Resultado", "La prueba de Rachas ha pasado.")
                view.rachas_radio.config(fg="green")
            if result == False:
                MessageBox.show_error("Resultado", "La prueba de Rachas no ha pasado.")
                view.rachas_radio.config(fg="black")
