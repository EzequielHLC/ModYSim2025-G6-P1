import unittest
from unittest.mock import MagicMock
from service.main_service import MainService

class TestMainService(unittest.TestCase):
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Se crean mocks para la base de datos y otros elementos necesarios.
        """
        self.mock_db_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_db_connection.cursor.return_value = self.mock_cursor
        self.textbox = MagicMock()
        self.result_textbox = MagicMock()

    def test_save_von_neuman_result(self):
        """
        Prueba que el método save_von_neuman_result guarde correctamente
        los resultados en la base de datos.
        """
        # Ejecutar el método
        result = MainService.save_von_neuman_result(
            self.mock_db_connection,
            seed="1234",
            chi_result=True,
            rachas_result=False,
            random_numbers=["1234", "5678"]
        )

        # Verificar que se ejecutó la consulta SQL correctamente
        self.mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO vn_results (seed, chi_square_result, rachas_result, random_numbers) VALUES (%s, %s, %s, %s)""".strip(),
            ("1234", True, False, "1234,5678")
        )
        self.mock_db_connection.commit.assert_called_once()
        self.assertTrue(result)

    def test_save_mixed_congruence_result(self):
        """
        Prueba que el método save_mixed_congruence_result guarde correctamente
        los resultados en la base de datos.
        """
        # Ejecutar el método
        result = MainService.save_mixed_congruence_result(
            self.mock_db_connection,
            seed="1234",
            a=5,
            m=16,
            c=3,
            chi_result=True,
            rachas_result=False,
            random_numbers=["1234", "5678"]
        )

        # Verificar que se ejecutó la consulta SQL correctamente
        expected_query = """
            INSERT INTO mixed_congruence_results (seed, a, m, c, chi_square_result, rachas_result, random_numbers) VALUES (%s, %s, %s, %s, %s, %s, %s)""".strip()

        self.mock_cursor.execute.assert_called_once_with(
            expected_query,
            ("1234", 5, 16, 3, True, False, "1234,5678")
        )
        self.mock_db_connection.commit.assert_called_once()
        self.assertTrue(result)

    def test_validate_digits_valid(self):
        """
        Prueba que el método validate_digits retorne True
        cuando la cantidad de dígitos es válida.
        """
        result = MainService.validate_digits("100")
        self.assertTrue(result)

    def test_validate_digits_invalid(self):
        """
        Prueba que el método validate_digits retorne False
        cuando la cantidad de dígitos es inválida.
        """
        invalid_inputs = ["-1", "0", "10001", "abc"]
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                result = MainService.validate_digits(invalid_input)
                self.assertFalse(result)

    def test_error_message(self):
        """
        Prueba que el método error_message muestre correctamente
        un mensaje de error en el textbox.
        """
        MainService.error_message("Error: mensaje de prueba", self.textbox)
        self.textbox.delete.assert_called_once_with(1.0, "end")
        self.textbox.insert.assert_called_once_with("end", "Error: mensaje de prueba\n")
        self.textbox.config.assert_called_with(state="disabled")
        self.textbox.see.assert_called_once_with("end")

    def test_loading(self):
        """
        Prueba que el método loading muestre correctamente
        un mensaje de carga en el textbox.
        """
        service = MainService()
        service.view = MagicMock()  # Mock de la vista para evitar errores
        service.loading(self.textbox)
        self.textbox.delete.assert_called_once_with(1.0, "end")
        self.textbox.insert.assert_called_once_with("end", "Generando números...\n")
        self.textbox.config.assert_called_with(state="disabled")

    def test_paste_result(self):
        """
        Prueba que el método paste_result muestre correctamente
        los resultados en el textbox.
        """
        result = ["1234", "5678"]
        MainService.paste_result(result, self.textbox)
        self.textbox.delete.assert_called_once_with(1.0, "end")
        self.textbox.insert.assert_any_call("end", "Números generados:\n")
        self.textbox.insert.assert_any_call("end", "1, 2, 3, 4, 5, 6, 7, 8\n")
        self.textbox.config.assert_called_with(state="disabled")
        self.textbox.see.assert_called_once_with("end")

if __name__ == "__main__":
    unittest.main()