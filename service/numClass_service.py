from service.main_service import MainService
import math
from scipy.stats import norm

class NumClassService:

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
            clases.append((li, ls))
        
        return clases
    
    def get_MarcasClase(self, clases):
        if len(clases) > 0:
            m_clases = []
            for clase in clases:
                marca = (clase[0] + clase[1]) / 2
                m_clases.append(marca)
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
    
    def get_ValoresEsperados(self, muestra_artificial, probabilidades):
        esperados = [p * len(muestra_artificial) for p in probabilidades]
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