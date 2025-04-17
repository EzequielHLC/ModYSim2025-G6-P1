from view.message_box import MessageBox
from model.database import Database
import math

class MainService:

    @staticmethod
    def save_von_neuman_result(db_connection, seed, chi_result, rachas_result, random_numbers):
        query = """
        INSERT INTO vn_results (seed, chi_square_result, rachas_result, random_numbers) VALUES (%s, %s, %s, %s)""".strip()
        cursor = db_connection.cursor()
        cursor.execute(query, (seed, chi_result, rachas_result, ",".join(map(str, random_numbers))))
        db_connection.commit()
        return True

    
    @staticmethod
    def save_mixed_congruence_result(db_connection, seed, a, m, c, chi_result, rachas_result, random_numbers):
        query = """
        INSERT INTO mixed_congruence_results (seed, a, m, c, chi_square_result, rachas_result, random_numbers) VALUES (%s, %s, %s, %s, %s, %s, %s)""".strip()
        cursor = db_connection.cursor()
        cursor.execute(query, (seed, a, m, c, chi_result, rachas_result, ",".join(map(str, random_numbers))))
        db_connection.commit()
        return True

    def error_message(message, textbox):
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
        self.view.root.update()
    
    def paste_result(result, textbox):
        # Método para pegar el resultado en el textbox
        textbox.config(state="normal")
        textbox.delete(1.0, "end")
        textbox.insert("end", "Números generados:\n")
        digit_by_digit_result = ", ".join(", ".join(digit for digit in str(number)) for number in result)
        textbox.insert("end", digit_by_digit_result + "\n")
        textbox.config(state="disabled")
        textbox.see("end")

    def validate_digits(n_digits):
        # Validar que la cantidad de dígitos sea un número entero positivo
        if not n_digits.isdigit() or int(n_digits) <= 0 or int(n_digits) > 10000:
            return False
        return True

    def run_chi_square_test(textbox, result_textbox):
        # Obtener los números generados desde la vista
        numbers = textbox.get("1.0", "end-1c").split(",")
        numbers = [int(num.strip()) for num in numbers if num.strip().isdigit()]
        if len(numbers) == 0:
            MessageBox.show_error("Error", "No se han generado números válidos para realizar la prueba.")
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

        # Mostrar las frecuencias observadas en el textbox
        result_textbox.config(state="normal")
        result_textbox.delete(1.0, "end")
        result_textbox.insert("end", "Frecuencias observadas:\n")
        for i, freq in enumerate(observed_freq):
            result_textbox.insert("end", f"Dígito {i}: {freq}\n")
        result_textbox.insert("end", f"\nEstadístico Chi Cuadrado: {chi_square_statistic}\n")
        result_textbox.insert("end", f"Valor crítico: {critical_value}\n")
        result_textbox.insert("end", f"Resultado: {'Aceptado' if result else 'Rechazado'}\n")
        result_textbox.config(state="disabled")
        result_textbox.see("end")

        return result  # Retornar el resultado de la prueba
    
    def run_rachas_test(textbox, result_textbox):
        # Obtener los números generados desde la vista
        numbers = textbox.get("1.0", "end-1c").split(",")
        numbers = [int(num.strip()) for num in numbers if num.strip().isdigit()]
        n = len(numbers)
        if n == 0:
            MessageBox.show_error("Error", "No se han generado números válidos para realizar la prueba.")
            return
        
        # Calcular el número de rachas
        runs = 1 # Siempre hay al menos una racha

        # Calcular cuantos bits se necesitan para representar el número mas grande
        max_number = max(numbers)
        bits = max_number.bit_length() or 1 # Me aseguro de que bits sea al menos 1

        # Convertir los números a binario y contar las rachas (una racha es un cambio de 0 a 1 o de 1 a 0)
        # Almaceno el bit anterior para compararlo con el actual
        prev_bit = None
        for num in numbers:
            # Convertir el número a binario y rellenar con ceros a la izquierda
            binary_num = format(num, '0' + str(bits) + 'b')
            for bit in binary_num:
                if prev_bit is None or bit != prev_bit:
                    runs += 1
                prev_bit = bit
        
        # Calcular el número esperado de rachas
        mu = 1 + (2 * n - 1) / 2 # Número esperado de rachas
        variance = (n * (n - 2)) / (4 * (n - 1))  if n > 1 else 0 # Varianza de rachas
        std_dev = math.sqrt(variance) # Desviación estándar de rachas

        # Calcular estadístico Z
        z = (runs - mu) / std_dev if std_dev != 0 else 0

        # Calcular el valor crítico para el nivel de significancia del 5%
        critical_value = 1.96  # Valor crítico para Z con alpha = 0.05 (bilateral)

        # Comparar el estadístico Z con el valor crítico
        if abs(z) < critical_value:
            result = True
        else:
            result = False

        # Mostrar el resultado de la prueba en el textbox
        result_textbox.config(state="normal")
        result_textbox.delete(1.0, "end")
        result_textbox.insert("end", f"Rachas: {runs}\n")
        result_textbox.insert("end", f"Valor Z: {z}\n")
        result_textbox.insert("end", f"Valor crítico: {critical_value}\n")
        result_textbox.insert("end", f"Resultado: {'Aceptado' if result else 'Rechazado'}\n")
        result_textbox.config(state="disabled")
        result_textbox.see("end")
        return result  # Retornar el resultado de la prueba