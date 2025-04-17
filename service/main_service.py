from view.message_box import MessageBox

class MainService:

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
        result_textbox.config(state="disabled")
        result_textbox.see("end")

        return result  # Retornar el resultado de la prueba