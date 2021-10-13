﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config as cf
import sys
import controller 
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitadaooohdiohcoi
"""
#=====================
# funciones iniciales
#=====================

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Ver las n obras mas antiguas para un medio especifico")
    print("3- Cantidad de obras por nacionalidad.")
    print("0-  Salir")
    
def initCatalog():
    """
    Inicializa el catalogo de obras
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga las obras en la estructura de datos
    """
    return controller.loadData(catalog)

catalog = None

#===========================================
# especificaciones de la impresion de datos
#===========================================

def printArtworkData(artworks):
    size = lt.size(artworks)
    if size>0:
        for artwork in lt.iterator(artworks):
            if artwork is not None:
                print ("ID: " + artwork["ObjectID"] + ", Título: " + artwork["Title"] 
                    + ", Fecha:  " + artwork["Date"] + ", Medio: " 
                    + artwork["Medium"])
    else:
        print ("No se encontraron obras")
    
def tamañoNacionalidades(catalog):
    """
    """
    keys = mp.keySet(catalog["nationality"])
    for key in lt.iterator(keys):
        entry = mp.get(catalog["nationality"], key)
        nac = me.getValue(entry)
        print (str(key) + ": " + str(lt.size(nac["obras"])))

#=================
# requerimientos
#=================

def lab5(catalog,n,medio):
    obras = controller.obrasAntiguas(catalog,n,medio)
    printArtworkData(obras)

#=================
# Menu principal
#=================

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        start_time = time.process_time()
        loadData(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("-" * 74)
        print('Obras cargadas: ' + str(lt.size(catalog['artworks']))+ "\n")
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])) + "\n")
        print ("Tiempo de carga: " + str(elapsed_time_mseg))
    
    elif int(inputs[0]) == 2:
        n = input("Ingrese el numero de obras que quiere ver: ")
        medio = input("Ingrese el medio o tecnica: ")
        start_time = time.process_time()
        lab5(catalog,n,medio)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print ("Tiempo transcurrido: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        tamañoNacionalidades(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print ("Tiempo transcurrido: " + str(elapsed_time_mseg))
    else:
        sys.exit(0)
sys.exit(0)