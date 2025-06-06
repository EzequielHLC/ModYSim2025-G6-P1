import sys
from PyQt5.QtWidgets import QApplication
from controller.hidroStat_controller import HidroStatController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = HidroStatController()
    controller.run()
    sys.exit(app.exec_())