from random import choice
from constantes import OBJETIVOS, TIPOS_DE_ATAQUES, STATS_BOOSTERS
from funciones_auxiliares import redondear_numero

class Pokemon:

    def __init__(self,imagen,nombre, tipo, hp, atk, defs, spa, spd, spe, tabla_tipos, diccionario_tipos):
        '''Recibe el nombre de un pokemon con sus respectivas características, e inicializa
        la clase pokemon, siendo sus atributos los parametros que recibe.
        Pre: nombre y tipo deben ser string, y el resto deben ser enteros.'''
        

        self.imagen = imagen
        self.nombre = nombre
        self.tipo = tipo
        self.hp = int(hp) + 110
        self.hp_max_original = int(hp) + 110
        self.atk = int(atk)
        self.atk_original = int(atk)
        self.defs = int(defs)
        self.defs_original = int(defs)
        self.spa = int(spa)
        self.spd = int(spd)
        self.spe = int(spe)
        self.spe_original = int(spe)
        self.movimientos = []
        self.vivo = True
        self.tabla_tipos = tabla_tipos
        self.diccionario_tipos = diccionario_tipos

    def obtener_imagen(self):
        '''Retorna la imagen del pokemon'''
        return self.imagen

    def obtener_nombre(self):
        '''Retorna el nombre del pokemon'''
        return self.nombre

    def obtener_spe(self):
        '''Retorna la velocidad del pokemon'''
        return self.spe
    
    def obtener_hp(self):
        '''Retorna la vida actual del pokemon'''
        return self.hp
        
    def obtener_hp_max_original(self):
        '''Retorna la vida original del pokemon'''
        return self.hp_max_original
    
    def obtener_movimientos(self):
        '''Retorna una lista con los movimientos'''
        return self.movimientos

    def obtener_tipo(self):
        '''Retorna el tipo del pokemon'''
        return self.tipo

    def reiniciar_stats(self):
        '''Reinicia sus stats a los valores originales'''
        self.atk = self.atk_original
        self.spe = self.spe_original
        self.defs = self.defs_original

    def recibir_ataque(self, danio):
        '''Recibe el daño (final) inflijido en el pokemon. Le resta a su atributo hp
        el daño, y si el hp del pokemon es igual o mayor a cero, se cambia el valor a su
        atributo esta_vivo.
        Pre: danio debe ser un entero.'''
        self.hp -= danio
        if self.hp <= 0:
            self.vivo = False

    def realizar_booster(self, movimiento, defensor):
        '''Recibe el movimiento (puede provenir del mismo pokemon, o de otro)
        y el pokemon rival. En caso de que el objetivo del movimiento sea el propio
        pokemon, se aumentara sus respectivos stats, pero si el objetivo es el
        pokemon rival le reducirá sus stats.
        Pre: movimiento debe provenir de la clase Movimiento y defensor de la clase Pokemon.'''
        obj_self, obj_normal, obj_allad = OBJETIVOS
        atk, defs, spe, spa, spd = STATS_BOOSTERS
        if movimiento.objetivo in (obj_allad, obj_normal):
            for stat in movimiento.stats:
                if stat == spe:
                    defensor.spe *= 0.5
                if stat == atk:
                    defensor.atk *= 0.5
                if stat == defs:
                    defensor.defs *= 0.5
                if stat == spa:
                    defensor.spa *= 0.5
                if stat == spd:
                    defensor.spd *= 0.5
            return defensor
                
        if movimiento.objetivo == obj_self:
            for stat in movimiento.stats:
                if stat == spe:
                    self.spe *= 2
                if stat == atk:
                    self.atk *= 2
                if stat == defs:
                    self.defs *= 2
                if stat == spa:
                    defensor.spa *= 2
                if stat == spd:
                    defensor.spd *= 2
            return self

    def __repr__(self):
        '''La representacion del pokemon es su nombre'''
        return self.nombre
    
    def __str__(self):
        '''El string del pokemon es su nombre con sus movimientos entre parentesis'''
        string = ', '.join(map(lambda mov: str(mov) ,self.movimientos))
        return f'{self.nombre} ({string})'

    def realizar_ataque(self, movimiento, defensor):
        '''Recibe un movimiento propio y el pokemon al que ataca. Dependiendo
        de la categoría del ataque se calcula el daño base, luego se calcula el
        daño final y se usa el metodo recibir_ataque en el defensor
        Pre: movimiento debe provenir de la clase Movimiento y defensor de la clase Pokemon.'''
        atk_phy, atk_special = TIPOS_DE_ATAQUES
        if movimiento.categoria == atk_phy:
            danio_base = 15*movimiento.poder*(self.atk/defensor.defs)/50
        if movimiento.categoria == atk_special:
            danio_base = 15*movimiento.poder*(self.spa/defensor.spd)/50

        danio_final = calcular_modificadores_ataque(danio_base, self, defensor, movimiento)
        defensor.recibir_ataque(danio_final)
        return danio_final
        
    def sanacion(self):
        '''Le proporciona el 50% de su vida maxima al pokemon. Si esto supera
        su vida maxima original, self.hp queda con el valor de su vida maxima original.'''
        suma_inicial = self.hp + self.hp_max_original * 0.5
        self.hp = int(suma_inicial - (suma_inicial % self.hp_max_original) * (suma_inicial // self.hp_max_original))
        
    def esta_vivo(self):
        '''Devuelve un valor booleano en caso de que el pokemon este vivo o no.'''
        return self.vivo

    def agregar_movimientos(self, lista_movimientos):
        '''Recibe una lista con movimientos y los agrega'''
        self.movimientos.extend(lista_movimientos)

    def eliminar_movimiento(self, movimiento):
        '''Recibe un movimiento y si este esta en el pokemon, lo elimina'''
        if movimiento in self.movimientos:
            self.movimientos.remove(movimiento)

    def tiene_movimientos(self):
        '''Retorna si el pokemon tiene algun movimiento'''
        return self.movimientos != []

def calcular_modificadores_ataque(danio_base, atacante, defensor, movimiento):
    '''Recibe un danio base, el atacante, el defensor y un movimiento.
    Calcula el daño final con respecto a los tipos del atacante, defensor y del movimiento, ademas 
    de una variacion aleatoria'''
    if atacante.tipo == movimiento.obtener_tipo():
        danio_base *= 1.5
    modificador = 0
    for i in range(len(defensor.obtener_tipo())):
        columna = defensor.diccionario_tipos[defensor.obtener_tipo()[i]]
        fila = atacante.diccionario_tipos[movimiento.obtener_tipo()]
        modificador += defensor.tabla_tipos[columna][fila]
    danio_base *= modificador
    porcentaje_aleatorio = choice(range(80, 101))
    danio_final = danio_base*porcentaje_aleatorio/100
    
    return redondear_numero(danio_final)

    