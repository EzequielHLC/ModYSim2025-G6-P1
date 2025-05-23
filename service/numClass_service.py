from service.main_service import MainService
import math

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