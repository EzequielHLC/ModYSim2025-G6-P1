import unittest
from unittest.mock import MagicMock
from controller.main_controller import MainController
from service.von_neuman_service import VonNeumanService
from service.mixed_service import MixedCongruenceService
from service.main_service import MainService
from view.main_view import MainView

class TestMainController(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Se crean mocks para los servicios, vistas y modelo.
        """
        self.mock_model = MagicMock()
        self.mock_view = MagicMock(spec=MainView)
        self.mock_vn_service = MagicMock(spec=VonNeumanService)
        self.mock_mxc_service = MagicMock(spec=MixedCongruenceService)
        self.mock_main_service = MagicMock(spec=MainService)

        # Crear instancia del controlador con los mocks
        self.controller = MainController()
        self.controller.model = self.mock_model
        self.controller.view = self.mock_view
        self.controller.vn_service = self.mock_vn_service
        self.controller.mxc_service = self.mock_mxc_service
        self.controller.main_service = self.mock_main_service

        # Mock de las vistas específicas
        self.controller.vn_view = MagicMock()
        self.controller.mxc_view = MagicMock()

    def test_on_generate_von_neumann_valid(self):
        """
        Prueba que el método on_generate_von_neumann funcione correctamente
        cuando los datos de entrada son válidos.
        """
        # Configurar valores de entrada válidos
        self.controller.vn_view.seed_entry.get.return_value = "1234"
        self.controller.vn_view.digits_entry.get.return_value = "10"
        self.mock_vn_service.validate_seed_vn.return_value = True
        self.mock_main_service.validate_digits.return_value = True
        self.mock_vn_service.von_neuman_generator.return_value = ["1234", "5678"]

        # Ejecutar el método
        self.controller.on_generate_von_neumann()

        # Verificar que se llamaron los métodos esperados
        self.mock_vn_service.validate_seed_vn.assert_called_once_with("1234")
        self.mock_main_service.validate_digits.assert_called_once_with("10")
        self.mock_vn_service.von_neuman_generator.assert_called_once_with("1234", 10)
        self.mock_main_service.paste_result.assert_called_once()

    def test_on_generate_von_neumann_invalid_seed(self):
        """
        Prueba que el método on_generate_von_neumann maneje correctamente
        una semilla inválida.
        """
        # Configurar valores de entrada inválidos
        self.controller.vn_view.seed_entry.get.return_value = "12"
        self.controller.vn_view.digits_entry.get.return_value = "10"
        self.mock_vn_service.validate_seed_vn.return_value = False

        # Ejecutar el método
        self.controller.on_generate_von_neumann()

        # Verificar que se llamó al método de error
        self.mock_main_service.error_message.assert_called_once_with(
            "Error: La semilla debe tener exactamente 4 dígitos.",
            self.controller.vn_view.result_textbox
        )

    def test_on_generate_mixed_valid(self):
        """
        Prueba que el método on_generate_mixed funcione correctamente
        cuando los datos de entrada son válidos.
        """
        # Configurar valores de entrada válidos
        self.controller.mxc_view.seed_entry.get.return_value = "1234"
        self.controller.mxc_view.a_entry.get.return_value = "5"
        self.controller.mxc_view.m_entry.get.return_value = "16"
        self.controller.mxc_view.c_entry.get.return_value = "3"
        self.controller.mxc_view.quantity_entry.get.return_value = "10"
        self.mock_mxc_service.validate_mixed_parameters.return_value = True
        self.mock_main_service.validate_digits.return_value = True
        self.mock_mxc_service.mixed_congruence_generator.return_value = ["1234", "5678"]

        # Ejecutar el método
        self.controller.on_generate_mixed()

        # Verificar que se llamaron los métodos esperados
        self.mock_mxc_service.validate_mixed_parameters.assert_called_once_with("1234", "5", "16", "3")
        self.mock_main_service.validate_digits.assert_called_once_with("10")
        self.mock_mxc_service.mixed_congruence_generator.assert_called_once_with(1234, 5, 16, 3, 10)
        self.mock_main_service.paste_result.assert_called_once()

    def test_on_generate_mixed_invalid_parameters(self):
        """
        Prueba que el método on_generate_mixed maneje correctamente
        parámetros inválidos.
        """
        # Configurar valores de entrada inválidos
        self.controller.mxc_view.seed_entry.get.return_value = "1234"
        self.controller.mxc_view.a_entry.get.return_value = "5"
        self.controller.mxc_view.m_entry.get.return_value = "16"
        self.controller.mxc_view.c_entry.get.return_value = "3"
        self.mock_mxc_service.validate_mixed_parameters.return_value = False

        # Ejecutar el método
        self.controller.on_generate_mixed()

        # Verificar que se llamó al método de error
        self.mock_main_service.error_message.assert_called_once_with(
            "Error: Los parámetros A, M y C deben seguir las siguientes reglas:\n"
            + "A: Debe ser un entero impar, no divisible por 3 o 5.\n"
            + "C: Debe ser un entero impar, relativamente primo a M.\n"
            + "M: Debe ser un entero positivo, mayor que A y mayor que la Semilla.",
            self.controller.mxc_view.result_textbox
        )

if __name__ == "__main__":
    unittest.main()