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
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.khishdih

"""
#======================================
# Inicialización del Catálogo de obras
#======================================

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    t = "ARRAY_LIST"
    catalog = model.newCatalog(t)
    return catalog

#==================================
# Funciones para la carga de datos
#==================================

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)
    loadNationality(catalog)
    
def loadArtworks(catalog):
    """
    Carga las obras del archivo.
    """
    booksfile = cf.data_dir + 'MoMA/Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)   

def loadArtists(catalog):
    """
    Carga los artistas.
    """
    booksfile = cf.data_dir + 'MoMA/Artists-utf8-large.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

def loadNationality(catalog):
    """
    Carga las nacionalidades.
    """
    model.loadNationality(catalog)

#=================
# requerimientos
#=================

def obrasAntiguas(catalog,n,medio):
    """
    """
    return model.obrasAntiguas(catalog,n,medio)

def topNacionality(catalog):
    """
    Organiza el Top de Nacionalidades con más obras y tambien organiza 
    alfabeticamente las obras de una nacionalidad.
    """
    return model.topNacionality(catalog)

def organizeArtworkbyDate(catalog, startDate, finishDate):
    """
    Organiza y retorna las obras que esten en un rango de 
    una fecha inicial y final.
    """
    return model.organizeArtworkbyDate(catalog, startDate, finishDate)

def countPurchase(artworks):
    """
    Cuenta la cantidad de obras que fueron adquiridas por compra.
    """
    return model.countPurchase(artworks)

def getArtworksartists(catalog, codes):
    """
    """
    return model.getArtworksartists(catalog, codes)

def firstThreeD(lista):
    """
    Retorna una lista con los tres primeros elementos de una lista.
    """
    return model.firstThreeD(lista)
    
def lastThreeD(lista):
    """
    Retorna una lista con los 3 ultimos elementos de una lista.
    """
    return model.lastThreeD(lista)

#-----------------
# Requerimiento 1
#-----------------

def artistsbyAnioD(catalog,anio_inicial,anio_final):
    """
    """
    return model.artistsbyAnioD(catalog,anio_inicial,anio_final)

#-----------------
# Requerimiento 3
#-----------------

def artworksbyArtistD(catalog,nombre):
    """
    """
    return model.artworksbyArtistD(catalog,nombre)

def artworksbyMediumD(obras):
    """
    """
    return model.artworksbyMediumD(obras)

def contarMediosD(obras):
    """
    """
    return model.contarMediosD(obras)

def medioMaxD(obras):
    """
    """
    medio = lt.firstElement(obras)
    return medio['Medium']

#------------------
# Requerimiento 5
#------------------

def artworksbyDepartmentD(catalog,department):
    """
    """
    return model.artworksbyDepartmentD(catalog,department)

def masCostosasD(catalog,department):
    """
    """
    return model.masCostosasD(catalog,department)

def masAntiguasD(catalog,department):
    """
    """
    return model.masAntiguasD(catalog,department)
