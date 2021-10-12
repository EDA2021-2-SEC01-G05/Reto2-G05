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

"""
El controlador se encarga de mediar entre la vista y el modelo.

"""
#======================================
# Inicialización del Catálogo de obras
#======================================

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    t = "SINGLE_LINKED"
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
    
def loadArtworks(catalog):
    """
    Carga las obras del archivo.
    """
    booksfile = cf.data_dir + 'MoMA/Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)   

def loadArtists(catalog):
    """
    Carga los artistas.
    """
    booksfile = cf.data_dir + 'MoMA/Artists-utf8-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

#=================
# requerimientos
#=================

#-----------------
# requerimiento 1
#-----------------

def artistsbyAnio(catalog,anio_inicial,anio_final):
    """
    """
    return model.artistsbyAnio(catalog,anio_inicial,anio_final)

def firstThreeD(catalog):
    """
    """
    return model.firstThreeD(catalog)

def lastThreeD(catalog):
    """
    """
    return model.lastThreeD(catalog)

#--------
# lab 5
#--------

def obrasAntiguas(catalog,n,medio):
    """
    """
    return model.obrasAntiguas(catalog,n,medio)