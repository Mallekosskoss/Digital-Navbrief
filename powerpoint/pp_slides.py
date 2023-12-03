# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:17:37 2023

@author: mar"cu
"""

import xml.etree.ElementTree as ET
import sys
import os

# I CMD gå til mappen hvor scriptet ligger
# python pp_slides.py <tall> på lysbilde som skal endres <navn> på lysbilde når det skal lagres

# Henter argumentene som skrives i CMD
n = int(sys.argv[1])
output = str(sys.argv[2])

# Setter argumentene inn i kommandoen og kjører den
# Da åpner Inkscape filen og lagrer den igjen
args = "inkscape --export-plain-svg --export-area-drawing --export-filename=c:/users/lab/dropbox/bachelor/powerpoint/til_behandling/"+output+".svg c:/users/lab/dropbox/bachelor/powerpoint/slides/Lysbilde"+str(n)+".svg"
os.system(args)

#Åpner filen igjen og parser den
tree = ET.parse('../powerpoint/til_behandling/'+output+'.svg')
root = tree.getroot()

# Leter etter elementer fra lysbilder i powerpointen som ikke er ønskelig og sletter de
# Tar utgangspunkt i at lysbildene følger mal for navigasjonsbrief
iterasjon = 0
for i in range(len(root[1])):
    fill = root[1][i-iterasjon].get('fill')
    stroke = root[1][i-iterasjon].get('stroke')
    bilde = root[1][i-iterasjon].get('height')
    if fill == '#efefef' or fill =='#735d31' or fill == '#d5d2cd' or fill == '#ebeae8' or fill == '#5b9bd5' or fill == '#e7e7e7' or fill == '#c0504d' or fill == '#e8d0d0' or fill == 'f4e9e9':
        root[1].remove(root[1][i-iterasjon])
        iterasjon +=1
    elif stroke == '#d7d7d7': #legg til or stroke == '#EFEFEF' for å fjerne ruter helt
        root[1].remove(root[1][i-iterasjon])
        iterasjon +=1
    elif bilde == '100%' or bilde == '520':
        root[1].remove(root[1][i-iterasjon])
        iterasjon += 1

#Endrer fargen på skrift
for i in range(len(root[1])):
    text = root[1][i].get('font-size')
    if text == '15px':
        root[1][i].set('fill', '#191919')
    if len(root[1][i]) > 0:
        obj = root[1][i][0].get('fill')
        root[1][i][0].set('fill', '#191919')

#Denne gjør rutene sorte
for i in range(len(root[1])):
    strek = root[1][i].get('stroke')
    if strek == '#efefef':
        root[1][i].set('stroke', '#191919')

# Lagrer filen på nytt
tree.write('../powerpoint/behandlet/'+output+'.svg')

# Bruker Inkscape igjen for å lagre filen på nytt og tilpasser vinduets størrelse til innholdet
args = "inkscape --export-plain-svg --export-area-drawing --export-filename=../powerpoint/behandlet/"+output+".svg ../powerpoint/behandlet/"+output+".svg"
os.system(args)