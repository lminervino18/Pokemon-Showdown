from funciones_auxiliares import verificador_de_accion
import jugabilidad
import gamelib
import constantes as cte

IMAGEN_POKEBALL = "assets/pokeball.gif"
IMAGEN_TITULO_BATALLA = 'assets/titulo_batalla.gif'
#FORMATO
#DIMENSION_IMAGEN = (POSICION_X, POSICION_Y)
#DIMENSION_TEXTO = (POSICION_X, POSICION_Y, TAMAÑO LETRA)
#DISTANCIA = (POSICION_X, POSICION_Y)
DIMENSION_IMAGEN_JUGADOR = (cte.ANCHO_VENTANA*0.07, cte.ALTO_VENTANA*0.848)
DIMENSION_NOMBRE_JUGADOR = (cte.ANCHO_VENTANA*0.12, cte.ALTO_VENTANA*0.768, int(cte.ANCHO_VENTANA*0.018))
DIMENSION_POKEBALLS = (cte.ANCHO_VENTANA*0.09, cte.ALTO_VENTANA*0.808)
DIMENSION_IMAGEN_TITULO = (cte.ANCHO_VENTANA*0.1, cte.ALTO_VENTANA*0.16)
DIMENSION_HP = (cte.ANCHO_VENTANA*0.25, cte.ALTO_VENTANA*0.736, int(cte.ANCHO_VENTANA*0.1))
DIMENSION_IMAGEN_POK_ACTUAL = (cte.ANCHO_VENTANA*0.25, cte.ALTO_VENTANA*0.768)
DISTANCIA_ENTRE_JUGADORES = (cte.ANCHO_VENTANA*0.725, -cte.ALTO_VENTANA*0.64)
DISTANCIA_ENTRE_POKEMONES = (cte.ANCHO_VENTANA*0.350, -cte.ALTO_VENTANA*0.64)
DIMENSION_TEXTO_AVANZAR_TURNO = (cte.ANCHO_VENTANA*0.700,cte.ALTO_VENTANA*0.8, int(cte.ANCHO_VENTANA*0.02))

def mostrar_ventana_batalla(jugador_uno, jugador_dos):

	'''Recibe un jugador atacante y un jugador defensor, y dibuja la ventana batalla'''

	x, y = DIMENSION_IMAGEN_TITULO
	gamelib.draw_image(IMAGEN_TITULO_BATALLA, x, y)
	x, y ,tamanio = DIMENSION_TEXTO_AVANZAR_TURNO
	gamelib.draw_text(cte.TEXTO_AVANZAR_TURNO, x, y, font = cte.FUENTE, size = tamanio, bold = True, fill = cte.COLOR_GRIS)
	dx, dy = DISTANCIA_ENTRE_JUGADORES
	dpx, dpy = DISTANCIA_ENTRE_POKEMONES
	x, y, tamanio = DIMENSION_NOMBRE_JUGADOR
	gamelib.draw_text(jugador_uno, x, y, size=tamanio, bold=True, fill=cte.COLOR_GRIS)
	gamelib.draw_text(jugador_dos, x + dx, y + dy, size=tamanio, bold=True, fill=cte.COLOR_GRIS)
	
	x, y = DIMENSION_IMAGEN_JUGADOR
	gamelib.draw_image(jugador_uno.obtener_imagen(), x, y)
	gamelib.draw_image(jugador_dos.obtener_imagen(), x + dx, y + dy)
	
	x, y = DIMENSION_POKEBALLS
	mostrar_pokeballs(jugador_uno.obtener_equipo(), x, y)
	mostrar_pokeballs(jugador_dos.obtener_equipo(), x + dx, y + dy)
	x, y , ancho = DIMENSION_HP 
	mostrar_hp(jugador_uno.obtener_pokemon_actual(), x, y, ancho)
	mostrar_hp(jugador_dos.obtener_pokemon_actual(), x + dpx, y + dpy, ancho)

	x, y = DIMENSION_IMAGEN_POK_ACTUAL	
	gamelib.draw_image(jugador_uno.obtener_pokemon_actual().obtener_imagen(), x, y)
	gamelib.draw_image(jugador_dos.obtener_pokemon_actual().obtener_imagen(), x + dpx, y + dpy)

def mostrar_hp(poke, x, y, ancho):
	'''Recibe un pokemon, el largo de la barra de hp y unas coordenadas x e y,
	para dibujar la barra de vida actual de cada pokemon siendo utilizado'''
	porcentaje_restante = poke.obtener_hp() / poke.obtener_hp_max_original()
	if porcentaje_restante > 0.7:
		color = cte.COLOR_VERDE
	elif 0.2 < porcentaje_restante <= 0.7:
		color = cte.COLOR_AMARILLO
	else:
		color = cte.COLOR_ROJO
	gamelib.draw_text(f"Hp: {poke.hp}", x, y-15, size=15, bold=True, fill=cte.COLOR_NEGRO)
	gamelib.draw_rectangle(x, y, x + ancho, y + 10, fill='gray')
	gamelib.draw_rectangle(x, y, x + (ancho * porcentaje_restante), y + 10, fill=color)

def mostrar_pokeballs(equipo, x_inicial, y):
	'''Recibe un equipo y unas coordenadas x e y, y dibuja las pokeballs de los pokemons
	vivos en la partida'''
	for i, poke in enumerate(equipo.obtener_pokemons()):
		if poke.esta_vivo():
			gamelib.draw_image(IMAGEN_POKEBALL, x_inicial + i * 20, y)

def evaluar_en_ventana_batalla(ev, jugador_uno, jugador_dos):
	'''Evalua la accion del usuario en la ventana de los jugadores y sus equipos.
	   Retorna la ventana actual y el equipo elegido.'''
	batalla_esta_terminada = False
	
	if ev.key == 'space':
		batalla_esta_terminada = jugabilidad.jugar_turno(jugador_uno, jugador_dos)
	if ev.key == 'Escape':
		if verificador_de_accion(cte.MENSAJE_SALIR):
			batalla_esta_terminada = True

	return batalla_esta_terminada