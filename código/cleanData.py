#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os

def seleccionar_campos(reader, rows):
	for row in reader:	
		if row[7] != 'C' and (row[8] == 'Canino' or row[8] == 'Felino'):
			
			provinciaSplit = row[14].split('/')
			provincia=provinciaSplit[0]

			new_row = []
			new_row.append(row[1])
			new_row.append(row[3])
			new_row.append(row[4])
			new_row.append(row[7])
			new_row.append(row[9])
			new_row.append(row[11])
			new_row.append(provincia)
			new_row.append(row[15])
			rows.append(new_row)
	return rows

rows = []
reader = csv.reader(open('fueraEuskadi.csv', 'rb'))
rows = seleccionar_campos(reader, rows)

	
csvfile = open('datos.csv', 'w')
headers = ['numeroChip', 'fecha_nacimiento', 'fecha_implantacion', 'sexo', 'raza', 'aptitud', 'provincia', 'municipio']
writer = csv.writer(csvfile, delimiter=',')
writer.writerow(headers)
writer.writerows(rows)




