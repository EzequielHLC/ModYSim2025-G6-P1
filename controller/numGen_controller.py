from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer
from view.numGen_view import Ui_MainWindow
from service.main_service import MainService
from service.numGen_service import NumGenService
import os
import uuid


class NumGenController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.numGenService = NumGenService()
        self.mediaPlayer = QMediaPlayer()
    
        # Connect buttons to their respective functions
        self.ui.botonGenerar.clicked.connect(self.generate_numbers)
        self.ui.botonGuardarTxt.clicked.connect(self.export_txt)
        self.ui.botonTests.clicked.connect(self.change_TestWindow)
        self.ui.botonDistrib.clicked.connect(self.change_ClassWindow)
        self.ui.botonHidro.clicked.connect(self.change_HidroWindow)
    
    def run(self):
        self.show()

    def generate_numbers(self):
        self.ui.botonGuardarTxt.setEnabled(False)

        if self.ui.radioVonNeumann.isChecked():
            seed = self.ui.inputSemilla.text()
            n_digits = self.ui.inputCantidad.text()
            
            try:
                random_numbers = self.numGenService.generate_von_nuemann(seed, n_digits)
                digits = [int(d) for d in str(random_numbers) if d.isdigit()]
                self.ui.plainResultados.setPlainText(", ".join(map(str, digits)))
                self.ui.botonGuardarTxt.setEnabled(True)
                self.ui.inputNombre.setEnabled(True)
            except ValueError as e:
                MainService.show_message(str(e), "Error")
        
        elif self.ui.radioCongruencias.isChecked():
            seed = self.ui.inputSemilla.text()
            n_digits = self.ui.inputCantidad.text()
            a_value = self.ui.inputA.text()
            c_value = self.ui.inputC.text()
            m_value = self.ui.inputM.text()
            
            try:
                random_numbers = self.numGenService.generate_mixed_congruence(seed, n_digits, a_value, m_value, c_value)
                self.ui.plainResultados.setPlainText(", ".join(map(str, random_numbers)))
                self.ui.botonGuardarTxt.setEnabled(True)
                self.ui.inputNombre.setEnabled(True)
            except ValueError as e:
                MainService.show_message(str(e), "Error")
    
    def export_txt(self):
        # Exporto los resultados a un archivo de texto
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_folder, exist_ok=True)  # Me aseguro de que la carpeta existe

        if self.ui.inputNombre.text().strip() == "":
            random_id = uuid.uuid4().hex[:8]  # Generate a random 8-character ID
            file_name = os.path.join(data_folder, f"resultados_{random_id}.txt")
        else:
            file_name = os.path.join(data_folder, f"{self.ui.inputNombre.text()}.txt")

        # Guardo los resultados en el archivo
        with open(file_name, 'w') as file:
            file.write(self.ui.plainResultados.toPlainText().replace(", ", ""))
        MainService.show_message("¡Archivo guardado exitosamente!", "Éxito")

    def change_TestWindow(self):
        self.test_window = MainService.show_TestWindow()
        self.test_window.show()
        self.close()

    def change_ClassWindow(self):
        self.class_window = MainService.show_ClassWindow()
        self.class_window.show()
        self.close()
    
    def change_HidroWindow(self):
        self.hidro_window = MainService.show_HidroWindow()
        self.hidro_window.show()
        self.close()