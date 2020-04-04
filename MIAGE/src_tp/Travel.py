class Travel:
    def __init__(self,id_camion):
        self.camion = id_camion
        self.list_visit = []

    def get_list_visit(self) :
        return self.list_visit