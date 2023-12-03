# -*- coding: utf-8 -*-

import ephem    # Bibliotek med astronomisk data
import csv      # Gjør det mulig å skrive til og laste ned data til CVS-fil
import json     # Gjør det mulig å hente ut data som er skrevet på JSON-format fra fil
from datetime import datetime, timedelta

# Lage funksjon som henter inn riktig informasjon utifra koordinater oppgitt, der koordinater er i grader
def calculate_event_times(latitude_deg, longitude_deg):
    observer = ephem.Observer()
    observer.lat = str(latitude_deg)
    observer.long = str(longitude_deg)

    # Setter dato til å være i dag rett etter midnatt. Program henter inn data som ikke har skjedd enda, så når soloppgang har skjedd, henter den morgendagen sin soloppgang (den ønsker vi ikke i dette tilfellet)
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    observer.date = current_date

    event_angles = [0, -6, -12, -18]  # Vinkel ved solnedgang/oppgang og ulike tussmørker
    event_times = {}

    for angle in event_angles:
        observer.horizon = str(angle)
        next_rising = observer.next_rising(ephem.Sun(), use_center=True)
        next_setting = observer.next_setting(ephem.Sun(), use_center=True)

        # Setter tid til UTC+1 (Norsk vintertid) ved å legge til 1 time
        # Ved sommertid må man legge til 2 timer
        next_rising_utc1 = next_rising.datetime() + timedelta(hours=1)
        next_setting_utc1 = next_setting.datetime() + timedelta(hours=1)

        # Gjør tider om til tekst/string
        next_rising_str = next_rising_utc1.strftime('%Y-%m-%d %H:%M:%S')
        next_setting_str = next_setting_utc1.strftime('%Y-%m-%d %H:%M:%S')

        # Henter tidspunkt for de ulike hendelsene
        if angle == 0:
            event_times['Soloppgang'] = {
                'start': next_rising_str
            }
            event_times['Solnedgang'] = {
                'end': next_setting_str,
            }
        elif angle == -6:
            event_times['Borgerlig tussmørke'] = {
                'end': next_setting_str,
            }
        elif angle == -12:
            event_times['Nautisk tussmørke'] = {
                'end': next_setting_str,
            }
        elif angle == -18:
            event_times['Astronomisk tussmørke'] = {
                'end': next_setting_str,
            }       
    return event_times

# Åpner fil og leser inn data
with open("C:/Users/LAB/Dropbox/Bachelor/data_inn/valgt_pos/valgt_posisjon.txt", "r") as file:
    data = json.load(file)

# Henter ut høyde- og breddegrad og sender dette til funksjonen
latitude_deg = data["latitude"]
longitude_deg = data["longitude"]

event_times = calculate_event_times(latitude_deg, longitude_deg)

# Definerer start for de ulike hendelsene
borgerlig_start = event_times['Borgerlig tussmørke']['end']
nautisk_start = event_times['Nautisk tussmørke']['end']
astronomisk_start = event_times['Astronomisk tussmørke']['end']

# Regner ut varighet til de ulike hendelsene
borgerlig_duration = datetime.strptime(borgerlig_start, '%Y-%m-%d %H:%M:%S') - datetime.strptime(event_times['Solnedgang']['end'], '%Y-%m-%d %H:%M:%S')
nautisk_duration = datetime.strptime(nautisk_start, '%Y-%m-%d %H:%M:%S') - datetime.strptime(borgerlig_start, '%Y-%m-%d %H:%M:%S')
astronomisk_duration = datetime.strptime(astronomisk_start, '%Y-%m-%d %H:%M:%S') - datetime.strptime(nautisk_start, '%Y-%m-%d %H:%M:%S')

# Setter data inn i lister
data = [
    ["Hendelse", "Tid", "Varighet"],
    ["Soloppgang", event_times['Soloppgang']['start'], str(" ")],
    ["Solnedgang", event_times['Solnedgang']['end'], str(" ")],
    ["Borgerlig tussmørke", event_times['Borgerlig tussmørke']['end'], str(borgerlig_duration)],
    ["Nautisk tussmørke", event_times['Nautisk tussmørke']['end'], str(nautisk_duration)],
    ["Astronomisk tussmørke", event_times['Astronomisk tussmørke']['end'], str(astronomisk_duration)]
]

# Lagrer data til CSV fil
with open('C:/Users/LAB/Dropbox/Bachelor/data_inn/valgt_pos/astronomisk_valgt.csv', mode='w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)