# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 09:56:31 2023

@author: Marcus
"""

import xml.etree.ElementTree as ET

# Henter filen og parser
tree = ET.parse('C:/Users/LAB/Dropbox/Bachelor/data_inn/live_pos/ny_meteogram.svg')
root = tree.getroot()

#Fjerner elementet som utgjør bakgrunnen
iterasjon = 0
for i in range(len(root)):
    item = root[i-iterasjon].get('id')
    if item =="rect1":
        root.remove(root[i-iterasjon])
        iterasjon += 1

# Lagrer filen        
tree.write('C:/Users/LAB/Dropbox/Bachelor/bilder/live/meteogram.svg')
