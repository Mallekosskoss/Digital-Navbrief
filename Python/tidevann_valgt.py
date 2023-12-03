# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:53:20 2023

@author: Marcus
"""
import datetime
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

#Henter dataen og parser filen
tree = ET.parse('C:/Users/LAB/Dropbox/Bachelor/data_inn/valgt_pos/input_tidevann.xml')
root = tree.getroot()

#Initialiserer matriser hvor dataen skal lagres
x = []
x2 =[]
y = []
y2 =[]

#Henter klokkeslettet
klokke = datetime.datetime.now()
#Lagrer timen og minuttet til hver sin variabel
time = float(klokke.strftime("%H"))
minutt = float(klokke.strftime("%M"))
#Setter sammen klokkeslettet til desimalform
klokkeslett = time+minutt/60

#Henter observert tidevann
for i in range(len(root[0][2])):
    tid = root[0][2][i].get('time')
    tid = int(tid[11:13])
    x.append(tid)
    value = root[0][2][i].get('value')
    y.append(float(value))

#Henter forventet tidevann
for k in range(len(root[0][5])-1):
    tid = root[0][5][k].get('time')
    tid = int(tid[11:13])
    x2.append(tid)
    item = root[0][5][k].get('value')
    y2.append(float(item))

#Koden under jevner ut grafen ved å legge inn ekstra verdier og lage en B-spline
X_Y_Spline = make_interp_spline(x, y)
X2_Y2_Spline = make_interp_spline(x2, y2) 

X_ = np.linspace(min(x), max(x), 100)
X2_ = np.linspace(min(x2), max(x2), 100)

Y_ = X_Y_Spline(X_)
Y2_ = X2_Y2_Spline(X2_)
 
# Plotter begge grafene
fig, ax = plt.subplots()
plt.plot(X2_, Y2_, label='Forventet')
plt.plot(X_, Y_, label='Observert')
leg = plt.legend(loc='lower center')
plt.xlabel("Time")
plt.ylabel("Tidevann (cm)")
plt.grid()
plt.vlines(klokkeslett, 0, max(y), colors='green')
#Lagrer grafen med gjennomsiktig bakgrunn
plt.savefig("C:/Users/LAB/Dropbox/Bachelor/bilder/valgt/tidevann_valgt.svg", transparent=True)    