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
from DISClib.Algorithms.Sorting import mergesort as ms
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
    catalog["dates_artworks"] =mp.newMap(10000, 
                                            maptype="PROBING",
                                            loadfactor=0.2, 
                                            comparefunction=compareFecha)
    catalog['obbyArt'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareArtistD)
    # Map requerimiento 5
    catalog['department'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareDepartmentD)
    # Map requerimiento 5
    catalog['depCosto'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareDepartmentD)
    # Map requerimiento 5
    catalog['depAntiguas'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareDepartmentD)
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
    addDate_Artworks(catalog, artwork)
    addArtworkbyArtistD(catalog,artwork)
    addArtworkbyDepartmentD(catalog,artwork)
    addArtworkbyDepCostoD(catalog,artwork)
    addArtworkbyDepAntiguasD(catalog,artwork)

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

def addDate_Artworks(catalog, artwork):
    """
    """
    fechas = catalog['dates_artworks']
    fecha = artwork["DateAcquired"]
    existfecha = mp.contains(fechas,fecha)
    if existfecha:
        entry = mp.get(fechas,fecha)
        date = me.getValue(entry)
    else:
        date = newDate(fecha)
        mp.put(fechas, fecha, date)
    lt.addLast(date['obras'], artwork)

def newDate(fecha):
    entry = {'fecha': "", "obras": None}
    entry['fecha'] = fecha
    entry["obras"] = lt.newList('SINGLE_LINKED')
    return entry

