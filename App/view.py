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
assert cf
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#========================================================================
# Funciones iniciales
#========================================================================

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronologicamente los artistas")
    print("4- Clasificar las obras de los artistas por tecnica")
    print("6- Calcular costo de transportar las obras de un departamento")
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

#========================================================================
# Especificaciones de la impresion de datos
#========================================================================

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

def printArtistData_Req1(artists):
    size = lt.size(artists)
    if size>0:
        for artist in lt.iterator(artists):
            print ("Nombre: " + artist["DisplayName"] + ", Año nacimiento:  " 
                    + artist["BeginDate"] + ", Año fallecimiento: " + artist["EndDate"]
                    + ", Nacionalidad: " + artist["Nationality"] + ", Género: " + artist["Gender"])
    else:
        print ("No se encontraron artistas")

def printArtworkData_Req3(artworks):
    size = lt.size(artworks)
    if size>0:
        for artwork in lt.iterator(artworks):
            print ("ID: " + artwork["ObjectID"] + ", Título: " + artwork["Title"] 
                    + ", Fecha:  " + artwork["Date"] + ", Medio: " 
                    + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
    else:
        print ("No se encontraron artistas")

def printArtworkData_Req5(artworks):
    size = lt.size(artworks)
    if size>0:
        for artwork in lt.iterator(artworks):
            print ("ID: " + artwork["ObjectID"] + ", Título: " + artwork["Title"] 
                    + ", ID artistas: " + artwork['ConstituentID'] + ", Clasificacion: " 
                    + artwork['Classification'] + ", Fecha:  " + artwork["Date"] + ", Medio: " 
                    + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"] 
                    + ", Costo de transporte (USD): " + str(int(artwork['Transcost (USD)'])))
    else:
        print ("No se encontraron artistas")

#==========================================================================
# Requerimientos
#==========================================================================

def requerimiento1(catalog, anio_inicial, anio_final):
    """
    Genera una lista cronológicamente ordenada de los artistas en un rango de anios.
    Retorna el total de artistas en el rango cronológico, y los primeros 3 y ultimos 3 artistas del rango.
    """
    org_anio = controller.artistsbyAnio(catalog, anio_inicial, anio_final)
    print("\n")
    print("Total de artistas en el rango " + str(anio_inicial) + " - " + str(anio_final) + ": " + str(lt.size(org_anio)))
    print("-" * 50)
    last = controller.lastThreeD(org_anio)
    first = controller.firstThreeD(org_anio)
    print ("  Estos son los 3 primeros Artistas encontrados: ")
    printArtistData_Req1(first)
    print("-" * 50)
    print ("  Estos son los 3 ultimos Artistas encontrados: ")
    printArtistData_Req1(last)
    print("-" * 50)

def requerimiento3(catalog,nombre):
    artworks = controller.artworksbyArtist(catalog,nombre)
    print("\n")
    print("Total de obras del artista " + str(nombre) + ": " + str(lt.size(artworks)))
    lista = controller.artworksbyMedium(artworks)
    medios = controller.contarMedios(artworks)
    medio_max = controller.medioMax(lista)
    print("-" * 50)
    print("Total de medios usados por el artista en sus obras: " + str(medios))
    print("-" * 50)
    print("La técnica más usada por el artista es: " + str(medio_max))
    print("-" * 50)
    print("Listado de obras con la técnica más usada: ")
    printArtworkData_Req3(lista)

def requerimiento5(catalog,department):
    obras = controller.artworksbyDepartment(catalog,department)
    resultado = controller.costoTotal_masCostosas(obras)
    total = lt.removeFirst(resultado)
    costosas = lt.removeLast(resultado)
    peso = controller.pesoTotal(obras)
    antiguas = controller.masAntiguas(obras)
    print('Total de obras para transportar: ' + str(lt.size(obras)))
    print("-" * 50)
    print('Costo total estimado de transportar las obras (USD): ' + str(total))
    print("-" * 50)
    print('Peso total estimado de las obras (kg): ' + str(peso))
    print("-" * 50)
    print('Las 5 obras más antiguas a transportar son: ')
    print("-" * 50)
    printArtworkData_Req5(antiguas) 
    print("-" * 50)
    print('Las 5 obras más costosas a transportar son: ')
    print("-" * 50)
    printArtworkData_Req5(costosas)
    
#====================================================================================
# Menu principal
#====================================================================================

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        start_time = time.process_time()
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print("-" * 74)
        print('Obras cargadas: ' + str(lt.size(catalog['artworks']))+ "\n")
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])) + "\n")
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo de ejecución: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 2:
        anio_inicial = input("Ingrese el año inicial: ")
        anio_final = input("Ingrese el año final: ")
        start_time = time.process_time()
        requerimiento1(catalog, anio_inicial, anio_final)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo de ejecución: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 4:
        nombre = input("Ingrese el nombre del artista: ")
        start_time = time.process_time()
        requerimiento3(catalog,nombre)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo de ejecución: " + str(elapsed_time_mseg))

    elif int(inputs[0]) == 6:
        department = input("Ingrese el nombre del departamento del museo: ")
        start_time = time.process_time()
        requerimiento5(catalog,department)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("Tiempo de ejecución: " + str(elapsed_time_mseg))    

    else:
        sys.exit(0)
sys.exit(0)