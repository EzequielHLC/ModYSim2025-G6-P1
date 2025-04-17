from service.von_neuman_service import VonNeumanService
from view.von_neuman_view import VonNewmanView
from service.main_service import MainService

class VonNewmanController: 
    def __init__(self):
        self.von_neumann_service = VonNeumanService()
        self.view = self.von_newmann_view = VonNewmanView(self)  # Vista Von Neumann
        self.main_service = MainService(self.view)
    