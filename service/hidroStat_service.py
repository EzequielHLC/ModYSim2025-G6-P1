import math
from scipy.stats import norm
import os
import datetime
import base64
from io import BytesIO
from controller.dialog_controller import DialogController

class HidroStatService:

    def show_message(self, message, title="ATENCIÓN"):
        # Método para mostrar un mensaje en un cuadro de diálogo
        dialog = DialogController()
        dialog.ui.errorLabel.setText(message)
        dialog.ui.label.setText(title)
        dialog.run()

    def validate_input(self, LimInf, LimSup):
        if not LimInf.isdigit() or not LimSup.isdigit():
            return False
        else:
            return True
    
    def validate_intervalos(self, intervalos):
        if intervalos.isdigit():
            if int(intervalos) > 0:
                return True
            else:
                return False
        else:
            return False

    def validate_rango(self, rango):
        try:
            value = float(rango)
            if value > 0:
                return True
            else:
                return False
        except ValueError:
            return False
    
    def get_K_Intervalos(self, LimSup, LimInf):
        range = LimSup - LimInf
        k = 1 + math.log2(range)
        k = math.floor(k)
        return k
    
    def get_Amp_Clase(self, LimSup, LimInf, k_intervalos):
        range = LimSup - LimInf
        amplitud = range / k_intervalos
        amplitud = round(amplitud, 1)
        return amplitud
    
    def get_Clases(self, k, limInf, a):
        clases = []

        for i in range(k):
            li = limInf + i * a
            ls = li + a
            ls = round(ls, 2)
            li = round(li, 2)
            clases.append((li, ls))
        
        return clases
    
    def get_MarcasClase(self, clases):
        if len(clases) > 0:
            m_clases = []
            for clase in clases:
                marca = (clase[0] + clase[1]) / 2
                m_clases.append(round(marca, 2))
            return m_clases
        else:
            raise ValueError("No hay clases generadas para calcular las marcas de clase.")
        
    def get_probAcumuladas(self, clases, media, desv):
        prob_acumuladas = []

        for i in range(len(clases)):
            if i == len(clases) - 1:
                prob_acumuladas.append(1)
            else:
                z = (clases[i][1] - media) / desv
                prob_clase = norm.cdf(z)
                prob_acumuladas.append(round(prob_clase, 4))
        
        return prob_acumuladas
    
    def get_probPorClase(self, prob_acumuladas):
        prob_PorClase = []
        for i in range(len(prob_acumuladas)):
            if i == 0:
                prob_PorClase.append(round(prob_acumuladas[i], 4))
            else:
                prob = prob_acumuladas[i] - prob_acumuladas[i - 1]
                prob_PorClase.append(round(prob, 4))
        return prob_PorClase

    def get_RangosIndice(self, prob_acumuladas):
        rangoInSup = []

        for i in range(len(prob_acumuladas)):
            rango = round(prob_acumuladas[i]*10000)
            if rango >= 9999:
                rango = 9999
            rangoInSup.append(rango)
        
        rangosIndice = []

        for i in range(len(rangoInSup)):
            if i == 0:
                r_inf = 0
                r_sup = rangoInSup[i]
                rangosIndice.append((r_inf, r_sup))
                r_inf = r_sup + 1
            else:
                r_sup = rangoInSup[i]
                rangosIndice.append((r_inf, r_sup))
                r_inf = r_sup + 1

        return rangosIndice
    
    def get_MuestraConstruida(self, muestra):
        # Unir los números de self.muestra en números de 4 dígitos, rellenando con ceros si es necesario
        numeros = muestra[:]
        while len(numeros) % 4 != 0:
            numeros.append(0)
        numeros_4_digitos = [int(''.join(map(str, numeros[i:i+4]))) for i in range(0, len(numeros), 4)]

        return numeros_4_digitos
    
    def get_ProbObtenida(self, muestra_artificial, valores_obtenidos):
        esperados = [round((p / len(muestra_artificial)), 4) for p in valores_obtenidos]
        return esperados
    
    def get_ValoresObtenidos(self, muestra_artificial, rangos_indice):
        conteos = [0] * len(rangos_indice)
        for num in muestra_artificial:
            for idx, (r_inf, r_sup) in enumerate(rangos_indice):
                if r_inf <= num <= r_sup:
                    conteos[idx] += 1
                    break
        return conteos
    
    def get_MuestraContextual(self, muestra_artificial, media, desv, lim_inf):
        valores_transformados = []
        for num in muestra_artificial:
            num = num/10000
            z = norm.ppf(num)
            valor_t = media + (z * desv)
            try:
                valores_transformados.append(round(valor_t))
            except:
                valores_transformados.append(lim_inf)
        return valores_transformados
    
    def exportar_markdown(self, resultado):
        import matplotlib.pyplot as plt

        os.makedirs("./data/reports", exist_ok=True)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        filename = f"./data/reports/reporte_{now}.md"

        md = f"# 💧 Reporte Hidrológico de Caudales\n"
        md += f"🗓️ **Fecha de generación**: `{now}`\n\n"
        md += "---\n"

        md += "## 📐 Tabla de Rangos de Caudal\n"
        md += "| 💧 Rango de Caudal (m³/s) | 📍 Marca de Clase (m³/s) | 📊 Prob. Acumulada | 📈 Prob. Rango | 🎲 Rango Índice |\n"
        md += "|--------------------------|--------------------------|--------------------|----------------|-----------------|\n"
        for i in range(len(resultado["clases"])):
            rango = f"{resultado['clases'][i][0]} - {resultado['clases'][i][1]}"
            marca = resultado["marcas_clase"][i]
            prob_acum = resultado["prob_acumuladas"][i]
            prob_clase = resultado["prob_clase"][i]
            rango_indice = f"{resultado['rangos_indice'][i][0]} - {resultado['rangos_indice'][i][1]}"
            md += f"| {rango} | {marca} | {prob_acum:.4f} | {prob_clase:.4f} | {rango_indice} |\n"

        md += "\n## 📦 Resultados Obtenidos\n"
        md += "| 💧 Rango de Caudal (m³/s) | 📦 Frecuencia Observada | 📉 Prob. Observada |\n"
        md += "|--------------------------|------------------------|-------------------|\n"
        for i in range(len(resultado["clases"])):
            rango = f"{resultado['clases'][i][0]} - {resultado['clases'][i][1]}"
            valor = resultado["valores_obtenidos"][i]
            prob = resultado["prob_obtenida"][i]
            md += f"| {rango} | {valor} | {prob:.4f} |\n"

        md += "\n## 📊 Comparación: Probabilidad Esperada vs Observada\n"
        try:
            clases_labels = [f"{c[0]}-{c[1]}" for c in resultado["clases"]]
            prob_esperada = resultado["prob_clase"]
            prob_obtenida = resultado["prob_obtenida"]

            plt.figure(figsize=(8, 4))
            x = range(len(clases_labels))
            plt.bar(x, prob_esperada, width=0.4, label="Esperada", align='center', alpha=0.7)
            plt.bar([i + 0.4 for i in x], prob_obtenida, width=0.4, label="Observada", align='center', alpha=0.7)
            plt.xticks([i + 0.2 for i in x], clases_labels, rotation=45)
            plt.xlabel("Rango de Caudal (m³/s)")
            plt.ylabel("Probabilidad")
            plt.title("Probabilidad Esperada vs Observada por Rango de Caudal")
            plt.legend()
            plt.tight_layout()
            plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.4f}"))

            buf = BytesIO()
            plt.savefig(buf, format="png")
            plt.close()
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            md += f"![Comparación Probabilidad](data:image/png;base64,{img_base64})\n"
        except Exception as e:
            md += f"_No se pudo generar el gráfico: {e}_\n"

        md += "---\n"
        muestra = resultado.get("muestra_contextual", [])
        media = resultado.get("media", None)
        marcas_clase = resultado.get("marcas_clase", [])
        max_marca = max(marcas_clase) if marcas_clase else None
        min_marca = min(marcas_clase) if marcas_clase else None

        if muestra:
            max_val = max(muestra)
            min_val = min(muestra)
            pos_max = muestra.index(max_val) + 1  # Día desde 1
            pos_min = muestra.index(min_val) + 1
            promedio = round(sum(muestra) / len(muestra), 2)
            # Cuántas veces se superó la marca de clase más alta
            veces_sobre_max_marca = sum(1 for v in muestra if max_marca is not None and v > max_marca)
            # Cuántas veces se superó la media
            veces_sobre_media = sum(1 for v in muestra if media is not None and v > media)
            # Cuántas veces estuvo por debajo de la marca de clase más baja
            veces_bajo_min_marca = sum(1 for v in muestra if min_marca is not None and v < min_marca)
        else:
            max_val = min_val = pos_max = pos_min = promedio = veces_sobre_max_marca = veces_sobre_media = veces_bajo_min_marca = "N/A"

        md += "## 📌 Resumen Estadístico de la Muestra\n"
        md += f"- 🔢 Total de días: `{len(muestra)}`\n"
        md += f"- 📈 Caudal máximo: `{max_val} m³/s` (día {pos_max})\n"
        md += f"- 📉 Caudal mínimo: `{min_val} m³/s` (día {pos_min})\n"
        md += f"- 📊 Promedio de caudal: `{promedio} m³/s`\n"
        md += f"- 🚩 Días sobre la marca de caudal más alta: `{veces_sobre_max_marca}`\n"
        md += f"- 🚩 Días sobre la media: `{veces_sobre_media}`\n"
        md += f"- 🚩 Días bajo la marca de caudal más baja: `{veces_bajo_min_marca}`\n"

        md += "\n## 🧪 Muestra Contextual (Caudales diarios en m³/s)\n"
        if muestra:
            columnas = 10
            md += "\n| " + " | ".join([f"<span style='color:#2A4759'><b>Día {i+1}</b></span>" for i in range(columnas)]) + " |\n"
            md += "|" + "|".join(["------"] * columnas) + "|\n"
            for i in range(0, len(muestra), columnas):
                indices = [f"<span style='color:#2A4759'><b>{j+1}</b></span>" for j in range(i, min(i+columnas, len(muestra)))]
                valores = [f"{muestra[j]} m³/s" for j in range(i, min(i+columnas, len(muestra)))]
                while len(indices) < columnas:
                    indices.append("")
                    valores.append("")
                md += "| " + " | ".join(indices) + " |\n"
                md += "| " + " | ".join(valores) + " |\n"
        else:
            md += "_No se generó una muestra contextual._\n"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(md)

        return True