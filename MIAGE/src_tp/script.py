import pandas as pd
import numpy as np
import sys
path = '-MIAGE-TP_energie/MIAGE/src_tp/'
sys.path.append(path)
from Camion import Camion
from Travel import Travel
from Score import Score

travels = []

DEPOT = 0

MAX_DIST = 50.0
WORK_TIME = 28800
LOAD_PACKAGE = 600
LOAD_TIME = 60
RELOAD_SLOW = 60
RELOAD_MEDIUM = 180
RELOAD_FAST = 480

CAMION_SCORE = 50.0

package_time = 10
time_tot = 0
dist_tot = 0
cap_tot = 0
score = 0

actual_address = DEPOT
dilivered_package_at_t = 0

driver_list = []

visit = pd.read_csv('../lyon_200_2_3/visits.csv')
visit_list = visit['visit_id'].values.tolist()
visit_list.pop(0)

distances_matrix = np.loadtxt('../lyon_200_2_3/distances.txt')
time_matrix = np.loadtxt('../lyon_200_2_3/times.txt')

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
        if min_dist > distances_matrix[actual_address,address] and actual_address != address :
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

def reloadByType(type, camion):
    if type == "slow" :
        camion.time += RELOAD_SLOW
    if type == "medium":
        camion.time += RELOAD_MEDIUM
    if type == "fast":
        camion.time += RELOAD_FAST

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

def camionCanTravel(actual_address, next_address, camion):
    return has_enough_time(actual_address, next_address, camion) \
            and has_enough_storage(actual_address, next_address, camion)

def doTravel(camion, actual_address, next_address):
    camion.storage += get_load(next_address)
    camion.capacity += get_dist_between(actual_address, next_address)
    package_time = bag_time_calcul(get_load(next_address), get_time_between(actual_address, next_address))
    camion.time += package_time
    camion.travel.append(next_address)

    travel.list_visit.append(next_address)
    remove_address_visited(next_address)


def reloadToDepot(camion, type):
    camion.storage = 0
    camion.capacity = 0
    reloadByType(type, camion)

id_camion = 0
score = Score()
while len(visit_list) > 0: # only DEPOT remaining
    id_camion += 1
    score.score += CAMION_SCORE

    actual_address = DEPOT

    travel = Travel(id_camion)
    camion = Camion(id_camion, LOAD_PACKAGE, WORK_TIME, MAX_DIST)
    local_score = CAMION_SCORE


    next_address = look_for_neighbor(actual_address)

    while camionCanTravel(actual_address, next_address, camion) and actual_address != next_address:
        if not can_go_home(actual_address, next_address, camion):
            reloadToDepot(camion, 'fast')
            next_address = DEPOT

        doTravel(camion, actual_address, next_address)

        score.evaluate(get_dist_between(actual_address, next_address))
        score.travel_score.append(score.score)
        local_score += get_dist_between(actual_address, next_address)
        camion.score_camion.append(local_score)

        actual_address = next_address
        next_address = look_for_neighbor(actual_address)

    camion.travel.append(next_address)
    driver_list.append(camion)
    #travels.append(travel)

for driver in driver_list:
    with open("./camions/camion_" + str(driver.get_camion_id()) + ".txt", "w") as f:
        for travel in driver.get_camion_travel():
            f.write(str(travel)+',')

print("score = ", score.score)
for driver in driver_list :
    print("driver numero : ", driver.id_camion)
    print("score :", driver.score_camion)
print(score.travel_score)