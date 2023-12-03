# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:17:37 2023

@author: mar"cu
"""

import xml.etree.ElementTree as ET

# Henter filen og parser
tree = ET.parse('C:/Users/LAB/Dropbox/Bachelor/data_inn/valgt_pos/ny_marinogram.svg')
root = tree.getroot()

# Følgende for løkker fjerner elementer som ikke er ønskelig i svg filen
# Dersom den fjerner et element (child) vil foreldre-elementet (parent) ha et element mindre
# Må kompansere med å trekke fra 1 i indeksen for hvert element som blir fjernet for å slippe feilmelingen child out of range


# Leter gjennom filen i det andre elementet i root etter taggen g hvor atributten clip-path har en spesifikk verdi
iterasjon = 0
for i in range(len(root[1])):
    item = root[1][i-iterasjon].tag
    atributt = root[1][i-iterasjon].get('clip-path')
    if item == '{http://www.w3.org/2000/svg}g' and atributt=='url(#linearGradient1)':
        root[1].remove(root[1][i-iterasjon])
        iterasjon +=1

# Leter etter elemnter med taggen rect og atributt med spesiell farge/innhold
for i in range(len(root[1])):
    iterasjon = 0
    item = root[1][i].tag
    if item == '{http://www.w3.org/2000/svg}g':
        for j in range(len(root[1][i])):
            item = root[1][i][j-iterasjon].tag
            farge = root[1][i][j-iterasjon].get('clip-path')
            if item == '{http://www.w3.org/2000/svg}rect' and (farge == 'white' or farge == 'url(#clipPath1)'):
                root[1][i].remove(root[1][i][j-iterasjon])
                iterasjon +=1

# Noen ganger er strukturen til filen annerledes, og denne løkken fjerner elementer basert på størrelsen
for i in range(len(root[1])):
    iterasjon = 0
    farge = root[1][i].get('fill')
    if farge =='white':
        for j in range(len(root[1][i])):
            item = root[1][i][j-iterasjon].tag
            atributt = root[1][i][j-iterasjon].get('height')
            if item == '{http://www.w3.org/2000/svg}rect' and atributt == '181.310595':
                root[1][i].remove(root[1][i][j-iterasjon])
                iterasjon += 1
            elif item == '{http://www.w3.org/2000/svg}rect' and atributt == '112.262195':
                root[1][i].remove(root[1][i][j-iterasjon])
                iterasjon += 1

# Lagrer filen igjen     
tree.write('C:/Users/LAB/Dropbox/Bachelor/bilder/valgt/marinogram_valgt.svg')