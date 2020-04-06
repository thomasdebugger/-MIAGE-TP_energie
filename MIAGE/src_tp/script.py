import pandas as pd
import numpy as np
import sys
path = '-MIAGE-TP_energie/MIAGE/src_tp/'
sys.path.append(path)
from Camion import Camion
from Travel import Travel

travels = []

DEPOT = 0

MAX_DIST = 500
WORK_TIME = 28800
LOAD_PACKAGE = 600
LOAD_TIME = 60
RELOAD_SLOW = 60
RELOAD_MEDIUM = 180
RELOAD_FAST = 480

package_time = 0
time_tot = 0
dist_tot = 0
cap_tot = 0

actual_address = DEPOT
dilivered_package_at_t = 0

driver_list = []


visit = pd.read_csv('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/lyon_200_2_3/visits.csv')
visit_list = visit['visit_id'].values.tolist()
visit_list.pop(0)

distances_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/lyon_200_2_3/distances.txt')
time_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/lyon_200_2_3/times.txt')


def deliver(next_address, dilivered_package_at_t):
    #TODO incrémenter dist_tot, et MAJ dilivered_package_at_t
    #actual_address = next_adres
    pass

def bag_time_calcul(nb_bag, dist_time):
    return LOAD_TIME*nb_bag + dist_time

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


# faire en fonction du temps de travail d'un employé
def get_time_between(from_address, to_address):
    return time_matrix.item((from_address,to_address))

def get_load(next_address):
    return visit['demand'][next_address]

def reload(type):
    if type == "slow" :
        camion.time += RELOAD_SLOW
    if type == "medium":
        camion.time += RELOAD_MEDIUM
    if type == "fast":
        camion.time += RELOAD_FAST
    camion.capacity = 0

def has_enough_storage(actual_address, next_address, camion):
    cap = camion.capacity + visit['demand'][next_address]
    return (camion.storage_max) >= cap

def to_travel():
    pass

def has_enough_time(actual_address, next_address, camion):
    time = camion.time + time_matrix.item(actual_address, next_address)
    return (camion.time_max) >= time

def remove_address_visited(next_address) :
    for visit in visit_list :
        if visit == next_address :
            index = visit_list.index(visit)
            visit_list.pop(index)

id_camion = 0
while len(visit_list) > 0: # only DEPOT remaining
    id_camion += 1
    travel = Travel(id_camion)
    camion = Camion(id_camion, LOAD_PACKAGE, WORK_TIME, MAX_DIST)

    next_address = look_for_neighbor(actual_address)

    while can_go_home(actual_address, next_address, camion) and has_enough_time(actual_address, next_address, camion) \
            and has_enough_storage(actual_address, next_address, camion) and len(visit_list) > 0:
        next_address = look_for_neighbor(actual_address)
        camion.storage += get_load(next_address)
        remove_address_visited(next_address)

        if (actual_address != next_address) :
            actual_address = next_address
            travel.list_visit.append(next_address)
            camion.travel.append(next_address)
            camion.capacity += get_dist_between(actual_address, next_address)
            package_time = bag_time_calcul(get_load(next_address), get_time_between(actual_address, next_address))
            camion.time += package_time
        else :
            break
        if not can_go_home():
            reload()

    next_address = DEPOT

    camion.travel.append(next_address)
    driver_list.append(camion)
    #travels.append(travel)

    print(camion.actual_time())
for driver in driver_list:
    with open("./camions/camion_" + str(driver.get_camion_id()) + ".txt", "w") as f:
        for travel in driver.get_camion_travel():
            f.write(str(travel)+',')
