import pandas as pd
import numpy as np
import sys
path = '-MIAGE-TP_energie/MIAGE/src_tp/'
sys.path.append(path)
from Camion import Camion
from Travel import Travel
#id

travels = []

DEPOT = 0

MAX_DIST = 500
WORK_TIME = 28800
LOAD_PACKAGE = 600


time_tot = 0
dist_tot = 0
cap_tot = 0

actual_address = DEPOT
dilivered_package_at_t = 0

driver_list = []


visit = pd.read_csv('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/visits_test.csv')
visit_list = visit['visit_id'].values.tolist()
visit_list.pop(0)
print(visit_list)

distances_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/distances.txt')
time_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/times.txt')


def deliver(next_address, dilivered_package_at_t):
    #TODO incrémenter dist_tot, et MAJ dilivered_package_at_t
    #actual_address = next_adres
    pass


# on cherche tous les voisins, et nous renvoie le plus proche en terme de temps et de distance
def look_for_neighbor(actual_address):
    min_dist = 100000.0
    address_ = -1

    for address in visit_list:
        if min_dist > distances_matrix[actual_address,address] and distances_matrix[actual_address,address] != 0.0:
            min_dist = distances_matrix[actual_address,address]
            address_ = address

    if address_ == -1 :
        address_ = DEPOT

    return address_

# renvoie un boolean, vérifie si on a assez d'autonomie pour rentrer à la maison
def can_go_home(actual_address, next_address, cap_tot):
    dist = get_dist_between(actual_address,next_address) + get_dist_between(next_address,DEPOT)
    return camion.actual_capacity() >= dist


def get_dist_between(from_address, to_address):
    return distances_matrix.item((from_address,to_address))


#TODO faire en fonction du temps de travail d'un employé
def get_time_between(from_address, to_address):
    return time_matrix.item((from_address,to_address))

def get_load(next_address):
    return visit['demand'][next_address]



def has_enough_storage(actual_address, next_address, camion):
    cap = camion.capacity + visit['demand'][next_address]
    return (camion.storage_max) >= cap


def to_travel():
    pass


def has_enough_time(actual_address, next_address, camion):
    time = camion.actual_time() + time_matrix.item(actual_address, next_address)
    return (camion.time_max) >= time

def remove_address_visited() :
        visit_list.pop(next_address-1)

id_camion = 0
while len(visit_list) > 0: # only DEPOT remaining
    print("reste : ", visit_list)
    id_camion += 1
    travel = Travel(id_camion)
    camion = Camion(id_camion, LOAD_PACKAGE, WORK_TIME, MAX_DIST)

    while camion.enough_capacity() and camion.enough_storage() and camion.enough_time() and len(visit_list) > 0:
        next_address = look_for_neighbor(actual_address)

        #print(can_go_home(actual_address, next_address, camion))
        #print(has_enough_time(actual_address, next_address, camion))
        #print(has_enough_storage(actual_address, next_address, camion))

        if not can_go_home(actual_address, next_address, camion) \
                or not has_enough_time(actual_address, next_address, camion) \
                or not has_enough_storage(actual_address, next_address, camion) :
            next_address = DEPOT

        else:
            camion.storage += get_load(next_address)
        #travel = deliver(next_address, dilivered_package_at_t)

    #        dist_tot += travel.dist
    #        time_tot += travel.time
    #        cap_tot += travel.storage
    #        deliver_address.pop(actual_address)
    #       actual_address = next_address
            remove_address_visited()

        actual_address = next_address
        travel.list_visit.append(next_address)
        camion.capacity += get_dist_between(actual_address, next_address)
        camion.time += get_time_between(actual_address, next_address)

    camion.travel.append(travel)
    driver_list.append(camion)
    #travels.append(travel)

for driver in driver_list:
    with open(path + "camions/camion_" + str(driver.get_camion_id()) + ".txt", "w") as f:
        for travel in driver.get_camion_travel:
            f.write(str(travel))
            f.close
