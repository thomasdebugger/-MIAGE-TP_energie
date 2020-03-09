import pandas as pd
import numpy as np

POINT_DEPART = "im2ag"
MAX_DIST = 500
WORK_TIME = 8
LOAD_PACKAGE = 600


time_tot = 0
dist_tot = 0
cap_tot = 0
deliver_adress = []

actual_adress = POINT_DEPART
dilivered_package_at_t = 0


visit_list = pd.read_csv('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/visits.csv')

distances_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/distances.txt')
dtime_matrix = np.loadtxt('/Users/cbml5653/Documents/Cours_energie/-MIAGE-TP_energie/MIAGE/Example/times.txt')

def deliver(next_adress, dilivered_package_at_t):
    #TODO incrémenter dist_tot, et MAJ dilivered_package_at_t
    #actual_adress = next_adres
    pass


def look_for_neighbor(actual_adress):
    #TODO on cherche tous les voisins, et nous renvoie le plus proche en terme de temps et de distance
    pass


def can_go_home(next_adress, dist_tot):
    #TODO renvoie un boolean, vérifie si on a assez d'autonomie pour rentrer à la maison
    pass


def go_home():
    #TODO on rentre à la maison
    pass


def get_dist_between(from_adress, to_adress):
    #TODO renvoie la distance entre 2 points
    pass


#TODO faire en fonction du temps de travail d'un employé
def get_time_between(from_adress, to_adress):
    pass


def has_enough_storage(cap_tot):
    pass


def to_travel():
    pass


def has_enough_time(next_adress, time_tot):
    pass


#while MAX_DIST > dist_tot and WORK_TIME > time_tot and LOAD_PACKAGE > cap_tot :
#    next_adress = look_for_neighbor(actual_adress)
#    if not can_go_home(next_adress,dist_tot):
#        go_home()
#        dist_tot += get_dist_between(actual_adress, POINT_DEPART)
#        time_tot += get_time_between(actual_adress, POINT_DEPART)

#    if not has_enough_time(next_adress,time_tot):
#        go_home()
#        dist_tot += get_dist_between(actual_adress, POINT_DEPART)
#        time_tot += get_time_between(actual_adress, POINT_DEPART)

#    if not has_enough_storage(cap_tot,next_adress):
#        to_travel()

#    else:
#        travel = deliver(next_adress, dilivered_package_at_t)
#        dist_tot += travel.dist
#        time_tot += travel.time
#        cap_tot += travel.storage
#        deliver_adress.pop(actual_adress)
 #       actual_adress = next_adress



