import unittest
from unittest.mock import MagicMock
from controller.main_controller import MainController

class TestMainController(unittest.TestCase):
    """
    Clase de pruebas unitarias para la clase MainController.
    Esta clase contiene pruebas para validar las funcionalidades del controlador principal,
    incluyendo la validación de entradas, generación de números pseudoaleatorios mediante
    los métodos de Von Neumann y Congruencia Mixta, y manejo de errores en la interfaz de usuario.
    Métodos:
    --------
    - setUp():
        Configura el entorno de pruebas inicializando el controlador y simulando las vistas.
    - test_validate_seed_vn_valid():
        Verifica que el método validate_seed_vn acepte semillas válidas de 4 dígitos.
    - test_validate_seed_vn_invalid():
        Verifica que el método validate_seed_vn rechace semillas inválidas (menos o más de 4 dígitos, o caracteres no numéricos).
    - test_validate_mixed_parameters_valid():
        Verifica que el método validate_mixed_parameters acepte parámetros válidos para el método de Congruencia Mixta.
    - test_validate_mixed_parameters_invalid():
        Verifica que el método validate_mixed_parameters rechace parámetros inválidos que no cumplan las reglas establecidas.
    - test_validate_digits_valid():
        Verifica que el método validate_digits acepte valores válidos de dígitos (números enteros positivos dentro del rango permitido).
    - test_validate_digits_invalid():
        Verifica que el método validate_digits rechace valores inválidos (números negativos, cero, caracteres no numéricos o fuera del rango permitido).
    - test_von_neumann():
        Prueba la generación de números pseudoaleatorios mediante el método de Von Neumann,
        verificando que la cantidad de números generados sea la esperada.
    - test_mixed_congruence():
        Prueba la generación de números pseudoaleatorios mediante el método de Congruencia Mixta,
        verificando que la cantidad de números generados sea la esperada.
    - test_on_generate_von_neumann_invalid_seed():
        Verifica que el controlador maneje correctamente el error cuando se intenta generar números
        con una semilla inválida en el método de Von Neumann.
    - test_on_generate_mixed_invalid_parameters():
        Verifica que el controlador maneje correctamente el error cuando se intenta generar números
        con parámetros inválidos en el método de Congruencia Mixta.
    """
    def setUp(self):
        self.controller = MainController()
        self.controller.view = MagicMock()
        self.controller.vn_view = MagicMock()
        self.controller.mxc_view = MagicMock()

    def test_validate_seed_vn_valid(self):
        self.assertTrue(self.controller.validate_seed_vn("1234"))

    def test_validate_seed_vn_invalid(self):
        self.assertFalse(self.controller.validate_seed_vn("123"))
        self.assertFalse(self.controller.validate_seed_vn("abcd"))
        self.assertFalse(self.controller.validate_seed_vn("12345"))

    def test_validate_mixed_parameters_valid(self):
        self.assertTrue(self.controller.validate_mixed_parameters("5", "7", "11", "3"))

    def test_validate_mixed_parameters_invalid(self):
        self.assertFalse(self.controller.validate_mixed_parameters("0", "7", "11", "3"))
        self.assertFalse(self.controller.validate_mixed_parameters("5", "6", "11", "3"))
        self.assertFalse(self.controller.validate_mixed_parameters("5", "7", "5", "3"))
        self.assertFalse(self.controller.validate_mixed_parameters("5", "7", "11", "2"))

    def test_validate_digits_valid(self):
        self.assertTrue(self.controller.validate_digits("100"))
        self.assertTrue(self.controller.validate_digits("1"))

    def test_validate_digits_invalid(self):
        self.assertFalse(self.controller.validate_digits("0"))
        self.assertFalse(self.controller.validate_digits("-1"))
        self.assertFalse(self.controller.validate_digits("abc"))
        self.assertFalse(self.controller.validate_digits("10001"))

    def test_von_neumann(self):
        result = self.controller.von_neumann("1234", 5)
        self.assertEqual(len(result), 5)

    def test_mixed_congruence(self):
        result = self.controller.mixed_congruence(5, 7, 11, 3, 5)
        self.assertEqual(len(result), 5)

    def test_on_generate_von_neumann_invalid_seed(self):
        self.controller.vn_view.seed_entry.get.return_value = "123"
        self.controller.vn_view.digits_entry.get.return_value = "5"
        self.controller.error_message = MagicMock()
        self.controller.on_generate_von_neumann()
        self.controller.error_message.assert_called_with(
            "Error: La semilla debe tener exactamente 4 dígitos.",
            self.controller.vn_view.result_textbox
        )

    def test_on_generate_mixed_invalid_parameters(self):
        self.controller.mxc_view.seed_entry.get.return_value = "0"
        self.controller.mxc_view.a_entry.get.return_value = "6"
        self.controller.mxc_view.m_entry.get.return_value = "5"
        self.controller.mxc_view.c_entry.get.return_value = "2"
        self.controller.error_message = MagicMock()
        self.controller.on_generate_mixed()
        self.controller.error_message.assert_called_with(
            "Error: Los parámetros A, M y C deben seguir las siguientes reglas:\n"
            + "A: Debe ser un entero impar, no divisible por 3 o 5.\n"
            + "C: Debe ser un entero impar, relativamente primo a M.\n"
            + "M: Debe ser un entero positivo, mayor que A y mayor que la Semilla.",
            self.controller.mxc_view.result_textbox
        )

if __name__ == "__main__":
    unittest.main()