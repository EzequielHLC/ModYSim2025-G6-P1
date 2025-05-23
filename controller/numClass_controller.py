from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
from view.numClass_view import Ui_MainWindow
from service.numClass_service import NumClassService
from service.main_service import MainService
import os
import math

class NumClassController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.numClassService = NumClassService()

        self.ui.botonGenerador.clicked.connect(self.change_GenWindow)
        self.ui.botonTests.clicked.connect(self.change_TestWindow)
        self.ui.botonGenerarMarcas.clicked.connect(self.gen_MarcasClase)
        self.get_GeneratedNumbers()

    def run(self):
        self.show()
    
    def gen_MarcasClase(self):

        # Parte 1: Validación de los límites

        LimInf = self.ui.inputLimInf.text()
        LimSup = self.ui.inputLimSup.text()

        if not self.numClassService.validate_input(LimInf, LimSup):
            MainService.show_message("Los límites deben ser números enteros.", "Error")
            return
        LimInf = float(LimInf)
        LimSup = float(LimSup)
        if LimInf >= LimSup:
            MainService.show_message("El límite inferior debe ser menor que el límite superior.", "Error")
            return
        
        # Parte 2: Validación de los intervalos y el rango, si se ingresan

        k_intervalos = self.ui.inputNumClases.text()
        amplitud = self.ui.inputAmpClases.text()

        if k_intervalos.strip() != "":
            if not self.numClassService.validate_intervalos(k_intervalos):
                MainService.show_message("Los intervalos y el rango deben ser números enteros, mayores a cero.", "Error")
                return
            k_intervalos = int(k_intervalos)
        else:
            k_intervalos = self.numClassService.get_K_Intervalos(LimSup, LimInf)

        if amplitud.strip() != "":
            if not self.numClassService.validate_rango(amplitud):
                MainService.show_message("Los intervalos y el rango deben ser números enteros, mayores a cero.", "Error")
                return
            amplitud = float(amplitud)
        else:
            amplitud = self.numClassService.get_Amp_Clase(LimSup, LimInf, k_intervalos)

        # Parte 3: Generación de las marcas de clase y sus marcas
    
        clases = []
        for i in range(k_intervalos):
            li = LimInf + i * amplitud
            ls = li + amplitud
            clases.append((li, ls))

   
        marcas_clase = []
        for clase in clases:
            marca = (clase[0] + clase[1]) / 2
            marcas_clase.append(marca)
        
        

        print("Número de intervalos: ", k_intervalos)
        print("Amplitud de clase: ", amplitud)
        print("Rango: ", LimSup - LimInf)
        print("Clases: ", clases)
        print("Marcas de Clase: ", marcas_clase)
        

    def get_GeneratedNumbers(self):
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
        txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
        model = QStringListModel(txt_files)
        self.ui.listaNumGuardados.setModel(model)

    def change_GenWindow(self):
        self.gen_window = MainService.show_GenWindow()
        self.gen_window.show()
        self.close()

    def change_TestWindow(self):
        self.test_window = MainService.show_TestWindow()
        self.test_window.show()
        self.close()