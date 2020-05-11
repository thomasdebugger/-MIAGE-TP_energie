import pandas as pd
import numpy as np
import sys
path = '-MIAGE-TP_energie/MIAGE/src_tp/'
sys.path.append(path)
from Camion import Camion
from Travel import Travel


class ScriptNonAlea :

    def __init__(self):
        self.travels = []
        self.DEPOT = 0
        self.MAX_DIST = 50.0
        self.WORK_TIME = 28800
        self.LOAD_PACKAGE = 600
        self.LOAD_TIME = 60
        self.RELOAD_SLOW = 60
        self.RELOAD_MEDIUM = 180
        self.RELOAD_FAST = 480
        self.CAMION_SCORE = 50
        self.package_time = 10
        self.time_tot = 0
        self.dist_tot = 0
        self.cap_tot = 0
        self.score = 0
        self.actual_address = 0
        self.dilivered_package_at_t = 0
        self.driver_list = []
        self.visit = []
        self.distances_matrix = ""
        self.time_matrix = ""

    def initial(self):
        self.visit = pd.read_csv(
            '/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/lyon_200_2_3/visits.csv')
        self.visit_list = self.visit['visit_id'].values.tolist()
        self.visit_list.pop(0)
        self.distances_matrix = np.loadtxt(
            '/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/lyon_200_2_3/distances.txt')
        self.time_matrix = np.loadtxt(
            '/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/lyon_200_2_3/times.txt')



    def bag_time_calcul(self, nb_bag, dist_time):
        return self.LOAD_TIME * nb_bag + dist_time

        # on cherche tous les voisins, et nous renvoie le plus proche en terme de temps et de distance

    def look_for_neighbor(self, actual_address):
        min_dist = 100000.0
        address_ = -1

        for address in self.visit_list:
            if min_dist > self.distances_matrix[actual_address, address] and self.distances_matrix[
                actual_address, address] != 0.0:
                min_dist = self.distances_matrix[actual_address, address]
                address_ = address

        if address_ == -1:
            address_ = self.DEPOT

        return address_

        # renvoie un boolean, vérifie si on a assez d'autonomie pour rentrer à la maison

    def can_go_home(self, actual_address, next_address, cap_tot, camion):
        dist = self.get_dist_between(actual_address, next_address) + self.get_dist_between(next_address, self.DEPOT)
        return camion.actual_capacity() >= dist

    def get_dist_between(self, from_address, to_address):
        return self.distances_matrix.item((from_address, to_address))

        # faire en fonction du temps de travail d'un employé

    def get_time_between(self, from_address, to_address):
        return self.time_matrix.item((from_address, to_address))

    def get_load(self, next_address):
        return self.visit['demand'][next_address]

    def reloadByType(self, type, camion):
        if type == "slow":
            camion.time += self.RELOAD_SLOW
        if type == "medium":
            camion.time += self.RELOAD_MEDIUM
        if type == "fast":
            camion.time += self.RELOAD_FAST

    def has_enough_storage(self, actual_address, next_address, camion):
        cap = camion.capacity + self.visit['demand'][next_address]
        return (camion.storage_max) >= cap

    def has_enough_time(self, actual_address, next_address, camion):
        time = camion.time + self.time_matrix.item(actual_address, next_address)
        return (camion.time_max) >= time

    def remove_address_visited(self, next_address):
        for visit in self.visit_list:
            if visit == next_address:
                index = self.visit_list.index(visit)
                self.visit_list.pop(index)

    def camionCanTravel(self,actual_address, next_address, camion):
        return self.has_enough_time(actual_address, next_address, camion) \
               and self.has_enough_storage(actual_address, next_address, camion)

    def doTravel(self, camion, actual_address, next_address):
        camion.storage += self.get_load(next_address)
        camion.capacity += self.get_dist_between(actual_address, next_address)
        package_time = self.bag_time_calcul(self.get_load(next_address), self.get_time_between(actual_address, next_address))
        camion.time += package_time
        camion.travel.append(next_address)

        self.travel.list_visit.append(next_address)
        self.remove_address_visited(next_address)

    def reloadToDepot(self, camion, type):
        camion.storage = 0
        camion.capacity = 0
        self.reloadByType(type, camion)


    def main_ (self):
        id_camion = 0
        while len(self.visit_list) > 0:  # only DEPOT remaining
            id_camion += 1
            self.score += self.CAMION_SCORE

            actual_address = self.DEPOT

            travel = Travel(id_camion)
            camion = Camion(id_camion, self.LOAD_PACKAGE, WORK_TIME, MAX_DIST)

            next_address = self.look_for_neighbor(actual_address)

            while self.camionCanTravel(actual_address, next_address, camion) and actual_address != next_address:

                if not self.can_go_home(actual_address, next_address, camion):
                    self.reloadToDepot(camion, 'fast')
                    next_address = self.DEPOT

                self.doTravel(camion, actual_address, next_address)
                self.score += self.get_dist_between(actual_address, next_address)

                actual_address = next_address
                next_address = self.look_for_neighbor(actual_address)

            camion.travel.append(next_address)
            self.driver_list.append(camion)
            # travels.append(travel)

        for driver in self.driver_list:
            with open("./camions/camion_" + str(driver.get_camion_id()) + ".txt", "w") as f:
                for travel in driver.get_camion_travel():
                    f.write(str(travel) + ',')

        print("score = ", self.score)

