import unittest
from service.mixed_service import MixedCongruenceService

class TestMixedCongruenceService(unittest.TestCase):
    def test_mixed_congruence_generator_valid(self):
        """
        Prueba que el método mixed_congruence_generator genere correctamente
        números aleatorios con parámetros válidos.
        """
        seed = 5
        a = 3
        m = 16
        c = 7
        n_digits = 5
        expected_output = [6, 9, 2, 13, 14]

        result = MixedCongruenceService.mixed_congruence_generator(seed, a, m, c, n_digits)
        self.assertEqual(result, expected_output)

    def test_mixed_congruence_generator_zero_seed(self):
        """
        Prueba que el método mixed_congruence_generator maneje correctamente
        un caso donde la semilla inicial es cero.
        """
        seed = 0
        a = 3
        m = 16
        c = 7
        n_digits = 3
        expected_output = [7, 12, 11]

        result = MixedCongruenceService.mixed_congruence_generator(seed, a, m, c, n_digits)
        self.assertEqual(result, expected_output)

    def test_validate_mixed_parameters_valid(self):
        """
        Prueba que el método validate_mixed_parameters retorne True
        cuando los parámetros son válidos.
        """
        valid_parameters = [
            ("5", "17", "901", "19"),
            ("1", "37", "1511", "811"),
            ("10", "7", "31", "3")
        ]
        for seed, a, m, c in valid_parameters:
            with self.subTest(seed=seed, a=a, m=m, c=c):
                result = MixedCongruenceService.validate_mixed_parameters(seed, a, m, c)
                self.assertTrue(result)

    def test_validate_mixed_parameters_invalid(self):
        """
        Prueba que el método validate_mixed_parameters retorne False
        cuando los parámetros son inválidos.
        """
        invalid_parameters = [
            ("-5", "3", "16", "7"),  # Semilla negativa
            ("5", "4", "16", "7"),   # A no es impar
            ("5", "3", "10", "7"),   # M no es mayor que A o la semilla
            ("5", "3", "16", "8"),   # C no es relativamente primo a M
            ("abc", "3", "16", "7"), # Semilla no numérica
            ("5", "3", "16", "-7")   # C negativo
        ]
        for seed, a, m, c in invalid_parameters:
            with self.subTest(seed=seed, a=a, m=m, c=c):
                result = MixedCongruenceService.validate_mixed_parameters(seed, a, m, c)
                self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()