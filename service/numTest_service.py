from service.main_service import MainService
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from scipy import stats
import math

class NumTestService:

    def run_chi_square_test(self, numbers, input_significance):
        # Obtener los números generados desde la vista 
        numbers = [int(num.strip()) for num in numbers if num.strip().isdigit()]
        if len(numbers) == 0:
            MainService.show_message("No se han encontrado números generados.", "Error")
            return
        input_significance = input_significance.replace(",", ".")
        significance_level = float(input_significance)

        # Calcular la frencuencia esperada
        frec_esperada = len(numbers) / 10

        # Calcular la frecuencia observada
        frec_observada = [0] * 10
        for num in numbers:
            if 0 <= num < 10:
                frec_observada[num] += 1
        
        # Calcular el estadístico de chi cuadrado
        chi_square = sum((frec_observada[i] - frec_esperada) ** 2 / frec_esperada for i in range(10))

        # Calcular los grados de libertad
        grados_libertad = 9
        # Calcular el valor crítico de chi cuadrado
        alpha = 1 - significance_level
        chi_square_critical = stats.chi2.ppf(alpha, grados_libertad)

        # Preparar los datos para la QTableView
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Número", 
            "Frecuencia Observada", 
            "Frecuencia Esperada"
        ])

        # Agregar filas para cada número (0-9)
        for i in range(10):
            row = [
            QStandardItem(str(i)),
            QStandardItem(str(frec_observada[i])),
            QStandardItem(f"{frec_esperada:.2f}")
            ]
            model.appendRow(row)

        # Agregar una fila vacía como separador
        model.appendRow([QStandardItem("") for _ in range(3)])

        # Agregar resultados del test
        model.appendRow([
            QStandardItem("Chi-cuadrado"),
            QStandardItem(f"{chi_square:.4f}"),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Valor crítico"),
            QStandardItem(f"{chi_square_critical:.4f}"),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Significancia"),
            QStandardItem(f"{significance_level:.4f}"),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Grados de libertad"),
            QStandardItem(str(grados_libertad)),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Resultado"),
            QStandardItem("Se acepta H0" if chi_square < chi_square_critical else "Se rechaza H0"),
            QStandardItem("")
        ])

        return model

    def run_runs_test(self, numbers, input_significance):
        # Obtener los números generados desde la vista
        numbers = [int(num.strip()) for num in numbers if num.strip().isdigit()]
        if len(numbers) == 0:
            MainService.show_message("No se han encontrado números generados.", "Error")
            return
        input_significance = input_significance.replace(",", ".")
        significance_level = float(input_significance)

        # Calcular los bits necesarios para representar el número más grande y convertir los números a binario
        min_bits = math.log2(max(numbers) + 1)
        min_bits = math.ceil(min_bits)
        bits_string = ""
        for number in numbers:
            number = format(number, f'0{min_bits}b')
            bits_string += str(number)
        
        # Contar los bits 0 y 1 y el total de bits
        count_0 = bits_string.count("0")
        count_1 = bits_string.count("1")
        total = len(bits_string)

        # Calcular el número de rachas
        runs = 0
        prev_bit = None
        for bit in bits_string:
            if prev_bit is not None and bit != prev_bit:
                runs += 1
            prev_bit = bit

        # Calcular el número esperado de rachas
        mu = ((2*count_0*count_1)/total) + 1
        num = 2 * count_0 * count_1 * (2 * count_0 * count_1 - total)
        den = total**2 * (total - 1)
        variance = num / den
        std_dev = math.sqrt(variance)

        # Calcular el valor crítico de z
        z = abs((runs - mu)/std_dev)
        z_crit = stats.norm.ppf(1 - significance_level / 2)

        # Preparar los datos para la QTableView
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([
            "Descripción",
            "Valor",
            ""
        ])

        model.appendRow([
            QStandardItem("Número de rachas"),
            QStandardItem(str(runs)),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Cantidad de 0"),
            QStandardItem(str(count_0)),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Cantidad de 1"),
            QStandardItem(str(count_1)),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Z calculado"),
            QStandardItem(f"{z:.4f}"),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Z crítico"),
            QStandardItem(f"{z_crit:.4f}"),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Significancia"),
            QStandardItem(f"{significance_level:.4f}"),
            QStandardItem("")
        ])
        model.appendRow([
            QStandardItem("Resultado"),
            QStandardItem("Se acepta H0" if z < z_crit else "Se rechaza H0"),
            QStandardItem("")
        ])

        return model