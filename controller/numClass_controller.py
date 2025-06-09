from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel, Qt
from view.numClass_view import Ui_MainWindow
from service.numClass_service import NumClassService
from service.main_service import MainService
import os
import math
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

class NumClassController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.numClassService = NumClassService()
        self.muestra = []
        self.resultado = []

        self.ui.botonGenerador.clicked.connect(self.change_GenWindow)
        self.ui.botonTests.clicked.connect(self.change_TestWindow)
        self.ui.botonGenerarMarcas.clicked.connect(self.gen_MarcasClase)
        self.ui.listaNumGuardados.clicked.connect(self.preview_numbers_and_reset)
        self.ui.botonGenerarReporte.clicked.connect(self.gen_Report)
        self.ui.botonHidro.clicked.connect(self.change_HidroWindow)
        self.get_GeneratedNumbers()

    def run(self):
        self.show()

    def gen_MarcasClase(self):
        # Validar muestra:
        if not self.muestra:
            MainService.show_message("Debe seleccionar una muestra primero.", "Error")
            return

        # Parte 1: Validación de los límites

        limInf = self.ui.inputLimInf.text()
        limSup = self.ui.inputLimSup.text()

        if not self.numClassService.validate_input(limInf, limSup):
            MainService.show_message("Los límites deben ser números enteros.", "Error")
            return
        limInf = float(limInf)
        limSup = float(limSup)
        if limInf >= limSup:
            MainService.show_message("El límite inferior debe ser menor que el límite superior.", "Error")
            return
        
        # Parte 2: Llamada a la función pertinente
        if self.ui.radioBernoulli.isChecked():
            result = self.gen_MarcasClaseBernoulli(limInf, limSup)
            self.resultado = result  # Guardar el resultado para el reporte
            self.set_tabla_clases(
                result['clases'],
                result['marcas_clase'],
                result['prob_clase'],
                result['prob_acumuladas'],
                result['rangos_indice']
            )
            self.set_tabla_muestra(result['prob_obtenida'], result['valores_obtenidos'])

        
        elif self.ui.radioNormal.isChecked():
            media = self.ui.inputMediaN.text()
            desv = self.ui.inputStDevN.text()
            k = self.ui.inputNumClases.text()
            a = self.ui.inputAmpClases.text()

            if not (media.replace('.', '', 1).isdigit() and desv.replace('.', '', 1).isdigit()):
                MainService.show_message("La media y el desvío deben ser números.", "Error")
                return
            media = float(media)
            desv = float(desv)
            if desv <= 0:
                MainService.show_message("El desvío debe ser mayor a cero.", "Error")
                return
            
            # Validar k (número de clases)
            if k.strip() != "":
                if not k.isdigit() or int(k) <= 0:
                    MainService.show_message("El número de clases debe ser un entero mayor a cero.", "Error")
                    return
                k = int(k)
            else:
                k = None

            # Validar a (amplitud de clase)
            if a.strip() != "":
                try:
                    a_val = float(a)
                    if a_val <= 0:
                        MainService.show_message("La amplitud de clase debe ser mayor a cero.", "Error")
                        return
                    a = a_val
                except ValueError:
                    MainService.show_message("La amplitud de clase debe ser un número.", "Error")
                    return
            else:
                a = None
            
            result = self.gen_MarcasClaseNormal(limInf, limSup, media, desv, k, a)
            self.resultado = result  # Guardar el resultado para el reporte
            self.set_tabla_clases(
                result['clases'],
                result['marcas_clase'],
                result['prob_acumuladas'],
                result['prob_acumuladas'],
                result['rangos_indice']
            )
            self.set_tabla_muestra(result['prob_obtenida'], result['valores_obtenidos'])

    def gen_MarcasClaseBernoulli(self, limInf, limSup):
        n = limSup - limInf
        k = 2
        a = round((n/k), 1)

        clases = self.numClassService.get_Clases(k, limInf, a)
        marcas_clase = self.numClassService.get_MarcasClase(clases)
        prob_acumuladas = [0.5, 1]
        prob_clase = [0.5, 0.5]
        rangos_indice = self.numClassService.get_RangosIndice(prob_acumuladas)
        muestra_artificial = self.numClassService.get_MuestraConstruida(self.muestra)
        valores_obtenidos = self.numClassService.get_ValoresObtenidos(muestra_artificial, rangos_indice)
        prob_obtenida = self.numClassService.get_ProbObtenida(muestra_artificial, valores_obtenidos)

        return {
            "clases": clases,
            "marcas_clase": marcas_clase,
            "prob_acumuladas": prob_acumuladas,
            "prob_clase": prob_clase,
            "rangos_indice": rangos_indice,
            "valores_obtenidos": valores_obtenidos,
            "prob_obtenida": prob_obtenida
        }
        
    def gen_MarcasClaseNormal(self, limInf, limSup, media, desv, k, a):
        if k == None:
            k = self.numClassService.get_K_Intervalos(limSup, limInf)
        if a == None:
            a = self.numClassService.get_Amp_Clase(limSup, limInf, k)
        
        clases = self.numClassService.get_Clases(k, limInf, a)
        marcas_clase = self.numClassService.get_MarcasClase(clases)
        prob_acumuladas = self.numClassService.get_probAcumuladas(clases, media, desv)
        prob_clase = self.numClassService.get_probPorClase(prob_acumuladas)
        rangos_indice = self.numClassService.get_RangosIndice(prob_acumuladas)
        muestra_artificial = self.numClassService.get_MuestraConstruida(self.muestra)
        valores_obtenidos = self.numClassService.get_ValoresObtenidos(muestra_artificial, rangos_indice)
        prob_obtenida = self.numClassService.get_ProbObtenida(muestra_artificial, valores_obtenidos)
        muestra_contextual = self.numClassService.get_MuestraContextual(muestra_artificial, media, desv, limInf)

        return {
            "clases": clases,
            "marcas_clase": marcas_clase,
            "prob_acumuladas": prob_acumuladas,
            "prob_clase": prob_clase,
            "rangos_indice": rangos_indice,
            "valores_obtenidos": valores_obtenidos,
            "prob_obtenida": prob_obtenida,
            "muestra_contextual": muestra_contextual
        }

    def set_tabla_clases(self, clases, marcas_clase, prob_clase, prob_acumuladas, rangos_indice):
        rows = 4
        cols = len(clases)
        model = QStandardItemModel(rows, cols)
        for i, (li, ls) in enumerate(clases):
            model.setHeaderData(i, Qt.Horizontal, f"Clase {i+1}\n[{li}, {ls}]")
        for i, marca in enumerate(marcas_clase):
            model.setItem(0, i, QStandardItem(f"{marca}"))
        model.setVerticalHeaderItem(0, QStandardItem("Marca de Clase"))
        for i, prob in enumerate(prob_clase):
            model.setItem(1, i, QStandardItem(f"{prob}"))
        model.setVerticalHeaderItem(1, QStandardItem("Prob. Clase"))
        for i, prob_acumulada in enumerate(prob_acumuladas):
            model.setItem(2, i, QStandardItem(f"{prob_acumulada}"))
        model.setVerticalHeaderItem(2, QStandardItem("Prob. Acumulada"))
        for i, rango in enumerate(rangos_indice):
            model.setItem(3, i, QStandardItem(f"{rango}"))
        model.setVerticalHeaderItem(3, QStandardItem("Rango Índice"))
        self.ui.tablaResClases.setModel(model)
        self.ui.tablaResClases.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def set_tabla_muestra(self, prob_obtenida, valores_obtenidos):
        model2 = QStandardItemModel(2, len(prob_obtenida))
        model2.setVerticalHeaderItem(0, QStandardItem("Prob. Obtenidas"))
        model2.setVerticalHeaderItem(1, QStandardItem("Val. Obtenidos"))
        for i, (ve, vo) in enumerate(zip(prob_obtenida, valores_obtenidos)):
            model2.setItem(0, i, QStandardItem(f"{ve}"))
            model2.setItem(1, i, QStandardItem(f"{vo}"))
            model2.setHeaderData(i, Qt.Horizontal, f"Clase {i+1}")
        self.ui.tablaResMuestra.setModel(model2)
        self.ui.tablaResMuestra.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_GeneratedNumbers(self):
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data', 'tested')
        txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
        model = QStringListModel(txt_files)
        self.ui.listaNumGuardados.setModel(model)

    def gen_Report(self):
        if not self.resultado:
            MainService.show_message("Debe generar las marcas de clase primero.", "Error")
            return
        if self.numClassService.exportar_markdown(self.resultado):
            MainService.show_message("Reporte generado exitosamente.", "Éxito")
        else:
            MainService.show_message("Error al generar el reporte.", "Error")
        
    def preview_numbers_and_reset(self):
        selected_file = self.ui.listaNumGuardados.currentIndex().data()
        if selected_file:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tested', selected_file)
            with open(file_path, 'r') as file:
                content = file.read()
                digits = [int(d) for d in content if d.isdigit()]
                self.muestra = digits

                # Obtener fecha de modificación del archivo
                file_stat = os.stat(file_path)
                fecha = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                numeros = digits[:]
                while len(numeros) % 4 != 0:
                    numeros.append(0)
                num_by_4 = [int(''.join(map(str, numeros[i:i+4]))) for i in range(0, len(numeros), 4)]

                self.ui.detalleMuestraNombre.setText(f"Nombre de la muestra: {selected_file}")
                self.ui.detalleMuestraElementos.setText(f"Cantidad de elementos: {len(num_by_4)}")
                self.ui.detalleMuestraFecha.setText(f"Fecha: {fecha}")

    def change_GenWindow(self):
        self.gen_window = MainService.show_GenWindow()
        self.gen_window.show()
        self.close()

    def change_TestWindow(self):
        self.test_window = MainService.show_TestWindow()
        self.test_window.show()
        self.close()

    def change_HidroWindow(self):
        self.hidro_window = MainService.show_HidroWindow()
        self.hidro_window.show()
        self.close()