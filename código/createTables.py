#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os


print "Creando base de datos"

con = sqlite3.connect('IdentificacionAnimales.db')
cursor = con.cursor()

print "La base de datos se ha creado correctamente"

#CREAMOS LAS TABLAS

cursor.execute(''' CREATE TABLE ANIMALES (
  idChip			varchar(100),
  fechaImplantacion 		varchar(50),
  sexo 				varchar(1),
  raza 	  			varchar(50),
  aptitud	  		varchar(50),
  provincia 	 		varchar(50),
  municipio		  	varchar(50),
  difTiempoNacImp		integer(10)
);''')

cursor.execute(''' CREATE TABLE AUXILIAR_ANIMALES1 (
  idChip			varchar(100) PRIMARY KEY,
  fechaImplantacion 		varchar(50),
  sexo 				varchar(1),
  raza 	  			varchar(50),
  aptitud	  		varchar(50),
  provincia 	 		varchar(50),
  municipio		  	varchar(50),
  difTiempoNacImp		integer(10)
);''')

cursor.execute(''' CREATE TABLE AUXILIAR_ANIMALES2 (
  fechaImplantacion 		varchar(50),
  sexo				varchar(1),
  raza 	  			varchar(50),
  aptitud	  		varchar(50),
  provincia 	 		varchar(50),
  municipio		  	varchar(50),
  difTiempoNacImp		integer(10),
  totalAnimales			integer

);''')


cursor.execute(''' CREATE TABLE Dimension_FechaImplantacion (	
  idFechaImplantacion	INTEGER PRIMARY KEY,
  fecha					date,
  dia					integer(2),
  mes					integer(2),
  año					integer(4)	
);''')

cursor.execute(''' CREATE TABLE Dimension_Localizacion (	
  idLocalizacion		INTEGER PRIMARY KEY,
  municipio				varchar(50),
  provincia				varchar(50)	
);''')

cursor.execute(''' CREATE TABLE Dimension_Sexo (	
  idSexo		INTEGER PRIMARY KEY,
  sexo			varchar(1)	
);''')


cursor.execute(''' CREATE TABLE Dimension_Aptitud (	
  idAptitud		INTEGER PRIMARY KEY,
  aptitud			varchar(50)	
);''')

cursor.execute(''' CREATE TABLE Dimension_Raza (	
  idRaza		INTEGER PRIMARY KEY,
  raza			varchar(50)	
);''')

cursor.execute(''' CREATE TABLE Hechos_Implantaciones (
  idFechaImplantacion		INTEGER,
  idSexo			INTEGER,
  idRaza			INTEGER,
  idAptitud			INTEGER,
  idLocalizacion		INTEGER,
  difTiempoNacImp		INTEGER,
  totalAnimales			INTEGER,
  animalesCaza			INTEGER,
  PRIMARY KEY(idFechaImplantacion, idSexo, idRaza, idAptitud, idLocalizacion),
  FOREIGN KEY(idFechaImplantacion) REFERENCES Dimension_FechaImplantacion(idFechaImplantacion),
  FOREIGN KEY(idSexo) REFERENCES Dimension_Sexo(idSexo),
  FOREIGN KEY(idRaza) REFERENCES Dimension_Raza(idRaza),
  FOREIGN KEY(idAptitud) REFERENCES Dimension_Aptitud(idAptitud),
  FOREIGN KEY(idLocalizacion) REFERENCES Dimension_Localizacion(idLocalizacion)
);''')

con.commit()
cursor.close()
con.close()





