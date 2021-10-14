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
 * Dario Correal - Version inicialhdihfirh
 """

from DISClib.DataStructures.arraylist import iterator
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from datetime import date, timedelta
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
                                   loadfactor=2.00,
                                   comparefunction=compareMedio)
    catalog["nationality"] = mp.newMap(1000,
                                        maptype="CHAINING",
                                        loadfactor=2.00,
                                        comparefunction=compareNacionalidad)
    catalog["artists_ID"] = mp.newMap(15223,
                                        maptype="PROBING",
                                        loadfactor=0.2)

    return catalog

#==========================
# Agregar info al catalogo
#==========================

def addArtwork(catalog,artwork):
    if artwork["DateAcquired"] == "" or artwork["DateAcquired"] == "Unknown":
        hoy = date.today()
        artwork["DateAcquired"] = hoy.strftime("%Y-%m-%d")
    if artwork["Date"] == "" or artwork["Date"] == "Unknown":
        hoy = date.today()
        artwork["DateAcquired"] = hoy.strftime("%Y-%m-%d")
    lt.addLast(catalog["artworks"], artwork)
    addArtworkMedium(catalog,artwork)

def addArtist(catalog,artist):
    lt.addLast(catalog["artists"], artist)
    info = newArtist(artist)
    mp.put(catalog["artists_ID"], artist["ConstituentID"], info)

def newArtist(artist):
    """"""
    artista = {"Nombre": "",
            "Bio": "",
            "Nacionalidad": "",
            "Genero": "",
            "Nacimiento": "",
            "Muerte": "",
            "Wiki": "",
            "ULAN": ""}
    artista["Nombre"] = artist["DisplayName"]
    artista["Bio"] = artist["ArtistBio"]
    artista["Nacionalidad"] = artist["Nationality"]
    artista["Genero"] = artist["Gender"]
    artista["Nacimiento"] = artist["BeginDate"]
    artista["Muerte"] = artist["EndDate"]
    artista["Wiki"] = artist["Wiki QID"]
    artista["ULAN"] = artist["ULAN"]
    return artista

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
    entry['obras'] = lt.newList(cmpfunction=compareDate)
    return entry

def loadNationality(catalog):
    """
    Esta funcion adiciona un artista a la lista de obras que usan un medio especifico.
    Los medios se guardan en un Map, donde la llave es el medio y el valor la lista de obras de ese medio.
    """
    for obra in lt.iterator(catalog["artworks"]):
        codes = obra["ConstituentID"]
        nacionalidades = getArtworksNationality(catalog, codes)
        for nacionalidad in lt.iterator(nacionalidades):
            if nacionalidad == " " or nacionalidad == "":
                nacionalidad = "Nationality unknown"
            existnation = mp.contains(catalog["nationality"], nacionalidad)
            if existnation:
                entry = mp.get(catalog["nationality"], nacionalidad)
                nac = me.getValue(entry)
            else:
                nac = newNation(nacionalidad)
                mp.put(catalog["nationality"], nacionalidad, nac)
            lt.addLast(nac["obras"], obra)

def newNation(nacionalidad):
    entry = {'nacionalidad': "", "obras": None}
    entry['nacionalidad'] = nacionalidad
    entry["obras"] = lt.newList('SINGLE_LINKED')
    return entry

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

def getArtworksNationality(catalog, codes):
    """
    """
    nations = lt.newList()
    cIDS = codes.replace("[", "").replace("]", "").split(",")
    for cID in cIDS:
        cID = cID.strip()
        existnation = mp.contains(catalog["artists_ID"], cID)
        if existnation:
            pareja = mp.get(catalog["artists_ID"], cID)
            nacionalidad = me.getValue(pareja)
            n = nacionalidad["Nacionalidad"]
        lt.addLast(nations, n)
    return nations

#==========================
# funciones de comparacion
#==========================

def ordenAscendente(a,b):
    if (a > b):
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

def compareNacionalidad(nacionalidad, nacentry):
    nacentry = me.getKey(nacentry)
    if (str(nacentry) == str(nacionalidad)):
        return 0
    elif (str(nacentry) < str(nacionalidad)):
        return 1
    else:
        return -1

#================
# requerimientos
#================

def obrasAntiguas(catalog,n,medio):
    """
    Devuelve una lista con las n obras mas antiguas para un medio especifico.
    """
    antiguas = lt.newList('SINGLE_LINKED',compareDate)
    fechas = lt.newList()
    medio = mp.get(catalog['medium'], medio)
    if medio:
        valor = me.getValue(medio)
    obras = valor["obras"]
    for obra in lt.iterator(obras):
        if obra['Date'] == '':
            obra['Date'] = '2022'
        lt.addLast(fechas,int(obra['Date']))
    sa.sort(fechas,ordenAscendente)
    i = 0
    while i < int(n):
        fecha = lt.removeFirst(fechas)
        o = getElementbyparameterE(obras,str(fecha))
        lt.addLast(antiguas,o)
        i += 1
    return antiguas