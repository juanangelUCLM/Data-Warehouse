#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os


bd = sqlite3.connect('IdentificacionAnimales.db')
cursor = bd.cursor()

def menu():

	os.system('clear')

	print "MENU PRINCIPAL"
	print "Selecciona una opcion:\n"
	print "1 - Mostrar el numero de animales por provincia."
	print "2 - Mostrar el numero de animales por aptitud."
	print "3 - Mostrar el numero de animales por ano de implantacion."
	print "4 - Mostrar el numero de animales por raza"
	print "5 - Salir"

 

def crearGrafica(vectorConsulta):

	ejeX = []
	ejeY = []

	for element in vectorConsulta:
		ejeX.append(element[0])
		ejeY.append(element[1])


	fig = plt.figure()
	plt.axes((0.1, 0.3, 0.8, 0.6))  
	plt.bar(range(len(ejeX)), ejeY, align = 'center', color = "y")
	plt.xticks(np.arange(len(ejeX)), ejeX, rotation = 90)
	plt.show()
	#fig.savefig('Aptitudes.jpg', dpi=fig.dpi)

def crearGrafica2(vectorConsulta):
	ejeX = []
	ejeY = []
	ejeX1 = []
	ejeY1 = []
	ejeX2 = []
	ejeY2 = []

	for element in provincias:
		ejeX.append(element[0])
		ejeY.append(element[1])
		
	ejeX1 = ejeX[:len(ejeX)/2]
	ejeY1 = ejeY[:len(ejeX)/2]
	ejeX2 = ejeX[(len(ejeX)/2)+1:]
	ejeY2 = ejeY[(len(ejeX)/2)+1:]

	fig = plt.figure()
	plt.axes((0.1, 0.3, 0.8, 0.6))  
	plt.bar(range(len(ejeX1)), ejeY1, align = 'center', color = "r") 
	plt.xticks(np.arange(len(ejeX1)), ejeX1, rotation = 90) 
	#fig.savefig('Provincias1.jpg', dpi=fig.dpi)

	fig = plt.figure()
	plt.axes((0.1, 0.3, 0.8, 0.6))  
	plt.bar(range(len(ejeX2)), ejeY2, align = 'center', color = "r")  
	plt.xticks(np.arange(len(ejeX2)), ejeX2, rotation = 90) 
	plt.show()
	#fig.savefig('Provincias2.jpg', dpi=fig.dpi)
	

