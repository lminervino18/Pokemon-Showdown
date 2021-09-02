class Movimiento():

    def __init__(self, nombre, categoria, objetivo, pp, poder, tipo, stats):
        '''Inicializa la instancia del objeto con los atributos recibidos por parametro'''
        '''Pre: pp y poder tienen que ser digitos(string o un numero)
        Pre: Stats tiene que ser una lista de strings'''
        self.nombre = nombre
        self.categoria = categoria
        self.objetivo = objetivo
        self.pp = int(pp)
        self.poder = int(poder)
        self.tipo = tipo
        self.stats = stats
        
    def __str__(self):
        '''Retorna el nombre del pokemon'''
        return self.nombre

    def restar_pp(self):
        '''Le resta un pp al pokemon'''
        if self.pp == 0:
            return
        self.pp -= 1

    def le_quedan_usos(self):
        '''Restorna si al movimiento le quedan usos(pp)'''
        return self.pp != 0

    def obtener_categoria(self):
        '''Retorna la categoria del movimiento'''
        return self.categoria

    def obtener_objetivo(self):
        '''Retorna el objetivo del movimiento'''
        return self.objetivo

    def obtener_poder(self):
        '''Retorna el poder del movimiento'''
        return self.poder

    def obtener_tipo(self):
        '''Retorna el tipo del movimiento'''
        return self.tipo

    def obtener_stats(self):
        '''Retorna la lista con sus stats'''
        return self.stats