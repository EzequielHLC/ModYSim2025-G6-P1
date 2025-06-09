import sys
from PyQt5.QtWidgets import QApplication
from controller.numGen_controller import NumGenController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = NumGenController()
    controller.run()
    sys.exit(app.exec_())