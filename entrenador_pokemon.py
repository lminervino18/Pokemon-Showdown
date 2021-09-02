class EntrenadorPokemon:
    
    def __init__(self, nombre, equipo, imagen):
        '''Al crear un entrenador se recibe por parametro su nombre, su equipo y su imagen'''
        '''Pre: El equipo tiene que ser un objeto Equipo_pk'''
        self.nombre = nombre
        self.equipo = equipo
        self.pokemon_actual = None
        self.imagen = imagen
    
    def obtener_equipo(self):
        '''Retora su equipo'''
        return self.equipo
        
    def cambiar_pokemon_actual(self, pokemon):
        '''Recibe un pokemon y lo establece como su pokemon actual
        Pre: el pokemon tiene que estar incluido en el equipo'''
        if pokemon not in self.equipo.obtener_pokemons():
            return
        self.pokemon_actual = pokemon
    
    def obtener_pokemon_actual(self):
        '''Retorna su pokemon actual '''
        return self.pokemon_actual

    def obtener_imagen(self):
        '''Retorna su imagen'''
        return self.imagen
    
    def __str__(self):
        '''Retorna su nombre'''
        return self.nombre