"""
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
    print("1- Cargar información en el catálogo.")
    print("2- Ver las n obras mas antiguas para un medio especifico.")
    print("3- Listar crónologicamente las adquisiciones.")
    print("5- Clasificar las obras por la nacionalidad de sus creadores.")
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
                artistas = controller.getArtworksartists(catalog, artwork["ConstituentID"])
                print ("ID: " + artwork["ObjectID"] + ", Título: " + artwork["Title"] + ", Artista(s): " + artistas
                    + "Fecha:  " + artwork["Date"] + ", Medio: " 
                    + artwork["Medium"])
    else:
        print ("No se encontraron obras")
    
def tamañoNacionalidades(catalog):
    """
    """
    top = controller.topNacionality(catalog)
    first = lt.firstElement(top)
    count = 0 
    print(("-" * 15) + "Top Nacionalidades con más obras obras" + ("-" * 15) + "\n")
    for x in range(1, 11):
        nac = lt.getElement(top, x)
        count += 1
        print(str(count) + ". " + str(nac["nacionalidad"]) + ": " + str(lt.size(nac["obras"]))+ "\n")
    top_1 = mp.get(catalog["nationality"], first["nacionalidad"])
    valor = me.getValue(top_1)
    obras = valor["obras"]
    first_three = controller.firstThreeD(obras)
    last_three = controller.lastThreeD(obras)
    print("-" * 84)
    print(("-" * 21) + "Estos son las 3 primeras Obras encontradas" + ("-" * 21) + "\n")
    printArtworkData(first_three)
    print("-" * 84)
    print(("-" * 22) + "Estos son las 3 ultimas Obras encontradas" + ("-" * 21) + "\n")
    printArtworkData(last_three)

def artworksBydate(catalog, startDate, finishDate):
    """
    Genera una lista cronológicamente ordenada de las obras adquiridas 
    por el museo en un rango de fecha. Retorna el total de obras en el rango cronológico, 
    total de obras adquiridas por compra y las primeras 3 y utimas 3 obras del rango. ()()()
    """
    org_dates = controller.organizeArtworkbyDate(catalog, startDate, finishDate)
    last = controller.lastThreeD(org_dates)
    first = controller.firstThreeD(org_dates)
    print("\n")
    print("Total de obras en el rango " + str(startDate) + " - " + str(finishDate) + ": " + str(lt.size(org_dates))+ "\n") 
    print("-" * 84 + "\n")
    print("Total de obras compradas en el rango: " + str(controller.countPurchase(org_dates)) + "\n")
    print("-" * 84)
    print(("-" * 21) + "Estos son las 3 primeras Obras encontradas" + ("-" * 21) + "\n")
    printArtworkData(first)
    print("-" * 84)
    print(("-" * 22) + "Estos son las 3 ultimas Obras encontradas" + ("-" * 21) + "\n")
    printArtworkData(last)
    print("-" * 84)

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
        startDate = input("Fecha de Inicio (YYYY-MM-DD): ")
        finishDate = input("Fecha Final (YYYY-MM-DD): ")
        start_time = time.process_time()
        artworksBydate(catalog, startDate, finishDate)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print ("Tiempo transcurrido: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 5:
        start_time = time.process_time()
        tamañoNacionalidades(catalog)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print ("Tiempo transcurrido: " + str(elapsed_time_mseg))
    else:
        sys.exit(0)
sys.exit(0)