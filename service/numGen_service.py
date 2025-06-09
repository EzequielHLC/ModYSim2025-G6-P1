import math

class NumGenService:

    def validate_digits(self, n_digits):
        if not n_digits.isdigit() or int(n_digits) <= 0 or int(n_digits) > 10000:
            return False
        return True

    def validate_input_vn(self, input_seed):
        if not input_seed.isdigit() or int(input_seed) <= 0:
            return False
        if len(input_seed) != 4:
            return False
        return True
    
    def generate_von_nuemann(self, seed, n_digits):
        
        # Validación de la semilla y la cantidad de dígitos
        if not self.validate_input_vn(seed):
            raise ValueError("Valor de semilla inválido. Debe ser un número entero positivo de hasta 4 dígitos.")
        if not self.validate_digits(n_digits):
            raise ValueError("Valor de dígitos inválido. Debe ser un número entero positivo entre 1 y 10000.")
        
        # Variables para el generador
        seed = int(seed)
        n_digits = int(n_digits)
        random_numbers = []

        # Generación de números aleatorios
        for _ in range(n_digits):
            squared = str(int(seed) ** 2).zfill(8)  # Cuadrar la semilla y rellenar con ceros
            mid_digits = squared[2:6]  # Obtener los 4 dígitos del medio
            if str(mid_digits).endswith("00"):
                mid_digits = int(mid_digits) + 13  # Si termina en 00, sumar 13
            random_numbers.append(mid_digits)  # Agregar el número generado a la lista
            seed = mid_digits  # Actualizar la semilla para la siguiente iteración
            random_numbers = random_numbers[-n_digits:]  # Limitar la lista a n_dígitos
        return random_numbers

    def validate_input_mc(self, input_seed, input_a, input_m, input_c):
        if not (input_seed.isdigit() and input_a.isdigit() and input_m.isdigit() and input_c.isdigit()):
            return False
        if (int(input_seed) <= 0):
            return False
        if (int(input_a) <= 0 or int(input_a) % 2 == 0):
            return False
        if (int(input_m) <= 0 or int(input_m) <= int(input_a) or int(input_m) <= int(input_seed)):
            return False
        if (int(input_c) <= 0 or int(input_c) % 2 == 0 or math.gcd(int(input_c), int(input_m)) != 1):
            return False
        return True
    
    def generate_mixed_congruence(self, seed, n_digits, a, m, c):
        
        if not self.validate_input_mc(seed, a, m, c):
            raise ValueError("Valor de parámetros inválido. No se cumplen las reglas establecidas.")
        if not self.validate_digits(n_digits):
            raise ValueError("Valor de dígitos inválido. Debe ser un número entero positivo entre 1 y 10000.")
        
        seed = int(seed)
        a = int(a)
        m = int(m)
        c = int(c)
        n_digits = int(n_digits)
        random_numbers = []

        for _ in range(n_digits):
            seed = (a * seed + c) % m  # Aplicar la fórmula de congruencia mixta
            random_numbers.append(seed)  # Agregar el número generado a la lista
        digits = [int(d) for d in str(random_numbers) if d.isdigit()]
        digits = digits[-n_digits:]  # Limitar la lista a n_dígitos
        return digits # Retornar la lista de números generados
