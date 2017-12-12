#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sqlite3
import os


bd = sqlite3.connect('IdentificacionAnimales.db')
cursor = bd.cursor()

def diferenciaFecha(fecha_nacimiento, fecha_implantacion):

	return (abs(int(fecha_nacimiento[7:]) - int(fecha_implantacion[7:])) * 365) + (abs(int(fecha_nacimiento[4:5]) - int(fecha_implantacion[4:5])) * 30) + abs(int(fecha_nacimiento[:2]) - int(fecha_implantacion[:2]))
		


#metemos todos los datos de animales en la tabla ANIMALES
reader = csv.reader(open('datos.csv', 'rb'))
x = 0
for row in reader:
	if x > 0:
		id_chip = row[0].decode("windows-1258")
		fecha_nacimiento= row[1].decode("windows-1258")
		fecha_implantacion= row[2].decode("windows-1258")
		difTiempo = diferenciaFecha(fecha_nacimiento, fecha_implantacion)
		sexo= row[3].decode("windows-1258")
		raza= row[4].decode("windows-1258")
		aptitud= row[5].decode("windows-1258")
		provincia= row[6].decode("windows-1258")
		municipio= row[7].decode("windows-1258")
		cursor.execute("INSERT INTO ANIMALES (idChip, fechaImplantacion, sexo, raza, aptitud, provincia, municipio, difTiempoNacImp) VALUES (?,?,?,?,?,?,?,?)", 
			(id_chip, fecha_implantacion, sexo, raza, aptitud, provincia, municipio, difTiempo))
		
	x = x + 1



#eliminamos posibles filas repetidas agrupando por el idchip
cursor.execute("INSERT INTO AUXILIAR_ANIMALES1 SELECT DISTINCT idChip, fechaImplantacion, sexo, raza, aptitud, provincia, municipio, difTiempoNacImp FROM ANIMALES GROUP BY idChip")

#agrupamos los animales que tienen las mismas caracteristicas independientemente del chip
cursor.execute("INSERT INTO AUXILIAR_ANIMALES2 SELECT fechaImplantacion, sexo, raza, aptitud, provincia, municipio, difTiempoNacImp, count(*) FROM AUXILIAR_ANIMALES1 GROUP BY fechaImplantacion, sexo, raza, aptitud, provincia, municipio")

#introducimos los datos en las tablas de dimensiones

cursor.execute ("INSERT INTO  Dimension_FechaImplantacion (fecha, dia, mes, año) SELECT DISTINCT a.fechaImplantacion, SUBSTR(a.fechaImplantacion, 1, 2), SUBSTR(a.fechaImplantacion, 4, 2), SUBSTR(a.fechaImplantacion, 7, 4) FROM AUXILIAR_ANIMALES2 a")

cursor.execute ("INSERT INTO  Dimension_Localizacion (municipio, provincia) SELECT DISTINCT a.municipio, a.provincia FROM AUXILIAR_ANIMALES2 a")

cursor.execute ("INSERT INTO  Dimension_Sexo (sexo) SELECT DISTINCT a.sexo FROM AUXILIAR_ANIMALES2 a")

cursor.execute ("INSERT INTO  Dimension_Raza (raza) SELECT DISTINCT a.raza FROM AUXILIAR_ANIMALES2 a")

cursor.execute ("INSERT INTO  Dimension_Aptitud (aptitud) SELECT DISTINCT a.aptitud FROM AUXILIAR_ANIMALES2 a")



#introducimos los datos en la tabla de hechos
cursor.execute ("INSERT INTO Hechos_Implantaciones (idFechaImplantacion, idSexo, idRaza, idAptitud, idLocalizacion, difTiempoNacImp, totalAnimales) SELECT fi.idFechaImplantacion, s.idSexo, ra.idRaza, ap.idAptitud, lo.idLocalizacion, a.difTiempoNacImp, a.totalAnimales FROM Dimension_FechaImplantacion fi, Dimension_Sexo s, Dimension_Raza ra, Dimension_Aptitud ap, Dimension_Localizacion lo INNER JOIN AUXILIAR_ANIMALES2 a ON a.fechaImplantacion = fi.fecha AND a.sexo = s.sexo AND a.raza = ra.raza AND a.aptitud = ap.aptitud AND a.municipio = lo.municipio AND a.provincia = lo.provincia ORDER BY fi.idFechaImplantacion")


cursor.execute("UPDATE Hechos_Implantaciones SET animalesCaza = CASE WHEN idAptitud = (SELECT idAptitud FROM Dimension_Aptitud WHERE aptitud = 'CAZA') THEN 1 ELSE 0 END")

cursor.execute("DROP TABLE ANIMALES")
cursor.execute("DROP TABLE AUXILIAR_ANIMALES1")
cursor.execute("DROP TABLE AUXILIAR_ANIMALES2")
bd.commit()
cursor.close()
bd.close()






