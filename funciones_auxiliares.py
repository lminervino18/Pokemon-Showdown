import gamelib

def verificador_de_accion(cadena):
	'''Recibe una cadena, se la muestra al usuario, le pide una respuesta
	y retorna si esa respuesta es 's' '''
	respuesta = gamelib.input(cadena)
	return respuesta == 's'

def siguiente_indice(actual, cantidad):
	'''Recibe un indice y la longitud de una lista y avanza al siguiente
	teniendo en cuenta que si llego al final, vuelve al principio'''
	return (actual + 1) % cantidad

def anterior_indice(actual, cantidad):
	'''Recibe un indice y la longitud de una lista y retrocede al anterior
	teniendo en cuenta que si llego al principio, va al final'''
	if actual == 0:
		return cantidad - 1
	return actual - 1

#Pokedex
def buscar_pokemon(cadena, valor_por_defecto, lista_nombres_pokemones):
	'''Recibe una cadena que igreso el usuario, un valor por defecto y una lista con los nombres
	de los pokemons, si la cadena es un numero retorna el indice al que hace referencia y si la cadena
	es el nombre del Pokemon retorna el indice correspondiente. Si lo que el usuario ingreso es
	incorrecto retorna el valor por defecto '''
	cantidad_pokemones = len(lista_nombres_pokemones)
	if not cadena:
		return valor_por_defecto
	if cadena.isdigit() and int(cadena) in range(cantidad_pokemones):
		return int(cadena) - 1
	if cadena in lista_nombres_pokemones:
		return lista_nombres_pokemones.index(cadena)
	return valor_por_defecto

def elegir_elemento_lista(lista, string):
	'''Recibe una lista, una cadena
	, y arma un mensaje listando los elementos de la lista, que aparecerá en un
	cuadro de texto en la ventana'''
	string_opciones = ''
	for indice, elemento in enumerate(lista):
		string += f'{indice+1}: {elemento}\n'
	mensaje = string + '\n' f'Ingrese el numero de la opcion correcta\n{string_opciones}' 
	while True:
		numero_elegido = gamelib.input(mensaje)
		if not numero_elegido:
			return
		if numero_elegido.isnumeric() and 0 <= int(numero_elegido) - 1 < len(lista):
			break
		gamelib.say('Lo que ingresaste no es correcto, vuelve a intentarlo')
	
	return lista[int(numero_elegido)-1]

def redondear_numero(numero):
	'''Recibe un numero y lo redondea. Si su parte decimal es mayor o igual
	a 0.50 lo redondea al siguiente numero, caso contrario al anterior'''
	if (numero - int(numero)) >= 0.50:
		return int(numero) + 1
	return int(numero)


