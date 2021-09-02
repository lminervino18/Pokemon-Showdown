from equipo import EquipoPokemon
from pokemon import Pokemon
from movimiento import Movimiento
import csv

DELIMITADOR_CSV = ';'
DELIMITADOR_TIPOS = ','

def cargar_tabla_tipos(archivo_tabla_tipos):
    '''Recibe un archivo con las combinaciones de los tipos y el multiplicador de daño.
    Crear una diccionario con el indice correspondiente a cada tipo y una tabla de doble entrada con
    las correspondientes combinaciones'''

    diccionario = {}
    tabla = []
    with open(archivo_tabla_tipos) as f:
        csv_reader = csv.reader(f, delimiter = DELIMITADOR_CSV)
        encabezado = next(csv_reader)
        for indice, tipo in enumerate(encabezado[1:]):
            diccionario[tipo] = indice
        for linea in csv_reader:
            linea = list(map(lambda numero: float(numero), linea[1:]))
            tabla.append(linea)

    return tabla, diccionario

def cargar_equipos(archivo_equipos):
    '''Recibe un archivo csv con los equipos y carga en la lista todos los equipos como objeto 
    Equipo_pk con todos sus datos. Retorna la lista'''
    lista_equipos = []
    with open(archivo_equipos) as f:
            csv_reader = csv.reader(f, delimiter = DELIMITADOR_CSV)
            next(csv_reader)
            for equipo in csv_reader:
                if len(equipo) == 0:
                    continue
                equipo_nuevo = EquipoPokemon(equipo[0])
                for pokemon in equipo[1:]:
                    pokemon = list(pokemon.split(DELIMITADOR_TIPOS))
                    nombre_pokemon = pokemon[0]
                    equipo_nuevo.agregar_pokemon(nombre_pokemon, pokemon[1])
                    for movimiento in pokemon[2:]:
                        equipo_nuevo.agregar_movimiento(nombre_pokemon, movimiento)
                lista_equipos.append(equipo_nuevo)
    return lista_equipos

def cargar_pokemons(archivo_pokemons, lista_equipos, archivo_tabla_tipos):
    '''Recibe un archivo con los datos de los pokemons, un archivo con las combinaciones de tipos y una lista
    con los equipos. Lee el archiv pokemons y verifica si ese pokemon pertence a algun equipo de la lista
    pasada por parametro. Si esta en alguno, reemplaza ese string por un objet Pokemon con todos sus datos'''

    tabla_tipos, diccionario = cargar_tabla_tipos(archivo_tabla_tipos)
    with open(archivo_pokemons) as fpk:
            fpk_csv = csv.reader(fpk, delimiter = DELIMITADOR_CSV)
            next(fpk_csv)
            for _, img, nom, tip, hp, atk, defs, spa, spd, spe in fpk_csv:
                for equipo in lista_equipos:
                    lista_pokemons = equipo.obtener_pokemons()
                    if nom in lista_pokemons:
                        posicion = lista_pokemons.index(nom)
                        pokemon_nuevo = Pokemon(img, nom, tip.split(','), hp, atk, defs, spa, spd, spe, tabla_tipos, diccionario)
                        movs = equipo.obtener_movimientos(nom)
                        pokemon_nuevo.agregar_movimientos(movs)
                        lista_pokemons[posicion] = pokemon_nuevo


def cargar_movimientos(lista_equipos, archivo_movimientos):
    '''Recibe un archivo con los datos de los movimientos y una lista
    con los equipos. Lee el archiv movimientos y verifica si ese movimiento pertence a algun pokemon de algun equipo
    que se encuentre en la lista pasada por parametro.
    Si esta en alguno, reemplaza ese string por un objeto Movimiento con todos sus datos'''
    with open(archivo_movimientos) as mov:
        mov_csv = csv.reader(mov, delimiter = DELIMITADOR_TIPOS)
        next(mov_csv)
        for nombre_mov, categoria, objetivo, pp, poder, tipo, stats in mov_csv:
            for equipo in lista_equipos:
                pokemons = equipo.obtener_pokemons()
                for pokemon in pokemons:
                    movimientos = pokemon.obtener_movimientos() 
                    for movimiento in movimientos:
                        if nombre_mov == movimiento:
                            posicion = movimientos.index(movimiento)
                            if stats == '':
                                stats_final = None
                            else:
                                stats_final = stats.split(DELIMITADOR_CSV)
                            movimientos[posicion] = Movimiento(nombre_mov, categoria, objetivo, pp, poder, tipo, stats_final)


def cargar_datos_equipos(archivo_equipos, archivo_pokemons, archivo_movimientos, archivo_tabla_tipos):
    '''Recibe el archivo origen con la informacion de los equipos guardados, un archivo con la informacion
    de los pokemons, un archivo con la infromacion de los movimientos y un archivo con la informacon de las combinaciones
    de multiplicadores de daño de los tipos.
    Despues de crear una lista con los objetos equipos, las recorre y reemplaza los strings(e los pokemones y movimientos) con
    objetos con sus respectivas caracteristicas.
    Retorna una lista con los equipos. Si algun archivo no existe o hay algun error retorna una lista de equipos vacia  
    '''
    try:
        lista_equipos = cargar_equipos(archivo_equipos)
        cargar_pokemons(archivo_pokemons, lista_equipos, archivo_tabla_tipos)
        cargar_movimientos(lista_equipos, archivo_movimientos) 
        
        return lista_equipos
    except :
        return [] 