while True:

	# Mostramos el menu
	menu()


	# solicituamos una opcion al usuario
	opcionMenu = raw_input("\nElige una de las opciones: ")

 

	if opcionMenu=="1":

		while True:

			print("\n\tSUBMENU-1")
			print("\tSelecciona una opcion:\n")
		
			opcionSubMenu = raw_input("\t1 - Mostrar todas las provincias (grafico de barras).\n\t2 - Introducir nombre de provincia.\n\t3 - Volver al menu principal.\n\n\tElige una de las opciones: ")

			if opcionSubMenu=="1":
				#numero de animales por provincia
				provincias = cursor.execute("SELECT dl.provincia, sum(hi.totalAnimales) as animales FROM Dimension_Localizacion dl, Hechos_Implantaciones hi WHERE dl.idLocalizacion = hi.idLocalizacion GROUP BY dl.provincia")
				crearGrafica2(provincias)
				
				
			elif opcionSubMenu=="2":
				nombreProvincia = raw_input("\n\t\tIntroduce el nombre de la provincia: ")
				numeroAnimales = cursor.execute("SELECT dl.provincia, sum(hi.totalAnimales) as animales FROM Dimension_Localizacion dl, Hechos_Implantaciones hi WHERE dl.idLocalizacion = hi.idLocalizacion AND dl.provincia = '"+ nombreProvincia + "'")
				for element in numeroAnimales:
					cadena = "\n\t\tProvincia: " + str(element[0]) + " - Numero de animales: " + str(element[1])
					print cadena
				raw_input("\n\t\tPulsa 'Intro' para continuar:")
				

			elif opcionSubMenu=="3":
				break

			else:
				print "\tOpcion incorrecta."

	elif opcionMenu=="2":
		while True:

			print("\n\tSUBMENU-2")
			print("\tSelecciona una opcion:\n")
		
			opcionSubMenu = raw_input("\t1 - Mostrar todas las aptitudes (grafico de barras).\n\t2 - Introducir aptitud.\n\t3 - Volver al menu principal.\n\n\tElige una de las opciones: ")

			if opcionSubMenu=="1":
				#numero de animales por aptitud
				aptitudes = cursor.execute("SELECT ap.aptitud, sum(he.totalAnimales) FROM Hechos_Implantaciones he, Dimension_Aptitud ap WHERE he.idAptitud = ap.idAptitud GROUP BY he.idAptitud")
				crearGrafica(aptitudes)
				#raw_input("\tPulsa 'Intro' para continuar:")
				

			elif opcionSubMenu=="2":

				codigoAptitud = raw_input("\n\t\t1 - Caza\n\t\t2 - Guarda defensa y utilidad\n\t\t3 - Lujo y compania\n\t\t4 - Pastor\n\n\t\tIntroduce el codigo de la actitud: ")
				
				if (codigoAptitud=="1" or codigoAptitud=="2" or codigoAptitud=="3" or  codigoAptitud=="4"):
					numeroAnimales = cursor.execute("SELECT ap.aptitud, sum(he.totalAnimales) FROM Hechos_Implantaciones he, Dimension_Aptitud ap WHERE he.idAptitud = ap.idAptitud AND ap.idAptitud = '"+ codigoAptitud + "'")
				for element in numeroAnimales:
					cadena = "\t\tNumero de animales: " + str(element[1])
					print cadena
					raw_input("\n\t\tPulsa 'Intro' para continuar:")
				else:
					print ("\t\tOpcion incorrecta.")

			elif opcionSubMenu=="3":
				break

			else:
				print "\tOpcion incorrecta.\n"

	elif opcionMenu=="3":

		while True:

			print("\n\tSUBMENU-3")
			print("\tSelecciona una opcion:\n")
		
			opcionSubMenu = raw_input("\t1 - Mostrar todos los anos (grafico de barras).\n\t2 - Introducir ano.\n\t3 - Volver al menu principal.\n\n\tElige una de las opciones: ")

			if opcionSubMenu=="1":
				#numero de animales por año de implantacion
				anios = cursor.execute("SELECT dfi.año AS año_implantacion , sum(hi.totalAnimales) as animales FROM Dimension_FechaImplantacion dfi, Hechos_Implantaciones hi WHERE dfi.idFechaImplantacion = hi.idFechaImplantacion GROUP BY dfi.año")
				crearGrafica(anios)
				#raw_input("\tPulsa 'Intro' para continuar:")
				

			elif opcionSubMenu=="2":
				numeroAno = raw_input("\n\t\tIntroduce un ano comprendido entre 1993-2007: ")
				numeroAnimales = cursor.execute("SELECT dfi.año AS año_implantacion , sum(hi.totalAnimales) as animales FROM Dimension_FechaImplantacion dfi, Hechos_Implantaciones hi WHERE dfi.idFechaImplantacion = hi.idFechaImplantacion AND dfi.año = '"+ numeroAno + "'")
				for element in numeroAnimales:
					cadena = "\n\t\tAno: " + str(element[0]) + " - Numero de animales: " + str(element[1])
					print cadena
					raw_input("\n\t\tPulsa 'Intro' para continuar:")

			elif opcionSubMenu=="3":
				break

			else:
				print "\tOpcion incorrecta."

	elif opcionMenu=="4":

		while True:

			print("\n\tSUBMENU-4")
			print("\tSelecciona una opcion:\n")
		
			opcionSubMenu = raw_input("\t1 - Mostrar el numero de animales por raza (Mostramos solo las 20 razas con mayor numero)(grafico de barras).\n\t2 - Volver al menu principal.\n\n\tElige una de las opciones: ")

			if opcionSubMenu=="1":
				#numero de animales por raza (mostramos solo las 20 razas con mas animales)
				razas = cursor.execute("SELECT dr.raza, sum(hi.totalAnimales) as animales FROM Dimension_Raza dr, Hechos_Implantaciones hi WHERE dr.idRaza = hi.idRaza GROUP BY dr.raza ORDER BY animales DESC LIMIT 20")
				crearGrafica(razas)
				#raw_input("\tPulsa 'Intro' para continuar:")
				

			elif opcionSubMenu=="2":
				break

			else:
				print "\tOpcion incorrecta."

	elif opcionMenu=="5":

		print "Gracias por usar la aplicacion. Saliendo..."

		break

	else:

		print ""

		raw_input("Opcion incorrecta. Pulsa 'Intro' para continuar:")


