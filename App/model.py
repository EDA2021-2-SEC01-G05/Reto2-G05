﻿"""
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

#======================================================================
# Construccion de modelos
#======================================================================

def newCatalog(type):
    """ 
    """
    catalog = {'artworks': None,
               'artists': None,
               'obbyArt': None,
               'departament': None}

    """
    """
    catalog["artworks"] = lt.newList(type, 
                                    cmpfunction=None)
    catalog["artists"] = lt.newList(type, 
                                    cmpfunction=None)
    # Map requerimiento 3
    catalog['obbyArt'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtist)
    # Map requerimiento 5
    catalog['department'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareDepartmentM)

    return catalog

#===========================================================
# Agregar info al catalogo
#===========================================================

def addArtwork(catalog,artwork):
    lt.addLast(catalog["artworks"], artwork)
    addArtworkbyArtist(catalog,artwork)
    addArtworkbyDepartment(catalog,artwork)

def addArtist(catalog,artist):
    lt.addLast(catalog["artists"], artist)

# Requerimiento 3
def addArtworkbyArtist(catalog,artwork):
    """
    Agregar las obras correspondientes a cada artista en el Map catalog['obbyArt']
    """
    mapa = catalog['obbyArt']
    if artwork['ConstituentID'] != '':
        ide = artwork['ConstituentID']
    else:
        ide = "[0]"
    
    ides = ide.strip('[]')
    artistas = ides.split(',')

    for artista in artistas:
        existartista = mp.contains(mapa,artista)
        if existartista:
            entry = mp.get(mapa,artista)
            artist = me.getValue(entry)
        else:
            artist = newArtista(artista)
            mp.put(mapa, artista, artist)
        lt.addLast(artist['obras'], artwork)

def newArtista(artista):
    """
    Esta funcion crea la estructura de obras asociadas a un artista.
    """
    entry = {'artista': "", "obras": None}
    entry['artista'] = artista
    entry['obras'] = lt.newList('SINGLE_LINKED', compareDate)
    return entry

# Requerimiento 5
def addArtworkbyDepartment(catalog,artwork):
    """
    Esta funcion adiciona una obra a la lista de obras de un departamento especifico.
    Los datos se guardan en un Map, donde la llave es el departamento y el valor la lista de obras de ese departamento.
    """
    departments = catalog['department']
    if artwork['Department'] != '':
        department = artwork['Department']
    else:
        department = "Ninguno"

    existdep = mp.contains(departments,department)
    if existdep:
        entry = mp.get(departments,department)
        dep = me.getValue(entry)
    else:
        dep = newDep(department)
        mp.put(departments, department, dep)
    lt.addLast(dep['obras'], artwork)

def newDep(department):
    """
    Esta funcion crea la estructura de obras asociadas a un departamento.
    """
    entry = {'departamento': "", "obras": None}
    entry['departamento'] = department
    entry['obras'] = lt.newList('SINGLE_LINKED', compareDate)
    return entry

#============================================================
# Funciones basicas o complementarias
#============================================================

def getElementbyparameter(lista, parameter):
    """
    Retorna un elemento de una lista dado un parametro, no lo elimina de la lista
    """
    pos = lt.isPresent(lista, parameter)
    if pos > 0:
        element = lt.getElement(lista, pos)
        return element
    else:
        return None

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

#======================================================
# Funciones de comparacion
#======================================================

# Se usan en varios requerimientos
def ordenAscendente(a,b):
    if (a > b):
        return 0
    return -1

# Se usan en requerimiento 1
def compareAnio(anio, artist):
    if anio in artist["BeginDate"]:
        return 0
    return -1

def ordAscArtiAnio(a,b):
    if int(a['BeginDate']) > int(b['BeginDate']):
        return 0
    return -1

# Se usan en requerimiento 3
def compareArtist(artist,artentry):
    artentry = me.getKey(artentry)
    if (str(artentry) == str(artist)):
        return 0
    return -1

def compareNames(nombre,artist):
    if nombre in artist["DisplayName"]:
        return 0
    return -1

def compareMedium(medium, artwork):
    if (medium in artwork["Medium"]):
        return 0
    return -1

# Se usan en requerimiento 5
def compareDepartmentM(departament, depentry):
    depentry = me.getKey(depentry)
    if (str(depentry) == str(departament)):
        return 0
    return -1

def compareDepartment(department, artwork):
    if department in artwork['Department']:
        return 0
    return -1

def compareDate(date,artwork):
    if date in artwork['Date']:
        return 0
    if date == '':
        return -1
    return -1

def ordAscArtwDate(a,b):
    fecha1 = a['Date']
    fecha2 = b['Date']
    if fecha1 != '' and fecha2 != '':
        if int(fecha1) > int(fecha2):
            return 0
        else:
            return -1
    elif fecha1 == '' and fecha2 == '':
        return 0
    elif fecha1 == '' and fecha2 != '':
        return 0
    elif fecha1 != '' and fecha2 == '':
        return -1

def ordAscArtwCost(a,b):
    if (a['Transcost (USD)'] > b['Transcost (USD)']):
        return 0
    return -1

#====================================================================
# Funciones propias de los requerimientos
#====================================================================

#-----------------
# Requerimiento 1
#-----------------

def artistsbyAnio(catalog,anio_inicial,anio_final):
    """
    Organiza y retorna los artistas que esten en un rango de una fecha inicial y final.
    """
    artistas = copiarLista(catalog['artists'],compareAnio)
    ms.sort(artistas,ordAscArtiAnio)
    pos = lt.isPresent(artistas,str(anio_inicial))
    pos_f = lt.isPresent(artistas,str(anio_final))
    l = int(pos_f)-int(pos)
    artists = lt.subList(artistas,pos,l+2)
    return artists

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

#------------------
# Requerimiento 3
#------------------

def artworksbyArtist(catalog,nombre):
    """
    Retorna una lt con las obras de un artista por su nombre.
    """
    copia = copiarLista(catalog['artists'],compareNames)
    artista = getElementbyparameter(copia,nombre)
    ide = artista['ConstituentID']
    artist = mp.get(catalog['obbyArt'], ide)
    if artist:
        obras = me.getValue(artist)['obras']
    return obras

def listaMedios(obras):
    """
    Retorna lista con representantes unicos para cada medio que se usa en una lista de obras 
    """
    first = lt.firstElement(obras)
    medios = lt.newList("SINGLE_LINKED",cmpfunction=compareMedium)
    lt.addFirst(medios,first)        
    for obra in lt.iterator(obras):
        i = 0
        for medio in lt.iterator(medios):
            if (str(obra['Medium']) == str(medio['Medium'])):
                i += 1
        if (i == 0):
            lt.addLast(medios,obra)
    return medios
    
def artworksbyMedium(obras):
    """
    Retorna un lt con las obras que usan la tecnica o medio mas recurrente en obras.
    """
    # contamos numero de veces que aparece cada medio y agregamos este numero a una lista (numeros)
    medios = listaMedios(obras)
    numeros = lt.newList()
    for medio in lt.iterator(medios):
        i = 0
        for obra in lt.iterator(obras):
            if (medio['Medium'] == obra['Medium']):
                i += 1
        lt.addLast(numeros,i)
    # ordenamos la lista y sacamos el numero mas grande
    ms.sort(numeros,cmpfunction=ordenAscendente)
    num = lt.lastElement(numeros)
    # hallamos el medio (medio) correspondiente a este numero mas grande (num)
    for medio in lt.iterator(medios):
        i = 0
        for obra in lt.iterator(obras):
            if (medio['Medium'] == obra['Medium']):
                i += 1
        if i is num:
            break
    # hacemos una lista (lista) con las obras que usan el medio hallado (medio)
    lista = lt.newList()
    if medio is not None:
        for obra in lt.iterator(obras):
            if (obra['Medium'] ==  medio['Medium']):
                lt.addLast(lista,obra)
        return lista

def contarMedios(obras):
    """
    Cuenta la cantidad de medios que se usan en una lista de obras
    """
    medios = listaMedios(obras)
    num = lt.size(medios)
    return num 

#------------------
# Requerimiento 5
#------------------

def artworksbyDepartment(catalog,department):
    """
    Retorna la lista de las obras en un departamento.
    """
    dep = mp.get(catalog['department'],department)
    if dep:
        obras = me.getValue(dep)['obras']
    return obras

def costoTransporte(obras):
    """
    Calcular el costo de transporte de cada obra en obras y agregar el dato al elemento correspondiente.
    """
    for obra in lt.iterator(obras):
        # sacar los datos relevantes y estipular valores por defecto
        peso = obra['Weight (kg)']
        largo = obra['Length (cm)']
        ancho = obra['Width (cm)']
        profundidad = obra['Depth (cm)']
        altura = obra['Height (cm)']
        if peso is "":
            peso = 0
        else:
            peso = float(peso)
        if largo is "":
            largo = 0
        if ancho is "":
            ancho = 0
        if profundidad is "":
            profundidad = 0
        if altura is "":
            altura = 0
        # calcular el tamano (tres posibles formas)
        t1 = (float(ancho)/100)*(float(altura)/100)
        t2 = (float(ancho)/100)*(float(largo)/100)
        t3 = (float(ancho)/100)*(float(altura)/100)*(float(profundidad)/100)
        # crear lista para comparar los tamanos y sacar el mas grande
        lista = lt.newList()
        lt.addLast(lista,peso)
        lt.addLast(lista,t3)
        lt.addLast(lista,t2)
        lt.addLast(lista,t1)
        ms.sort(lista,cmpfunction=ordenAscendente)
        tamano = lt.lastElement(lista)
        # estipular el costo y agregarlo a los datos de la obra
        if tamano == 0:
            costo = 48
        else:
            costo = tamano*72
        obra['Transcost (USD)'] = costo
    return obras

def costoTotal(obras):
    """
    Calcula el costo total de transportar unas obras.
    """
    ob = costoTransporte(obras)
    t = 0
    for o in lt.iterator(ob):
        c = o['Transcost (USD)']
        t += float(c)
    return int(t)

def pesoTotal(obras):
    """
    Calcula el peso total de las obras
    """
    w = 0
    for obra in lt.iterator(obras):
        peso = obra['Weight (kg)']
        if peso is "":
            peso = 0
        w += float(peso)
    return int(w)

def masAntiguas(obras):
    """
    Retorna una lista con las 5 obras mas antiguas de obras 
    """
    ms.sort(obras,ordAscArtwDate)
    antiguas = lt.newList()
    i = 0
    while i < 5:
        o = lt.removeFirst(obras)
        lt.addLast(antiguas,o)
        i += 1
    return antiguas

def masCostosas(obras):
    """
    Retorna una lista con las 5 obras mas costosas de obras 
    """
    o = costoTransporte(obras)
    ms.sort(o,ordAscArtwCost)
    costosas = lt.newList()
    i = 0
    while i < 5:
        ob = lt.removeLast(o)
        lt.addLast(costosas,ob)
        i += 1
    return costosas