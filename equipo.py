
from funciones_auxiliares import anterior_indice, siguiente_indice

class EquipoPokemon:

    def __init__(self, nombre):
        '''Recibe un nombre e inicializa un nuevo equipo con los siguientes atributos
        Pre = nombre tiene que ser un string'''
        self.nombre = nombre
        self.diccionario_mov = {}
        self.pokemons = []
        self.pokemon_actual = None
        
    def obtener_pokemon_actual(self):
        '''Retorna el pokemon actual'''
        if len(self.pokemons) == 0:
            return None
        return self.pokemons[self.pokemon_actual]
    
    def obtener_nombre(self):
        '''Retorna el nombre del equipo'''
        return self.nombre
    
    def cantidad_pokemones(self):
        '''Retorna la cantidad de pokemones'''
        return len(self.pokemons)

    def eliminar_pokemon(self, pokemon):
        '''Recibe el pokemon a borrar y los elimina
        Pre = el pokemon tiene que estar en el equipo'''
        self.pokemons.remove(pokemon)
        self.diccionario_mov.pop(pokemon.obtener_nombre())
        if len(self.pokemons) == 1:
            self.pokemon_actual = 0
        
    def agregar_pokemon(self, pokemon, movimiento):
        '''Recibe un pokemon y un movimiento y los agrega al equipo
        Pre = Pokemon tiene que ser uno valido y el movimiento tiene que ser valido
        Si el pokemon supera el limite de la cantidad de cantidad o el pokemon ya esta no modifica nada
        sino agrega el pokemon con su movimiento'''
        if len(self.pokemons) > 5:
            return
        if pokemon in self.pokemons:
            return
        self.pokemons.append(pokemon)
        self.diccionario_mov[pokemon] = [movimiento]

    def agregar_movimiento(self, pokemon, movimiento):
        '''Recibe un pokemon y un movimiento
        Pre = el pokemon tiene que estar incluido en el equipo y el movimiento tiene que ser valido
        Si supera la cantidad de movimientos o el movimiento ya esta incluido, no modifica nada'''
        if len(self.diccionario_mov[pokemon]) + 1 > 4:
            return
        if movimiento in self.diccionario_mov[pokemon]:
            return
        self.diccionario_mov[pokemon].append(movimiento)

    def sacar_movimiento(self, pokemon, movimiento):
        '''Recibe un pokemon y un movimiento
        Pre = el pokemon tiene que estar incluido y el movimiento tambien
        Si el movimiento es el unico no modifica nada
        Sino lo elimina'''
        if len(self.diccionario_mov[pokemon]) - 1 == 0:
            return
        self.diccionario_mov[pokemon].remove(movimiento)

    def __str__(self):
        '''El string del equipo es su nombre'''
        return self.nombre
    
    def __repr__(self):
        '''La representacion del objeto equipo'''
        return f'Equipo_pk({self.nombre})'
    
    def avanzar_pokemon_actual(self):
        '''Avanza al siguiente pokemon teniendo en cuenta los casos bordes donde hay uno solo
        o no hay pokemones'''
        if len(self.pokemons) == 0:
            self.pokemon_actual = None
            return
        if self.pokemon_actual is None or len(self.pokemons) == 1:
            self.pokemon_actual = 0
            return
        self.pokemon_actual = siguiente_indice(self.pokemon_actual, len(self.pokemons))
        
    def retroceder_pokemon_actual(self):
        '''Retrocede al anterior pokemon teniendo en cuenta los casos bordes donde hay uno solo
        o no hay pokemones'''
        if len(self.pokemons) == 0:
            return
        if self.pokemon_actual is None:
            self.pokemon_actual = 0
            return
        self.pokemon_actual = anterior_indice(self.pokemon_actual, len(self.pokemons))

    def obtener_pokemons(self):
        '''Retorna una lista con los pokemones del equipo'''
        return self.pokemons
        
    def obtener_movimientos(self, pokemon):
        '''Recibe un pokemon y retorna una lista con sus movimientos actuales
        Pre = el pokemon debe estar en el equipo'''
        return self.diccionario_mov[pokemon]
    
    def esta_vacio(self):
        '''Retorna si el equipo esta vacio'''
        return len(self.pokemons) == 0

