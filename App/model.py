"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

#=========================
# Construccion de modelos
#=========================

def newCatalog(type):
    """ 
    """
    catalog = {'artworks': None,
               'artists': None,
               'medium': None}

    """
    """
    catalog["artworks"] = lt.newList(type, 
                                    cmpfunction=compareDates)
    catalog["artists"] = lt.newList(type, 
                                    cmpfunction=compareCID)
    catalog['medium'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMedio)
    return catalog

#==========================
# Agregar info al catalogo
#==========================

def addArtwork(catalog,artwork):
    lt.addLast(catalog["artworks"], artwork)
    addArtworkMedium(catalog,artwork)

def addArtworkMedium(catalog,artwork):
    """
    Esta funcion adiciona una obra a la lista de obras que usan un medio especifico.
    Los medios se guardan en un Map, donde la llave es el medio y el valor la lista de obras de ese medio.
    """
    medios = catalog['medium']
    if artwork['Medium'] != '':
        medio = artwork['Medium']
    else:
        medio = "Ninguno"
    existmedio = mp.contains(medios,medio)
    if existmedio:
        entry = mp.get(medios,medio)
        med = me.getValue(entry)
    else:
        med = newMedio(medio)
        mp.put(medios, medio, med)
    lt.addLast(med['obras'], artwork)

def newMedio(medio):
    """
    Esta funcion crea la estructura de obras asociadas a un medio.
    """
    entry = {'medio': "", "obras": None}
    entry['medio'] = medio
    entry['obras'] = lt.newList('SINGLE_LINKED', compareDate)
    return entry

def addArtist(catalog,artist):
    lt.addLast(catalog["artists"], artist)

#=================================
# consultar info, modificar datos
#=================================

def getElementbyparameterE(lista, parameter):
    """
    Retorna un elemento de una lista dado un parametro, luego, lo elimina de la lista
    """
    pos = lt.isPresent(lista, parameter)
    if pos > 0:
        element = lt.getElement(lista, pos)
        lt.deleteElement(lista, pos)
        return element
    else:
        return None

def copiarLista(lista, cmpf):
    """
    Copia una lista con nueva cmpfunction cmpf
    """
    copia = lt.newList("ARRAY_LIST",cmpf)
    for elemento in lt.iterator(lista):
        lt.addLast(copia,elemento)
    return copia

#==========================
# funciones de comparacion
#==========================

def ordenAscendente(a,b):
    if (a > b):
        return 0
    return -1

def ordAscArtAnio(a,b):
    if int(a['BeginDate']) > int(b['BeginDate']):
        return 0
    return -1

def compareOID(OID, artwork):
    if (OID in artwork['ObjectID']):
        return 0
    return -1

def compareDates(date_1, artwork):
    if (date_1 in artwork["DateAcquired"]):
        return 0
    return -1

def compareCID(cID, artist):
    if cID == artist["ConstituentID"]:
        return 0
    return -1

def compareMedio(medio, medentry):
    medentry = me.getKey(medentry)
    if (str(medentry) == str(medio)):
        return 0
    return -1

def compareDate(date,artwork):
    if date in artwork['Date']:
        return 0
    return -1

def compareAnio(anio, artist):
    if anio in artist["BeginDate"]:
        return 0
    return -1

#================
# requerimientos
#================

#-----------------
# requerimiento 1
#-----------------

def artistsbyAnio(catalog,anio_inicial,anio_final):
    """
    Organiza y retorna los artistas que esten en un rango de una fecha inicial y final.
    """
    artistas = copiarLista(catalog['artists'],compareAnio)
    ms.sort(artistas,ordAscArtAnio)
    pos = lt.isPresent(artistas,str(anio_inicial))
    pos_f = lt.isPresent(artistas,str(anio_final))
    l = int(pos_f)-int(pos)
    artistas = lt.subList(artistas,pos,l+2)
    return artistas

def firstThreeD(lista):
    """
    Retorna una lista con los tres primeros elementos de una lista.
    """
    first = lt.subList(lista,1,3)
    return first

def lastThreeD(lista):
    """
    Retorna una lista con los 3 ultimos elementos de una lista.
    """
    last = lt.subList(lista,lt.size(lista)-2,3)
    return last

#--------
# lab 5
#--------

def obrasAntiguas(catalog,n,medio):
    """
    Devuelve una lista con las n obras mas antiguas para un medio especifico.
    """
    antiguas = lt.newList('SINGLE_LINKED',compareDate)
    fechas = lt.newList()
    medio = mp.get(catalog['medium'], medio)
    if medio: 
        obras = me.getValue(medio)['obras']
    for obra in lt.iterator(obras):
        lt.addLast(fechas,int(obra['Date']))
    ms.sort(fechas,ordenAscendente)
    i = 0
    while i < int(n):
        fecha = lt.removeFirst(fechas)
        o = getElementbyparameterE(obras,str(fecha))
        lt.addLast(antiguas,o)
        i += 1
    return antiguas