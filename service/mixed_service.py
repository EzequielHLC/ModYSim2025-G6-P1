import math

class MixedCongruenceService:

    def mixed_congruence_generator(seed, a, m, c, n_digits):
        # Método para generar números aleatorios usando el método de Congruencias Mixtas
        random_numbers = []  # Lista para almacenar los números aleatorios generados
        
        for _ in range(n_digits):
            seed = (a * seed + c) % m  # Aplicar la fórmula de congruencia mixta
            random_numbers.append(seed)  # Agregar el número generado a la lista
        return random_numbers  # Retornar la lista de números generados

    def validate_mixed_parameters(seed, a, m, c):
        # Validar que los parámetros A, M y C sean números enteros positivos
        if not (seed.isdigit() and a.isdigit() and m.isdigit() and c.isdigit()):
            return False
        if (int(seed) <= 0):
            return False
        if (int(a) <= 0):
            return False
        if (int(m) <= 0 or int(m) <= int(a) or int(m) <= int(seed)):
            return False
        if (int(c) <= 0 or int(c) % 2 == 0 or math.gcd(int(c), int(m)) != 1):
            return False
        return True

