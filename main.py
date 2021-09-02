import gamelib
from manejo_de_archivos import cargar_datos_equipos
from ventana_inicial import mostrar_ventana_inicial, evaluar_en_ventana_inicial
from ventana_batalla import mostrar_ventana_batalla, evaluar_en_ventana_batalla
import jugabilidad
import constantes as cte

'''Archivos a utilizar'''
ARCHIVO_EQUIPOS = 'assets/equipos.csv'
ARCHIVO_POKEMONS = 'assets/pokemons.csv'
ARCHIVO_MOVIMIENTOS = 'assets/detalle_movimientos.csv'
ARCHIVO_TABLA_TIPOS = 'assets/tabla_tipos.csv'

'''Defino constantes para las dimensiones de lo que vamos a dibujar'''
#Formato 
# RECTANGULO_X = (COORDENADA_X_INICIO, COORDENADA_X_FINAL)
# RECTANGULO_Y = (COORDENADA_Y_INICIO, COORDENADA_Y_FINAL)
DIMENSION_RECTANGULO_PRINCIPAL_X = (cte.ANCHO_VENTANA*0.0125, cte.ANCHO_VENTANA*0.9875)
DIMENSION_RECTANGULO_PRINCIPAL_Y = (cte.ALTO_VENTANA*0.02, cte.ALTO_VENTANA*0.98)

def mostrar_ventana(ventana_actual, jugador_uno, jugador_dos):
	"""Dibuja el rectangulo principal y dependiendo de la ventana_actual dibuja su representación"""
	x1, x2 = DIMENSION_RECTANGULO_PRINCIPAL_X
	y1, y2 = DIMENSION_RECTANGULO_PRINCIPAL_Y
	gamelib.draw_rectangle(x1, y1, x2, y2, fill = cte.COLOR_VIOLETA_OSCURO)

	if ventana_actual == cte.VENTANA_INICIAL:
		mostrar_ventana_inicial()

	if ventana_actual == cte.VENTANA_BATALLA:
		mostrar_ventana_batalla(jugador_uno, jugador_dos)
	
	return

def main():
	'''Abre la ventana y evalúa las acciones de los usuarios.'''

	#Abre la ventana
	gamelib.resize(cte.ANCHO_VENTANA, cte.ALTO_VENTANA)

	#Define el estado inicial
	ventana_actual = cte.VENTANA_INICIAL
	lista_equipos = cargar_datos_equipos(ARCHIVO_EQUIPOS, ARCHIVO_POKEMONS, ARCHIVO_MOVIMIENTOS, ARCHIVO_TABLA_TIPOS)
	jugadores_cargados = False
	jugador_uno, jugador_dos  = None, None
	while gamelib.is_alive():

		#Se dibuja la ventana y definimos el titulo
		gamelib.title(cte.TITULO)
		gamelib.icon(cte.ICONO)
		gamelib.draw_begin()
		mostrar_ventana(ventana_actual, jugador_uno, jugador_dos)
		gamelib.draw_end()

		#Se espera hasta que ocurra un evento
		ev = gamelib.wait()

		if not ev:
			#El usuario cerró la ventana
			break
		
		#Dependiendo de la ventana actual evalua de diferente forma la accion
		if ventana_actual == cte.VENTANA_INICIAL:
			ventana_actual = evaluar_en_ventana_inicial(ev)
			

		if ventana_actual == cte.VENTANA_BATALLA:
			if len(lista_equipos) == 0:
				gamelib.say(cte.MENSAJE_NO_HAY_EQUIPOS)
				break
			if not jugadores_cargados:
				jugador_uno = jugabilidad.crear_jugador(lista_equipos, cte.UNO)
				if not jugador_uno:
					ventana_actual = cte.VENTANA_INICIAL
					continue
				jugador_dos = jugabilidad.crear_jugador(lista_equipos, cte.DOS)
				if not jugador_dos:
					ventana_actual = cte.VENTANA_INICIAL
					continue
				jugadores_cargados = True
				continue
			
			batalla_esta_terminada = evaluar_en_ventana_batalla(ev, jugador_uno, jugador_dos)
			
			#Si la batalla termino, se cierra el programa	
			if batalla_esta_terminada:
				gamelib.say(cte.MENSAJE_BATALLA_TERMINADA)
				break

gamelib.init(main)
