from PyQt5.QtWidgets import *
from view.dialogH_view import Ui_Dialog

class DialogController(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def run(self):
        self.exec_()