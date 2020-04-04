import pandas as pd
import numpy as np
import sys
path = '-MIAGE-TP_energie/MIAGE/src_tp/'
sys.path.append(path)
from Camion import Camion
from Travel import Travel
#id
DEPOT = 0

MAX_DIST = 500
WORK_TIME = 28800
LOAD_PACKAGE = 600


time_tot = 0
dist_tot = 0
cap_tot = 0

actual_adress = DEPOT
dilivered_package_at_t = 0

driver_list = []


visit = pd.read_csv('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/visits_test.csv')
visit_list = visit['visit_id'].values.tolist()
visit_list.pop(0)
print(visit_list)

distances_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/distances.txt')
time_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/times.txt')


def deliver(next_adress, dilivered_package_at_t):
    #TODO incrémenter dist_tot, et MAJ dilivered_package_at_t
    #actual_adress = next_adres
    pass


#TODO on cherche tous les voisins, et nous renvoie le plus proche en terme de temps et de distance
def look_for_neighbor(actual_adress):
    min_dist = 100000.0
    adress_ = -1

    for adress in visit_list:
        if min_dist > distances_matrix[actual_adress,adress] and distances_matrix[actual_adress,adress] != 0.0:
            min_dist = distances_matrix[actual_adress,adress]
            adress_ = adress
    return adress_

#TODO renvoie un boolean, vérifie si on a assez d'autonomie pour rentrer à la maison
def can_go_home(actual_adress, next_adress, cap_tot):
    dist = distances_matrix.item((actual_adress,next_adress))
    return camion.actual_capacity() > dist


def get_dist_between(from_adress, to_adress):
    #TODO renvoie la distance entre 2 points
    return distances_matrix.item((from_adress,to_adress))


#TODO faire en fonction du temps de travail d'un employé
def get_time_between(from_adress, to_adress):
    return time_matrix.item((from_adress,to_adress))

def get_load(next_adress):
    return visit['demand'][next_adress]



def has_enough_storage(actual_adress, next_adress, camion):
    cap = camion.capacity + visit['demand'][next_adress]
    print(cap)
    return (camion.storage_max) >= cap


def to_travel():
    pass


def has_enough_time(actual_adress, next_adress, camion):
    time = camion.actual_time + time_matrix.item((actual_adress, next_adress))
    return (camion.time_max) >= time


id_camion = 0
while len(visit_list)>0:
    id_camion =+ 1
    travel = Travel(id_camion)
    camion = Camion(id_camion, LOAD_PACKAGE, WORK_TIME, MAX_DIST)

    while camion.enough_capacity() and camion.enough_storage() and camion.enough_time():

        next_adress = look_for_neighbor(actual_adress)
        if next_adress == -1:
            next_adress = DEPOT
        #print(can_go_home(actual_adress, next_adress, camion))
        #print(has_enough_time(actual_adress, next_adress, camion))
        print(has_enough_storage(actual_adress, next_adress, camion))

        if not can_go_home(actual_adress, next_adress, camion) \
                or not has_enough_time(actual_adress, next_adress, camion) \
                and next_adress != DEPOT:
            next_adress = DEPOT
            camion.capacity += get_dist_between(actual_adress, next_adress)
            camion.time += get_time_between(actual_adress, next_adress)
        else:
            camion.capacity += get_dist_between(actual_adress,next_adress)
            camion.time += get_time_between(actual_adress,next_adress)
            camion.storage += get_load(next_adress)
            visit_list.pop(next_adress)
            actual_adress = next_adress
            camion.travel.append(next_adress)
            travel.list_visit.append(next_adress)
            print(travel.list_visit)

        #travel = deliver(next_adress, dilivered_package_at_t)

    #        dist_tot += travel.dist
    #        time_tot += travel.time
    #        cap_tot += travel.storage
    #        deliver_adress.pop(actual_adress)
     #       actual_adress = next_adress

    driver_list.append(camion)