def addArtworkbyArtistD(catalog,artwork):
    """
    Esta funcion adiciona una obra a la lista de obras de un artista especifico.
    Los datos se guardan en un Map, donde la llave es el ID del artista y el valor la lista de obras de ese artista.
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
            artist = newArtistaD(artista)
            mp.put(mapa, artista, artist)
        lt.addLast(artist['obras'], artwork)

def newArtistaD(artista):
    """
    Esta funcion crea la estructura de obras asociadas a un artista.
    """
    entry = {'artista': "", "obras": None}
    entry['artista'] = artista
    entry['obras'] = lt.newList()
    return entry

# Requerimiento 5
def addArtworkbyDepartmentD(catalog,artwork):
    """
    Esta funcion adiciona una obra a la lista de obras de un departamento especifico.
    Los datos se guardan en un Map, donde la llave es el departamento y 
    el valor la estructura de obras por departamento de newDep().
    """
    obra = costoTransporteD(artwork)
    costo = obra['Transcost (USD)']
    peso = obra['Weight (kg)']
    if peso == '':
        peso = 0
    
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
        dep = newDepD(department)
        mp.put(departments,department,dep)

    dep['costo'] += float(costo)
    dep['peso'] += float(peso)
    lt.addLast(dep['obras'],obra)

def newDepD(department):
    """
    Esta funcion crea la estructura de obras por departamento para el map catalog['department'].
    """
    entry = {'departamento': "", 'costo': "", 'peso': "", "obras": None}
    entry['departamento'] = department
    entry['costo'] = 0
    entry['peso'] = 0
    entry['obras'] = lt.newList()
    return entry

def addArtworkbyDepCostoD(catalog,artwork):
    """
    Esta funcion adiciona las obras costosas a la lista de obras de un departamento especifico.
    Los datos se guardan en un Map, donde la llave es el departamento y 
    el valor la estructura de obras por departamento de newDepartment().
    """
    obra = costoTransporteD(artwork)
    costo = obra['Transcost (USD)']
    if int(costo) >= 90:
        departments = catalog['depCosto']
        if artwork['Department'] != '':
            department = artwork['Department']
        else:
            department = "Ninguno"

        existdep = mp.contains(departments,department)
        if existdep:
            entry = mp.get(departments,department)
            dep = me.getValue(entry)
        else:
            dep = newDepartmentD(department)
            mp.put(departments,department,dep)

        lt.addLast(dep['obras'],obra)

def newDepartmentD(department):
    """
    Esta funcion crea la estructura de obras por departamento para el map catalog['depCosto'].
    """
    entry = {'departamento': "", "obras": None}
    entry['departamento'] = department
    entry['obras'] = lt.newList("ARRAY_LIST")
    return entry

def addArtworkbyDepAntiguasD(catalog,artwork):
    """
    Esta funcion adiciona las obras antiguas a la lista de obras de un departamento especifico.
    Los datos se guardan en un Map, donde la llave es el departamento y 
    el valor la estructura de obras por departamento de newDepartment().
    """
    obra = costoTransporteD(artwork)
    fecha = artwork['Date']
    if fecha == '':
        fecha = '2022'
    if int(fecha) <= 1900:
        departments = catalog['depAntiguas']
        if artwork['Department'] != '':
            department = artwork['Department']
        else:
            department = "Ninguno"

        existdep = mp.contains(departments,department)
        if existdep:
            entry = mp.get(departments,department)
            dep = me.getValue(entry)
        else:
            dep = newDepartmentAD(department)
            mp.put(departments,department,dep)

        lt.addLast(dep['obras'],obra)

def newDepartmentAD(department):
    """
    Esta funcion crea la estructura de obras por departamento para el map catalog['depCosto'].
    """
    entry = {'departamento': "", "obras": None}
    entry['departamento'] = department
    entry['obras'] = lt.newList("SINGLE_LINKED")
    return entry

#=================================
# consultar info, modificar datos
#=================================

def getElementbyparameterD(lista, parameter):
    """
    Retorna un elemento de una lista dado un parametro, no lo elimina de la lista
    """
    pos = lt.isPresent(lista, parameter)
    if pos > 0:
        element = lt.getElement(lista, pos)
        return element
    else:
        return None

def getElementbyparameterED(lista, parameter):
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

def copiarListaD(lista, cmpf):
    """
    Copia una lista con nueva cmpfunction cmpf
    """
    copia = lt.newList("ARRAY_LIST",cmpf)
    for elemento in lt.iterator(lista):
        lt.addLast(copia,elemento)
    return copia

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

def getArtworksartists(catalog, codes):
    """
    """
    artistas = ""
    cIDS = codes.replace("[", "").replace("]", "").split(",")
    for cID in cIDS:
        cID = cID.strip()
        existnation = mp.contains(catalog["artists_ID"], cID)
        if existnation:
            pareja = mp.get(catalog["artists_ID"], cID)
            valor = me.getValue(pareja)
            nombre = valor["Nombre"]
        artistas += nombre + " "
    return artistas

def getArtworksbyDate(catalog, date, org):
    """
    """
    fechas = catalog["dates_artworks"]
    existdate = mp.contains(fechas, date)
    if existdate:
        pareja = mp.get(fechas, date)
        valor = me.getValue(pareja)
        obras = valor["obras"]
        for obra in lt.iterator(obras):
            lt.addLast(org, obra)

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

#==========================
# funciones de comparacion
#==========================

def ordenAscendente(a,b):
    if (a > b):
        return 0
    return -1

def ordenAscendenteD(a,b):
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

def compareFecha(fecha, fechaentry):
    fechaentry = me.getKey(fechaentry)
    if (str(fechaentry) == str(fecha)):
        return 0
    elif (str(fechaentry) < str(fecha)):
        return 1
    else:
        return -1

def compareSizes(nacionality1, nacionality2):
    return (lt.size(nacionality1["obras"]) > lt.size(nacionality2["obras"]))

def compareAlphabet(artwork1, artwork2):
    return(artwork1["Title"] < artwork2["Title"])

def compareAnioD(anio, artist):
    if anio in artist["BeginDate"]:
        return 0
    return -1

def ordAscArtiAnioD(a,b):
    if int(a['BeginDate']) > int(b['BeginDate']):
        return 0
    return -1

def compareArtistD(artist,artentry):
    artentry = me.getKey(artentry)
    if (str(artentry) == str(artist)):
        return 0
    return -1

def compareNamesD(nombre,artist):
    if nombre in artist["DisplayName"]:
        return 0
    return -1

def compareMediumD(medium, artwork):
    if (medium in artwork["Medium"]):
        return 0
    return -1

def compareCIDD(CID, element):
    if (CID in element['ConstituentID']):
        return 0
    return -1

# Se usan en requerimiento 5
def compareDepartmentD(departament, depentry):
    depentry = me.getKey(depentry)
    if (str(depentry) == str(departament)):
        return 0
    return -1

def ordAscArtwDateD(a,b):
    if a['Date'] != '' and b['Date'] != '':
        if int(a['Date']) > int(b['Date']):
            return 0
        else:
            return -1
    elif a['Date'] == '' and b['Date'] == '':
        return 0
    elif a['Date'] == '' and b['Date'] != '':
        return 0
    elif a['Date'] != '' and b['Date'] == '':
        return -1

def ordAscArtwCostD(a,b):
    if (a['Transcost (USD)'] > b['Transcost (USD)']):
        return 0
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
        o = getElementbyparameterED(obras,str(fecha))
        lt.addLast(antiguas,o)
        i += 1
    return antiguas

def topNacionality(catalog):
    """
    Organiza el Top de Nacionalidades con más obras y tambien organiza 
    alfabeticamente las obras de una nacionalidad.
    """
    keys = mp.keySet(catalog["nationality"])
    top = lt.newList()
    for key in lt.iterator(keys):
        entry = mp.get(catalog["nationality"], key)
        nac = me.getValue(entry)
        lt.addLast(top, nac)
    ms.sort(top, cmpfunction=compareSizes)
    return top

def organizeArtworkbyDate(catalog, startDate, finishDate):
    """
    Organiza y retorna las obras que esten en un rango de 
    una fecha inicial y final.
    """
    org = lt.newList()
    d_0 = date.fromisoformat(startDate)
    d_f = date.fromisoformat(finishDate)
    delta = d_f - d_0
    for day in range(delta.days + 1):
        new_day = d_0 + timedelta(days=day)
        new_date = new_day.strftime("%Y-%m-%d")
        getArtworksbyDate(catalog, new_date, org)
    return org

def countPurchase(artworks):
    """
    Cuenta la cantidad de obras que fueron adquiridas por compra.
    """
    size = lt.size(artworks)
    count_p = 0
    if size:
        for artwork in lt.iterator(artworks):
            if "purchase" in artwork["CreditLine"].lower():
                count_p +=1    
    return count_p

def artistsbyAnioD(catalog,anio_inicial,anio_final):
    """
    Organiza y retorna los artistas que esten en un rango de una fecha inicial y final.
    """
    artistas = copiarListaD(catalog['artists'],compareAnioD)
    ms.sort(artistas,ordAscArtiAnioD)
    pos = lt.isPresent(artistas,str(anio_inicial))
    pos_f = lt.isPresent(artistas,str(anio_final))
    l = int(pos_f)-int(pos)
    artists = lt.subList(artistas,pos,l+2)
    return artists

#------------------
# Requerimiento 3
#------------------

def artworksbyArtistD(catalog,nombre):
    """
    Retorna una lt con las obras de un artista por su nombre.
    """
    copia = copiarListaD(catalog['artists'],compareNamesD)
    artista = getElementbyparameterD(copia,nombre)
    ide = artista['ConstituentID']
    artist = mp.get(catalog['obbyArt'], ide)
    if artist:
        obras = me.getValue(artist)['obras']
    return obras

def listaMediosD(obras):
    """
    Retorna lista con representantes unicos para cada medio que se usa en una lista de obras 
    """
    first = lt.firstElement(obras)
    if first['Medium'] == '':
        first['Medium'] = "Ninguno"
    medios = lt.newList("ARRAY_LIST",cmpfunction=compareMediumD)
    lt.addLast(medios,first)        
    for obra in lt.iterator(obras):
        i = 0
        if obra['Medium'] == '':
            obra['Medium'] = "Ninguno"
        for medio in lt.iterator(medios):
            if (str(obra['Medium']) == str(medio['Medium'])):
                i += 1
        if (i == 0):
            lt.addLast(medios,obra)
    return medios
    
def artworksbyMediumD(obras):
    """
    Retorna un lt con las obras que usan la tecnica o medio mas recurrente en obras.
    """
    # contamos numero de veces que aparece cada medio y agregamos este numero a una lista (numeros)
    medios = listaMediosD(obras)
    numeros = lt.newList("ARRAY_LIST")
    for medio in lt.iterator(medios):
        i = 0
        for obra in lt.iterator(obras):
            if obra['Medium'] == '':
                obra['Medium'] = 'Ninguno'
            if (medio['Medium'] == obra['Medium']):
                i += 1
        lt.addLast(numeros,i)
    # ordenamos la lista y sacamos el numero mas grande
    ms.sort(numeros,cmpfunction=ordenAscendenteD)
    num = lt.lastElement(numeros)
    # hallamos el medio (medio) correspondiente a este numero mas grande (num)
    for medio in lt.iterator(medios):
        i = 0
        for obra in lt.iterator(obras):
            if obra['Medium'] == '':
                obra['Medium'] = "Ninguno"
            if (medio['Medium'] == obra['Medium']):
                i += 1
        if i == num:
            m = medio
            break
    # hacemos una lista (lista) con las obras que usan el medio hallado (medio)
    lista = lt.newList("ARRAY_LIST")
    if m is not None:
        for obra in lt.iterator(obras):
            if obra['Medium'] == '':
                obra['Medium'] = "Ninguno"
            if (obra['Medium'] ==  m['Medium']):
                lt.addLast(lista,obra)
        return lista

def contarMediosD(obras):
    """
    Cuenta la cantidad de medios que se usan en una lista de obras
    """
    medios = listaMediosD(obras)
    num = lt.size(medios)
    return num 

#------------------
# Requerimiento 5
#------------------

def artworksbyDepartmentD(catalog,department):
    """
    Dado un departamento retorna una lista con el total de sus obras, su costo total de transporte y su peso total.
    """
    dep = mp.get(catalog['department'],department)
    if dep:
        costo = me.getValue(dep)['costo']
        peso = me.getValue(dep)['peso']
        obras = me.getValue(dep)['obras']
    resultado = lt.newList("ARRAY_LIST")
    lt.addLast(resultado,lt.size(obras))
    lt.addLast(resultado,int(costo))
    lt.addLast(resultado,int(peso))
    return resultado

def costoTransporteD(obra):
    """
    Calcula el costo de transporte de una obra y agrega el dato a la obra correspondiente.
    """
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
    ms.sort(lista,cmpfunction=ordenAscendenteD)
    tamano = lt.lastElement(lista)
    # estipular el costo y agregarlo a los datos de la obra
    if tamano == 0:
        costo = 48
    else:
        costo = tamano*72
    obra['Transcost (USD)'] = costo
    return obra

def masCostosasD(catalog,department):
    """
    Retorna una lista con las 5 obras mas costosas de las obras del department.
    """
    dep = mp.get(catalog['depCosto'],department)
    if dep:
        obras = me.getValue(dep)['obras']
    ms.sort(obras,ordAscArtwCostD)
    costosas = lt.newList()
    i = 0
    while i < 5:
        o = lt.removeLast(obras)
        lt.addLast(costosas,o)
        i += 1
    return costosas

def masAntiguasD(catalog,department):
    """
    Retorna una lista con las 5 obras mas antiguas de las obras del department. 
    """
    dep = mp.get(catalog['depAntiguas'],department)
    if dep:
        obras = me.getValue(dep)['obras']
    ms.sort(obras,ordAscArtwDateD)
    antiguas = lt.newList()
    i = 0
    while i < 5:
        o = lt.removeFirst(obras)
        lt.addLast(antiguas,o)
        i += 1
    return antiguas