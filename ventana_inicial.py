import gamelib
import constantes as cte
#FORMATO
#DIMENSION_IMAGEN = (POSICION_X, POSICION_Y)
#DIMENSION_TEXTO = (POSICION_X, POSICION_Y, TAMAÑO LETRA)

DIMENSION_EMPEZAR_BATALLA = (cte.ANCHO_VENTANA*0.5, cte.ALTO_VENTANA*0.8, int(cte.ALTO_VENTANA*0.03))
DIMENSION_IMAGEN_TITULO = (cte.ANCHO_VENTANA*0.2, cte.ALTO_VENTANA*0.32)
IMAGEN_TITULO = 'assets/titulo_pok.gif'

def evaluar_en_ventana_inicial(ev):
	'''Evalua la accion del usuario en la ventana inicial y retorna la ventana actual'''

	if ev.key == cte.COMENZAR_BATALLA:
		return cte.VENTANA_BATALLA

	return cte.VENTANA_INICIAL

def mostrar_ventana_inicial():
	'''Dibuja la ventana inicial'''
	x, y = DIMENSION_IMAGEN_TITULO
	gamelib.draw_image(IMAGEN_TITULO, x, y)
	x, y, tamanio = DIMENSION_EMPEZAR_BATALLA
	gamelib.draw_text(cte.TEXTO_EMPEZAR_BATALLA, x, y, font = cte.FUENTE, size = tamanio, italic = True, fill = cte.COLOR_NEGRO)