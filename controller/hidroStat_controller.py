from PyQt5.QtWidgets import *
from service.hidroStat_service import HidroStatService
from view.hidroStat_view import Ui_MainWindow
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import os
from datetime import datetime, timedelta

class HidroStatController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hidroStatService = HidroStatService()
        self.muestra = []
        self.resultado = []

        self.get_GeneratedNumbers()
        self.ui.listaNumGuardados.clicked.connect(self.preview_numbers_and_reset)
        self.ui.botonGenerarMarcas.clicked.connect(self.gen_MarcasClase)
        self.ui.botonGenerarReporte.clicked.connect(self.gen_Report)

    def run(self):
        self.show() 
    
    def gen_MarcasClase(self):
        # Validar muestra:
        if not self.muestra:
            self.hidroStatService.show_message("Debe seleccionar una muestra primero.", "Error")
            return

        # Parte 1: Validación de los límites

        limInf = self.ui.inputLimInf.text()
        limSup = self.ui.inputLimSup.text()

        if not self.hidroStatService.validate_input(limInf, limSup):
            self.hidroStatService.show_message("Los límites deben ser números enteros.", "Error")
            return
        limInf = float(limInf)
        limSup = float(limSup)
        if limInf >= limSup:
            self.hidroStatService.show_message("El límite inferior debe ser menor que el límite superior.", "Error")
            return
        else:
            media = self.ui.inputMediaN.text()
            desv = self.ui.inputStDevN.text()
            k = self.ui.inputNumClases.text()
            a = self.ui.inputAmpClases.text()

            if not (media.replace('.', '', 1).isdigit() and desv.replace('.', '', 1).isdigit()):
                self.hidroStatService.show_message("La media y el desvío deben ser números.", "Error")
                return
            media = float(media)
            desv = float(desv)
            if desv <= 0:
                self.hidroStatService.show_message("El desvío debe ser mayor a cero.", "Error")
                return
            
            # Validar k (número de clases)
            if k.strip() != "":
                if not k.isdigit() or int(k) <= 0:
                    self.hidroStatService.show_message("El número de clases debe ser un entero mayor a cero.", "Error")
                    return
                k = int(k)
            else:
                k = None

            # Validar a (amplitud de clase)
            if a.strip() != "":
                try:
                    a_val = float(a)
                    if a_val <= 0:
                        self.hidroStatService.show_message("La amplitud de clase debe ser mayor a cero.", "Error")
                        return
                    a = a_val
                except ValueError:
                    self.hidroStatService.show_message("La amplitud de clase debe ser un número.", "Error")
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
        
    def set_tabla_clases(self, clases, marcas_clase, prob_clase, prob_acumuladas, rangos_indice):
        rows = 4
        cols = len(clases)
        model = QStandardItemModel(rows, cols)
        for i, (li, ls) in enumerate(clases):
            model.setHeaderData(i, Qt.Horizontal, f"Rango de Caudal {i+1}\n[{li}, {ls}]")
        for i, marca in enumerate(marcas_clase):
            model.setItem(0, i, QStandardItem(f"{marca}"))
        model.setVerticalHeaderItem(0, QStandardItem("Marca de Caudal"))
        for i, prob in enumerate(prob_clase):
            model.setItem(1, i, QStandardItem(f"{prob}"))
        model.setVerticalHeaderItem(1, QStandardItem("Prob. Caudal"))
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
            model2.setHeaderData(i, Qt.Horizontal, f"Rango de Caudal {i+1}")
        self.ui.tablaResMuestra.setModel(model2)
        self.ui.tablaResMuestra.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_GeneratedNumbers(self):
        data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
        txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
        model = QStringListModel(txt_files)
        self.ui.listaNumGuardados.setModel(model)
    
    def preview_numbers_and_reset(self):
        selected_file = self.ui.listaNumGuardados.currentIndex().data()
        if selected_file:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'data', selected_file)
            with open(file_path, 'r') as file:
                content = file.read()
                digits = [int(d) for d in content if d.isdigit()]
                self.muestra = digits

                # Obtener fecha de modificación del archivo
                file_stat = os.stat(file_path)
                fecha = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d')

                numeros = digits[:]
                while len(numeros) % 4 != 0:
                    numeros.append(0)
                num_by_4 = [int(''.join(map(str, numeros[i:i+4]))) for i in range(0, len(numeros), 4)]

                fecha_init_dt = datetime.fromtimestamp(file_stat.st_mtime) - timedelta(days=len(num_by_4))
                fecha_init = fecha_init_dt.strftime('%Y-%m-%d')

                self.ui.detalleMuestraNombre.setText(f"Código de Muestreo: {selected_file}")
                self.ui.detalleMuestraElementos.setText(f"Días de Muestra: {len(num_by_4)}")
                self.ui.detalleMuestraFecha.setText(f"Periodo: {fecha_init} - {fecha}")

    def gen_MarcasClaseNormal(self, limInf, limSup, media, desv, k, a):
        if k == None:
            k = self.hidroStatService.get_K_Intervalos(limSup, limInf)
        if a == None:
            a = self.hidroStatService.get_Amp_Clase(limSup, limInf, k)
        
        clases = self.hidroStatService.get_Clases(k, limInf, a)
        marcas_clase = self.hidroStatService.get_MarcasClase(clases)
        prob_acumuladas = self.hidroStatService.get_probAcumuladas(clases, media, desv)
        prob_clase = self.hidroStatService.get_probPorClase(prob_acumuladas)
        rangos_indice = self.hidroStatService.get_RangosIndice(prob_acumuladas)
        muestra_artificial = self.hidroStatService.get_MuestraConstruida(self.muestra)
        valores_obtenidos = self.hidroStatService.get_ValoresObtenidos(muestra_artificial, rangos_indice)
        prob_obtenida = self.hidroStatService.get_ProbObtenida(muestra_artificial, valores_obtenidos)
        muestra_contextual = self.hidroStatService.get_MuestraContextual(muestra_artificial, media, desv, limInf)

        return {
            "clases": clases,
            "marcas_clase": marcas_clase,
            "prob_acumuladas": prob_acumuladas,
            "prob_clase": prob_clase,
            "rangos_indice": rangos_indice,
            "valores_obtenidos": valores_obtenidos,
            "prob_obtenida": prob_obtenida,
            "muestra_contextual": muestra_contextual,
            "media": media,
            "desvio": desv
        }
    
    def gen_Report(self):
        if not self.resultado:
            self.hidroStatService.show_message("Debe generar las marcas de clase primero.", "Error")
            return
        if self.hidroStatService.exportar_markdown(self.resultado):
            self.hidroStatService.show_message("Reporte generado exitosamente.", "Éxito")
        else:
            self.hidroStatService.show_message("Error al generar el reporte.", "Error")