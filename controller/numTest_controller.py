from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from view.numTest_view import Ui_MainWindow
# from controller.numGen_controller import NumGenController
from service.main_service import MainService
from service.numTest_service import NumTestService
import os

class NumTestController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.numTestService = NumTestService()

        # Connect buttons to their respective functions
        self.ui.botonGenerador.clicked.connect(self.change_GenWindow)
        self.ui.botonDistrib.clicked.connect(self.change_ClassWindow)
        self.ui.listaNumGuardados.clicked.connect(self.preview_numbers_and_reset)
        self.ui.botonIniciarTest.clicked.connect(self.run_test)
        self.ui.botonDescartar.clicked.connect(self.discard_numbers)
        self.ui.botonGuardarBD.clicked.connect(self.save_testedNumbers)
        self.ui.botonHidro.clicked.connect(self.change_HidroWindow)
        self.get_GeneratedNumbers()

    def run(self):
        self.show()
    
    def get_GeneratedNumbers(self):
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
        txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
        model = QStringListModel(txt_files)
        self.ui.listaNumGuardados.setModel(model)

    def preview_numbers_and_reset(self):
        selected_file = self.ui.listaNumGuardados.currentIndex().data()
        if selected_file:
            self.ui.plainPrevistaNum.clear()
            self.ui.plainPrevistaNum.setPlainText("")
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', selected_file)
            with open(file_path, 'r') as file:
                content = file.read()
                digits = [int(d) for d in content if d.isdigit()]
                self.ui.plainPrevistaNum.setPlainText(", ".join(map(str, digits)))
                self.ui.checkChiCuadrado.setChecked(False)
                self.ui.checkRachas.setChecked(False)
                self.ui.botonGuardarBD.setEnabled(False)
                self.ui.lineResultado.setText("Sin resultados aún...")
                self.ui.lineResultado.setStyleSheet("color: #888888; border: 2px solid #F79B72; background-color: #DDDDDD; padding: 4px; border-radius: 5px;")
                self.ui.tablaResultados.setModel(QStandardItemModel())
                self.ui.botonDescartar.setEnabled(True)
        else:
            self.ui.plainPrevistaNum.clear()
            self.ui.botonDescartar.setEnabled(False)

    def run_test(self):
        if self.ui.radioChiCuadrado.isChecked():
            numbers = self.ui.plainPrevistaNum.toPlainText()
            resultado = self.numTestService.run_chi_square_test(numbers, self.ui.inputSignificancia.text())
            
            if resultado:
                self.ui.tablaResultados.setModel(resultado)
                self.ui.tablaResultados.resizeColumnsToContents()
                self.ui.lineResultado.setText(f"Resultado de la prueba: {resultado.itemFromIndex(resultado.index(15, 1)).text()}")
                
                if float(resultado.itemFromIndex(resultado.index(11, 1)).text()) < float(resultado.itemFromIndex(resultado.index(12, 1)).text()):
                    self.ui.lineResultado.setStyleSheet("color: #FFFFFF; border: 2px solid #F79B72; background-color: #319c00; padding: 4px; border-radius: 5px;")
                    self.ui.checkChiCuadrado.setChecked(True)
                else:
                    self.ui.lineResultado.setStyleSheet("color: #FFFFFF; border: 2px solid #F79B72; background-color: #EB5B00; padding: 4px; border-radius: 5px;")
                    self.ui.checkChiCuadrado.setChecked(False)
        
        elif self.ui.radioRachas.isChecked():
            numbers = self.ui.plainPrevistaNum.toPlainText()
            resultado = self.numTestService.run_runs_test(numbers, self.ui.inputSignificancia.text())
            
            if resultado:
                self.ui.tablaResultados.setModel(resultado)
                self.ui.tablaResultados.resizeColumnsToContents()
                self.ui.lineResultado.setText(f"Resultado de la prueba: {resultado.itemFromIndex(resultado.index(6, 1)).text()}")
                
                if float(resultado.itemFromIndex(resultado.index(4, 1)).text()) > float(resultado.itemFromIndex(resultado.index(3, 1)).text()):
                    self.ui.lineResultado.setStyleSheet("color: #FFFFFF; border: 2px solid #F79B72; background-color: #319c00; padding: 4px; border-radius: 5px;")
                    self.ui.checkRachas.setChecked(True)
                else:
                    self.ui.lineResultado.setStyleSheet("color: #FFFFFF; border: 2px solid #F79B72; background-color: #EB5B00; padding: 4px; border-radius: 5px;")
                    self.ui.checkRachas.setChecked(False)
        
        if self.ui.checkChiCuadrado.isChecked() and self.ui.checkRachas.isChecked():
            self.ui.botonGuardarBD.setEnabled(True)
        else:
            self.ui.botonGuardarBD.setEnabled(False)

    def discard_numbers(self):
        if MainService.show_conf_message("¿Está seguro de que desea descartar los números generados?", "ATENCIÓN"):
            selected_file = self.ui.listaNumGuardados.currentIndex().data()
            try:
                file_path = os.path.join(os.path.dirname(__file__), '..', 'data', selected_file)
                os.remove(file_path)
                self.get_GeneratedNumbers()
                MainService.show_message("Los números generados han sido descartados.", "Éxito")
                self.ui.plainPrevistaNum.clear()
                self.ui.plainPrevistaNum.setPlainText("")
                self.ui.checkChiCuadrado.setChecked(False)
                self.ui.checkRachas.setChecked(False)
                self.ui.botonGuardarBD.setEnabled(False)
                self.ui.lineResultado.setText("Sin resultados aún...")
                self.ui.lineResultado.setStyleSheet("color: #888888; border: 2px solid #F79B72; background-color: #DDDDDD; padding: 4px; border-radius: 5px;")
                self.ui.tablaResultados.setModel(QStandardItemModel())
                self.ui.botonDescartar.setEnabled(False)
                self.get_GeneratedNumbers()
            except Exception as e:
                MainService.show_message(f"Error al eliminar el archivo: {e}", "Error")

    def save_testedNumbers(self):
        selected_file = self.ui.listaNumGuardados.currentIndex().data()
        if selected_file:
            src_path = os.path.join(os.path.dirname(__file__), '..', 'data', selected_file)
            dest_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'tested')
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, selected_file)
            try:
                os.rename(src_path, dest_path)
                MainService.show_message("Archivo movido a la carpeta 'tested'.", "Éxito")
                self.get_GeneratedNumbers()
                self.ui.plainPrevistaNum.clear()
                self.ui.checkChiCuadrado.setChecked(False)
                self.ui.checkRachas.setChecked(False)
                self.ui.botonGuardarBD.setEnabled(False)
                self.ui.lineResultado.setText("Sin resultados aún...")
                self.ui.lineResultado.setStyleSheet("color: #888888; border: 2px solid #F79B72; background-color: #DDDDDD; padding: 4px; border-radius: 5px;")
                self.ui.tablaResultados.setModel(QStandardItemModel())
                self.ui.botonDescartar.setEnabled(False)
            except Exception as e:
                MainService.show_message(f"Error al mover el archivo: {e}", "Error")

    def change_GenWindow(self):
        self.gen_window = MainService.show_GenWindow()
        self.gen_window.show()
        self.close()
    
    def change_ClassWindow(self):
        self.class_window = MainService.show_ClassWindow()
        self.class_window.show()
        self.close()

    def change_HidroWindow(self):
        self.hidro_window = MainService.show_HidroWindow()
        self.hidro_window.show()
        self.close()