import gamelib
from entrenador_pokemon import EntrenadorPokemon
from funciones_auxiliares import elegir_elemento_lista
from random import choice
import constantes as cte

TUPLA_OPCIONES = (cte.OPCION_REALIZAR_MOVIMIENTO, cte.OPCION_CAMBIAR_POKEMON)

def elegir_quien_va_primero(jug_uno, jug_dos):
    '''Recibe dos jugadores actuales y de acuerdo a la velocidad del pokemon actual
    de su equipo decide quien va primero y quien va segundo.
     Retora esos mismo jugadores en el orden correspondiente'''

    pok_uno = jug_uno.obtener_pokemon_actual()
    pok_dos = jug_dos.obtener_pokemon_actual()
    if pok_uno.obtener_spe() > pok_dos.obtener_spe():
        primero, segundo = jug_uno, jug_dos
    elif pok_uno.obtener_spe() < pok_dos.obtener_spe():
        primero, segundo = jug_dos, jug_uno
    else:
        lista = [jug_uno, jug_dos]
        primero = lista.pop(lista.index(choice(lista)))
        segundo = lista[0]

    return primero, segundo

def crear_jugador(lista_equipos, numero_de_jugador):
    '''
    Recibe la lista de equipos. Le pregunta al usuario su nombre, el equipo que quiere utilizar
    y el pokemon para iniciar. Si en algun momento se recibe un None, retora None. Caso contrario
    retorna el objeto jugador correspondiente con todos los datos cargados'''
    nombre = gamelib.input(cte.STRING_ELEGIR_NOMBRE + numero_de_jugador)
    if not nombre:
        return None

    equipo = elegir_elemento_lista(lista_equipos, nombre + ':\n'+ cte.STRING_ELEGIR_EQUIPO)
    if not equipo:
        return None
    lista_equipos.remove(equipo)

    jugador = EntrenadorPokemon(nombre, equipo, cte.IMAGEN_HOMBRE)
    elegir_pokemon_actual(jugador)
    if not jugador.obtener_pokemon_actual():
        lista_equipos.append(equipo)
        return None
    return jugador


def realizar_movimiento(atacante, defensor, movimiento_a_jugar):
    '''Recibe al jugador atacante, al jugador defensor y el movimiento a jugar.
    Analiza las caracteristicas del movimiento y actua en consecuencia. Si el movimiento es
    de ataque muestra el daño recibido por el defensor. Si el movimiento es un booster muestra que pokemon 
    y que stat fue modificada'''

    pokemon_atacante = atacante.obtener_pokemon_actual()
    pokemon_defensor = defensor.obtener_pokemon_actual()
    movimiento_a_jugar.restar_pp()
    if not movimiento_a_jugar.le_quedan_usos():
        pokemon_atacante.eliminar_movimiento(movimiento_a_jugar)

    if movimiento_a_jugar.obtener_categoria() in cte.TIPOS_DE_ATAQUES:
        danio_final = pokemon_atacante.realizar_ataque(movimiento_a_jugar, pokemon_defensor)
        gamelib.say(f'{defensor}: ¡{pokemon_defensor.obtener_nombre()} recibio {danio_final} de daño!')
        return

    if not movimiento_a_jugar.obtener_stats():
        pokemon_atacante.sanacion()
        gamelib.say(f'{atacante}: el pokemon {pokemon_atacante.obtener_nombre()} se sanó')
        return
    
    pokemon_afectado = pokemon_atacante.realizar_booster(movimiento_a_jugar, pokemon_defensor)
    string_stats = ''

    for stat in movimiento_a_jugar.obtener_stats():
        string_stats += f'{cte.DICCIONARIO_STATS[stat]}\n'
    gamelib.say(f'{atacante} realizo un booster a los siguientes stats:\n\n{string_stats}\ndel Pokemon: {pokemon_afectado.obtener_nombre()}')

    
    
def elegir_accion(jugador):
    '''Le pide al usuario que elija entre realizar movimiento o cambiar pokemon. No lo deja salir 
    hasta que elija una opcion. En caso de que seleccione realizar movimiento le pide que seleccione
    uno de los disponibles y retora el movimiento elegido. En caso de que elija cambiar pokemon retorna None'''

    while True:
        opcion = elegir_elemento_lista(TUPLA_OPCIONES, f'{jugador.nombre}: {cte.STRING_ELEGIR_OPCION}')
        if opcion:
            break
    if opcion == cte.OPCION_REALIZAR_MOVIMIENTO:
        lista_movs = jugador.obtener_pokemon_actual().obtener_movimientos()
        while True:  
            movimiento_a_jugar = elegir_elemento_lista(lista_movs, f'{jugador.nombre}: {cte.STRING_ELEGIR_MOV}')
            if not movimiento_a_jugar:
                continue
            if not type(movimiento_a_jugar) == str:
                return movimiento_a_jugar
            gamelib.say('Tu movimiento no hizo efecto, procura no elegirlo la proxima vez')
    return None



