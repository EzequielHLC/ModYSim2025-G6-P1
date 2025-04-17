# from model.database import Database  # Descomentar si se usa la base de datos

from service.main_service import MainService  # Importar el servicio principal
from service.von_neuman_service import VonNeumanService  # Importar el servicio de Von Neumann
from service.mixed_service import MixedCongruenceService  # Importar la función de congruencias mixtas

from view.main_view import MainView
from view.message_box import MessageBox
import math # Importar la función gcd para calcular el máximo común divisor

class MainController:
    def __init__(self):
        # self.model = Database()
        self.view = MainView(self)  # Inicializa la vista principal
        self.vn_view = self.view.von_neumann_view  # Vista Von Neumann
        self.mxc_view = self.view.mixed_congruence_view  # Vista Congruencias Mixtas

        self.main_service = MainService # Inicializa el servicio principal
        self.vn_service = VonNeumanService  # Inicializa el servicio de Von Neumann
        self.mxc_service = MixedCongruenceService  # Inicializa el servicio de Congruencias Mixtas
    
    def run(self):
        #if self.model.connection is None:
            # Si la conexión a la base de datos es exitosa, se inicia la vista
        self.view.run()


    def on_generate_von_neumann(self): #REFACTORIZADO 
        # Obtener la semilla y la cantidad de dígitos desde la vista
        seed = self.vn_view.seed_entry.get()
        n_digits = self.vn_view.digits_entry.get()

        # Validar la semilla y la cantidad de dígitos
        if not self.vn_service.validate_seed_vn(seed):
            self.main_service.error_message("Error: La semilla debe tener exactamente 4 dígitos.", self.vn_view.result_textbox)
            return
        if not self.main_service.validate_digits(n_digits):
            self.main_service.error_message("Error: La cantidad de dígitos debe ser un número entero positivo menor a 10000.", self.vn_view.result_textbox)
            return
        
        # Llamar al método de la vista para generar números aleatorios (No suele llegar a ejecutarse por la generacion tan rapida)
        self.main_service.loading(self, self.vn_view.result_textbox)  # Mostrar mensaje de carga
        self.vn_view.generate_button.config(state="disabled")  # Deshabilitar el botón de generar

        # Aquí se llamaría al método de la base de datos para generar los números aleatorios
        random_numbers = self.vn_service.von_neuman_generator(seed, int(n_digits))
        self.main_service.paste_result(random_numbers, self.vn_view.result_textbox)
        self.vn_view.generate_button.config(state="normal")  # Habilitar el botón de generar nuevamente

    def on_generate_mixed(self): #REFACTORIZADO
        # Obtener la semilla y los parámetros desde la vista
        seed = self.mxc_view.seed_entry.get()
        a = self.mxc_view.a_entry.get()
        m = self.mxc_view.m_entry.get()
        c = self.mxc_view.c_entry.get()

        if not self.mxc_service.validate_mixed_parameters(seed, a, m, c):
            self.main_service.error_message("Error: Los parámetros A, M y C deben seguir las siguientes reglas:\n" + "A: Debe ser un entero impar, no divisible por 3 o 5.\n" + 
                               "C: Debe ser un entero impar, relativamente primo a M.\n" + 
                               "M: Debe ser un entero positivo, mayor que A y mayor que la Semilla.", self.mxc_view.result_textbox)
            return
        if not self.main_service.validate_digits(self.mxc_view.quantity_entry.get()):
            self.main_service.error_message("Error: La cantidad de dígitos debe ser un número entero positivo menor a 10000.", self.mxc_view.result_textbox)
            return
        
        # Llamar al método de la vista para generar números aleatorios (No suele llegar a ejecutarse por la generacion tan rapida)
        self.main_service.loading(self, self.mxc_view.result_textbox)
        self.mxc_view.generate_button.config(state="disabled")

        # Aquí se llamaría al método de la base de datos para generar los números aleatorios
        random_numbers = self.mxc_service.mixed_congruence_generator(int(seed), int(a), int(m), int(c), int(self.mxc_view.quantity_entry.get()))
        self.main_service.paste_result(random_numbers, self.mxc_view.result_textbox)
        self.mxc_view.generate_button.config(state="normal")


    def on_test_von_neumann(self):
        # Obtener el tipo de prueba seleccionada
        test_type = self.vn_view.test_type.get()
        view = self.vn_view
        match test_type:
            case "Chi Cuadrado":
                result = self.main_service.run_chi_square_test(view.result_textbox)
                if result:
                    MessageBox.show_info("Resultado", "La prueba Chi Cuadrado ha pasado.")
                    view.chi_radio.config(fg="green")
                elif result == False:
                    MessageBox.show_error("Resultado", "La prueba Chi Cuadrado no ha pasado.")
                    view.chi_radio.config(fg="red")
            case "Rachas":
                self.run_runs_test(view)

    def on_test_mixed(self):
        # Obtener el tipo de prueba seleccionada
        test_type = self.mxc_view.test_type.get()
        view = self.mxc_view
        match test_type:
            case "Chi Cuadrado":
                result = self.main_service.run_chi_square_test(view.result_textbox, view.test_result_textbox)
                if result:
                    MessageBox.show_info("Resultado", "La prueba Chi Cuadrado ha pasado.")
                    view.chi_radio.config(fg="green")
                elif result == False:
                    MessageBox.show_error("Resultado", "La prueba Chi Cuadrado no ha pasado.")
                    view.chi_radio.config(fg="red")
            case "Rachas":
                self.run_runs_test(view)