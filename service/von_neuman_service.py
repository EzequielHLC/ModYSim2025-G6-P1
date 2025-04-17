class VonNeumanService:
    
    def von_neuman_generator(seed, n_digits):
        """
        Generador de números aleatorios utilizando el método de Von Neumann.
        :param seed: Semilla inicial (debe ser un número entero positivo).
        :param n_digits: Cantidad de dígitos a generar (debe ser un número entero positivo).
        :return: Lista de números generados.
        """
        random_numbers = []  # Lista para almacenar los números aleatorios generados

        for _ in range(n_digits):
            squared = str(int(seed) ** 2).zfill(8)  # Cuadrar la semilla y rellenar con ceros
            mid_digits = squared[2:6]  # Obtener los 4 dígitos del medio

            if str(mid_digits).endswith("00"):
                mid_digits = int(mid_digits) + 13  # Si termina en 00, sumar 13
            random_numbers.append(mid_digits)  # Agregar el número generado a la lista
            seed = mid_digits  # Actualizar la semilla para la siguiente iteración
        return random_numbers  # Retornar la lista de números generados

    def validate_seed_vn(seed):
        # Validar que la semilla tenga exactamente 4 dígitos
        if len(seed) != 4 or not seed.isdigit():
            return False
        return True