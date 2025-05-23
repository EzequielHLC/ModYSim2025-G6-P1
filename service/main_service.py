from view.message_box import MessageBox
from model.database import Database
from controller.dialog_controller import DialogController
from controller.dialogConf_controller import DialogConfController


import math

class MainService:

    def show_message(message, title="ATENCIÓN"):
        # Método para mostrar un mensaje en un cuadro de diálogo
        dialog = DialogController()
        dialog.ui.errorLabel.setText(message)
        dialog.ui.label.setText(title)
        dialog.run()
    
    def show_conf_message(message, title="ATENCIÓN"):
        dialog = DialogConfController()
        dialog.ui.errorLabel.setText(message)
        dialog.ui.label.setText(title)
        dialog.run()
        return dialog.result()
    
    def show_TestWindow():
        from controller.numTest_controller import NumTestController
        test_window = NumTestController()
        return test_window
    
    def show_GenWindow():
        from controller.numGen_controller import NumGenController
        gen_window = NumGenController()
        return gen_window
    
    def show_ClassWindow():
        from controller.numClass_controller import NumClassController
        class_window = NumClassController()
        return class_window