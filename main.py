import sys
from PyQt5.QtWidgets import QApplication
from controller.numGen_controller import NumGenController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = NumGenController()  # Creo una instancia del controlador
    controller.run()  # Ejecuta el método run del controlador
    sys.exit(app.exec_())  # Inicia el bucle de eventos de la aplicación