def jugar_turno(jugador_uno, jugador_dos):
    '''Recibe los dos jugadores y se encarga de la mecanica del juego. LLama a la funcion elegir_quien_va_primero
    para decidir el turno de cada jugador en la batalla; llama a la  funcion elegir_accion. 
    En caso de que eligio realizar un movimiento, se hacen los efectos corresondientes.
    En caso de que elija cambiar pokemon se llama a la funcion elegir_pokemon_actual.
    Luego analiza el estado de los pokemons actuales de ambos jugadores, y si deben rotarlos, llama a la
    funcion cambio_de_pokemon. Retorna un booleano, True si la batalla termino, False si se mantiene.'''

    primer_jugador, segundo_jugador = elegir_quien_va_primero(jugador_uno, jugador_dos)
    primera_accion = elegir_accion(primer_jugador)
    segunda_accion = elegir_accion(segundo_jugador)
    
    if primera_accion:
        realizar_movimiento(primer_jugador, segundo_jugador, primera_accion)
    else:
        elegir_pokemon_actual(primer_jugador)
    
    pokemon_del_segundo = segundo_jugador.obtener_pokemon_actual()
    if not pokemon_del_segundo.esta_vivo():
        if cambio_de_pokemon_fallecido(str(primer_jugador), segundo_jugador):
            return True
        return False
    
    if segunda_accion:
       realizar_movimiento(segundo_jugador, primer_jugador, segunda_accion)
    else:
        elegir_pokemon_actual(segundo_jugador)
    
    pokemon_del_primero = primer_jugador.obtener_pokemon_actual()
    if not pokemon_del_primero.esta_vivo():
        if cambio_de_pokemon_fallecido(str(segundo_jugador), primer_jugador):
            return True

    if not pokemon_del_primero.tiene_movimientos():
        if cambio_de_pokemon_fallecido(str(segundo_jugador), primer_jugador):
            return True
    if not pokemon_del_segundo.tiene_movimientos():
        if cambio_de_pokemon_fallecido(str(primer_jugador), segundo_jugador):
            return True

    return False
        
def cambio_de_pokemon_fallecido(nombre_jugador_rival, jugador_actual):
    '''Recibe el nombre del jugador rival y el jugador actual. 
    Elimina el pokemon actual y le pide al usuario que elija entre los pokemones restantes
    Si el jugador se queda sin pokemones retorna True, caso contrario el jugador elige un nuevo pokemon
    y retorna False'''

    pokemon_del_jugador_actual = jugador_actual.obtener_pokemon_actual()
    jugador_actual.obtener_equipo().eliminar_pokemon(pokemon_del_jugador_actual)
    if not pokemon_del_jugador_actual.tiene_movimientos():
        gamelib.say(f'{jugador_actual}: \n\n¡Necesita descansar!\n\nLuego de este ultimo movimiento, tu pokemon ya no puede seguir peleando.\nMejor elige otro.')
    else:
        gamelib.say(f'¡El pokemon: {pokemon_del_jugador_actual.obtener_nombre()} de {jugador_actual} ha muerto!\n¡Hagamos un minuto de silencio!\n¡Tienes que cambiar tu pokemon!')
    if len(jugador_actual.obtener_equipo().obtener_pokemons()) == 0:
        gamelib.say(f'Al jugador {jugador_actual} no le quedan pokemons\n¡{nombre_jugador_rival} has ganado!')
        return True
    elegir_pokemon_actual(jugador_actual)
    return False

    
def elegir_pokemon_actual(jugador):
    '''Recibe un jugador. En caso de que ya haya elegido un pokemon anteriormente se le reinician las stats al
    pokemon actual. Luego el usuario selecciona el nuevo pokemon a utlizar (Puede volver a seleccionar el'''
    if jugador.obtener_pokemon_actual():
        jugador.obtener_pokemon_actual().reiniciar_stats()

    while True:
        pokemon_actual = elegir_elemento_lista(jugador.obtener_equipo().obtener_pokemons(), f'{jugador}:\n\n' + cte.STRING_ELEGIR_POK)
        if pokemon_actual:
            jugador.cambiar_pokemon_actual(pokemon_actual)
            break

