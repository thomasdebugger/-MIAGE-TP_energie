class Camion :

    def __init__(self, id, storage, time, capacity):
        self.id_camion = id
        self.storage_max = storage
        self.time_max = time
        self.capacity_max = capacity
        self.storage = 0
        self.time = 300.0
        self.capacity = 0

    def load_package(self, nb_package):
        self.time += nb_package * 10

    def actual_storage(self):
        return self.storage_max - self.storage

    def actual_time(self):
        return self.time_max - self.time

    def actual_capacity(self):
        return self.capacity_max - self.capacity

    def enough_capacity(self):
        return self.capacity_max >= self.capacity

    def enough_time(self):
        return self.time_max >= self.time

    def enough_storage(self):
        return self.storage_max >= self.storage

    def get_camion_id(self):
        return self.id_camion