#from fileinput import filename
#import numpy as np
#import matplotlib as plt
#import pandas as pd


def get_coordinates(line):
    return [float(line[31:38].strip()), float(line[39:46].strip()), float(line[47:55].strip())]
print("Enter pdb name")
filename = input()

# Chargement des données du fichier pdb
fn = open(filename)
CaPos = []
CaAA = []
CaMatrix = []
for line in fn:
        if line.startswith("ATOM"):
            atomline = int(line[8:13])
            atom = line[13:15].strip()

            Aa = line[17:20]
            if atom == "CA":
                CaPos.append(atomline)
                CaMatrix.append([Aa, get_coordinates(line)])


# Calcul des distances entre atomes CA

def calcul_dist(CaMatrix):
    CaDist = []
    y = 2
    from scipy.spatial import distance
    distance_aa = []
    i = 2
    while i < len(CaMatrix):
        j = 0
        while j < i-1:
            a = CaMatrix[i][1]
            b = CaMatrix[j][1]
            distance_aa.append([CaMatrix[i][0], CaMatrix[j][0], round(distance.euclidean(a, b), 2)])
            j += 1
        i+=1
    return distance_aa

distance_aa = calcul_dist(CaMatrix)


# Chargement du fichier dope
dope = []
dop = open('dope.par')
for line in dop:
    if line[4:6] == "CA" and line[11:13] == "CA":
        dope.append(line.split())



# Pour chaque distance entre Carbones Alpha de même Acide Aminé, cumul des énergies trouvées dans DOPE
def calcul_energ(distance_aa):
    ener = []
    for x in  distance_aa:
        i = round(x[2]*2, 0) + 4
        if i < 34:
            for y in dope:
                if x[0] == y[0] and x[1] == y[2]:
                   ener.append(float(y[int(i)]))

    # Somme des énergies cumulées
    energiesCumulees = sum(ener)
    return energiesCumulees

# Appel fonction calcul_energ
energiesCumulees = calcul_energ(distance_aa)
print(f"energies cumulées = {energiesCumulees}")


# Recherche d'énergies issues de conformations aléatoires de la protéine de base

print("Calcul du z-score")
import random
t = 0
RandEner = []
while t < 30:
    t += 1
    random.shuffle(CaMatrix)
    distance_aa = calcul_dist(CaMatrix)
    RandEner.append(calcul_energ(distance_aa))


# Calcul du z-score


import statistics
mu = round(statistics.mean(RandEner), 2)
ety = round(statistics.pstdev(RandEner), 2)
z_score = (energiesCumulees - mu) / ety
print(f"z_score = {z_score}")
























