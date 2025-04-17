import unittest
from service.von_neuman_service import VonNeumanService

class TestVonNeumanService(unittest.TestCase):
    def test_von_neuman_generator_valid(self):
        """
        Prueba que el método von_neuman_generator genere correctamente
        números aleatorios con una semilla válida.
        """
        seed = "1234"
        n_digits = 5
        expected_output = ["5227", "3215", "3362", "3030", "1809"]

        result = VonNeumanService.von_neuman_generator(seed, n_digits)
        self.assertEqual(result, expected_output)

    def test_von_neuman_generator_seed_ends_with_00(self):
        """
        Prueba que el método von_neuman_generator maneje correctamente
        semillas que terminan en "00".
        """
        seed = "1000"
        n_digits = 3
        expected_output = [13, '0001', 13]

        result = VonNeumanService.von_neuman_generator(seed, n_digits)
        self.assertEqual(result, expected_output)

    def test_von_neuman_generator_invalid_seed(self):
        """
        Prueba que el método von_neuman_generator maneje correctamente
        una semilla inválida (no numérica o negativa).
        """
        with self.assertRaises(ValueError):
            VonNeumanService.von_neuman_generator("abcd", 5)

    def test_validate_seed_vn_valid(self):
        """
        Prueba que el método validate_seed_vn retorne True
        cuando la semilla es válida.
        """
        valid_seeds = ["1234", "5678", "0001"]
        for seed in valid_seeds:
            with self.subTest(seed=seed):
                result = VonNeumanService.validate_seed_vn(seed)
                self.assertTrue(result)

    def test_validate_seed_vn_invalid(self):
        """
        Prueba que el método validate_seed_vn retorne False
        cuando la semilla es inválida.
        """
        invalid_seeds = ["12", "abcd", "-1234", "12345", ""]
        for seed in invalid_seeds:
            with self.subTest(seed=seed):
                result = VonNeumanService.validate_seed_vn(seed)
                self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()