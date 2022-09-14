from fileinput import filename

import numpy as np

import matplotlib as plt

import scipy as sp
import pandas as pd


def get_coordinates(line):
    return [float(line[33:39].strip()), float(line[40:46].strip()), float(line[47:54].strip())]
#print("Enter pdb name")
#filename = input()
filename = "1uz9.pdb"

# Chargement des données du fichier pdb
fn = open(filename)
CaPos = []
CaAA = []
CaMatrix = []
for line in fn:
        if line.startswith("ATOM"):
            atomline = int(line[6:11])
            atom = line[12:16].strip()
            Aa = line[20:23]
            if atom == "CA":
                CaPos.append(atomline)
                CaMatrix.append((get_coordinates(line)))
                CaAA.append(Aa)

# Calcul des distances entre atomes CA
CaDist = []
y = 2
from scipy.spatial import distance
distance_aa = []
i = 2
while i < len(CaMatrix):
    j = 0
    while j < i-1:
       a = CaMatrix[i]
       b = CaMatrix[j]
       distance_aa.append([CaAA[i], CaAA[j], round(distance.euclidean(a, b), 2)])
       j += 1
    i+=1

"""print("Affichage Matrice Distance_aa")
for x in distance_aa:
    print(x)
"""

# Chargement du fichier dope
dope = []
dop = open('dope.par')
for line in dop:
    if line[4:6] == "CA" and line[11:13] == "CA":
        dope.append(line.split())

#print("Affichage Matrice dope")
#for x in dope:
#    print(x)

# Pour chaque distance entre Carbones Alpha de même Acide Aminé, cumul des énergies trouvées dans DOPE
ener = []
for x in  distance_aa:
    i = round(x[2]*2, 0) + 4
    if i < 34:
      for y in dope:

          if x[0] == y[0] and x[1] == y[2]:
             #print(f"x[0] = {x[0]}, y[0] = {y[0]}, x[1] = {x[1]}, y[2] = {y[2]}")
             ener.append(float(y[int(i)]))
# Somme des énergies cumulées
energiesCumulees = sum(ener)
print(energiesCumulees)
# Recherche aléatoire d'énergies dans DOPE
import random
temoin = []

b = 0
while b < 10:
  temoin.clear()
  a = 0
  while a < 100:
      i = random.randrange(0, 100)
      j = random.randrange(4, 34)
      temoin.append(float(dope[i][j]))
      a += 1
  c = sum(temoin)
  print(c)
  b += 1
# Calcul du z-score






















