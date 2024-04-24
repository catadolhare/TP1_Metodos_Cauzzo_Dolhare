# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

class ListaEnlazada:
    def __init__( self ):
        self.raiz = None
        self.longitud = 0
        
        self.current = self.Nodo(None, self.raiz)

    def insertarFrente( self, valor ):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)    
    
        nuevoNodo = self.Nodo( valor, self.raiz )
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo( self, valor, nodoAnterior ):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo( valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push( self, valor ):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo( valor, None )
        else:      
            nuevoNodo = self.Nodo( valor, None )
            ultimoNodo = self.nodoPorCondicion( lambda n: n.siguiente is None )
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self
    
    def pop( self ):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion( lambda n: n.siguiente.siguiente is None )
            anteUltimoNodo.siguiente = None
        
        self.longitud -= 1

        return self

    def nodoPorCondicion( self, funcionCondicion ):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')
        
        nodoActual = self.raiz
        while not funcionCondicion( nodoActual ):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')
            
        return nodoActual
        
    def __len__( self ):
        return self.longitud

    def __iter__( self ):
        self.current = self.Nodo( None, self.raiz )
        return self

    def __next__( self ):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor
    
    def __repr__( self ):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__( self, valor, siguiente ):
            self.valor = valor
            self.siguiente = siguiente


class MatrizRala:
    def __init__( self, M, N ):
        self.filas = {}
        self.shape = (M, N)

    def __getitem__( self, Idx ):
        # Esta funcion implementa la indexacion ( Idx es una tupla (m,n) ) -> A[m,n]
        #accedo a la fila m en el diccionario
        #recorro la lista enlazada hasta encontrar el valor n
        #devuelvo lo que hay en esa posicion
        if self.filas.get(Idx[0]) == None:
            return 0
        else:
            nodo = self.filas[Idx[0]].raiz
            while nodo != None:
                if nodo.valor[0] == Idx[1]:
                    return nodo.valor[1]
                nodo = nodo.siguiente
            return 0
    
    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        #accedo a la fila m en el diccionario
        #recorro la lista enlazada hasta la posicion n
        #agrego nodo para esa posicion
        if self.filas.get(Idx[0]) == None: #si no hay nada en esa fila, creo una lista enlazada
            self.filas[Idx[0]] = ListaEnlazada()
            self.filas[Idx[0]].push([Idx[1], v])
        else: #si ya hay algo, puede ser que no haya nada en esa posicion o que haya que reemplazar
            if self.filas.get(Idx[0]) == 0:
                self.filas[Idx[0]].insertarFrente([Idx[1], v])
            nodo = self.filas[Idx[0]].raiz
            previo = None
            while nodo != None: #recorro la lista, si encuentra algo en n lo reemplaza
                if nodo.valor[0] < Idx[1]:
                    pass
                if nodo.valor[0] == Idx[1]:
                    nodo.valor = (Idx[1], v)
                    return
                if nodo.valor[0] > Idx[1]:
                    self.filas[Idx[0]].insertarDespuesDeNodo([Idx[1], v], previo)
                    return
                nodo = nodo.siguiente
                previo = nodo
            self.filas[Idx[0]].push([Idx[1], v]) #si llegamos al final de la lista y no se cumple ninguno de los ifs
        

    def __mul__( self, k ):
        # Esta funcion implementa el producto matriz-escalar -> A * k
        if self.filas == None:
            return 0
        for i in self.filas.keys():
            nodo = self.filas[i].raiz
            while nodo != None:
                nodo.valor = [nodo.valor[0], nodo.valor[1] * k]
                nodo = nodo.siguiente

        

    
    def __rmul__( self, k ): #cual es la diferencia con anterior??????????????????
        # Esta funcion implementa el producto escalar-matriz -> k * A
        for i in self.filas.keys():
            nodo = self.filas[i].raiz
            while nodo != None:
                nodo.valor[1] = nodo.valor[1] * k
                nodo = nodo.siguiente

    def __add__( self, other ):
        if self.shape != other.shape:
            raise Exception('Las matrices no tienen las mismas dimensiones')
        res:MatrizRala = MatrizRala(len(self.shape[0]), len(self.shape[1])) #cual es el valor de n?
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res[i,j] = self[i,j] + other[i,j]
        return res
        # Esta funcion implementa la suma de matrices -> A + B
    
    def __sub__( self, other ):
        res:MatrizRala = MatrizRala( len(self.filas), len(self.shape[0]))
        for i in range(len(self.filas)):
            for j in range(len(self.shape[0])):
                res[i,j] = self[i,j] - other[i,j]
        return res
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
    
    def __matmul__( self, other ):
        # COMPLETAR:
        res:MatrizRala = MatrizRala( len(self.filas), len(self.shape[0]))
        for i in range(len(self.filas)):
            for j in range(len(other.shape[0])):
                for k in range(len(self.shape[0])):
                    res[i,j] += self[i,k] * other[k,j]
        return res
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        pass                

        
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            
            res += ']\n'

        res += '])'

        return res

def GaussJordan( A, b ):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado
    pass





