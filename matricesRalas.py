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
        # Devuelve el valor de la matriz en la posición (m, n)
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
        # Asigna un valor a la matriz en la posición (m, n)
        if self.filas.get(Idx[0]) == None: #si no hay nada en esa fila, creo una lista enlazada
            self.filas[Idx[0]] = ListaEnlazada()
        nodo = self.filas[Idx[0]].raiz
        prev = None
        while nodo != None:
            if nodo.valor[0] == Idx[1]:
                nodo.valor = (Idx[1], v)
                return
            if nodo.valor[0] > Idx[1]:
                if prev is None:
                    self.filas[Idx[0]].insertarFrente((Idx[1], v))
                else:
                    self.filas[Idx[0]].insertarDespuesDeNodo((Idx[1], v), prev)
                return
            prev = nodo
            nodo = nodo.siguiente
        self.filas[Idx[0]].push((Idx[1], v))

    def __mul__( self, k ):
        # Multiplica la matriz por un escalar
        res:MatrizRala = MatrizRala(self.shape[0], self.shape[1])
        for fila in range(self.shape[0]):
            if fila not in self.filas: #si el diccionario esta vacio, pasar a proxima fila
                continue
            nodo = self.filas[fila].raiz
            while nodo != None:
                res[fila, nodo.valor[0]] = nodo.valor[1] * k
                nodo = nodo.siguiente
        return res

    def __rmul__( self, k ):
        # Multiplica un escalar por la matriz
        '''res:MatrizRala = MatrizRala(self.shape[0], self.shape[1])
        for fila in range(self.shape[0]):
            if fila not in self.filas: #si el diccionario esta vacio, pasar a proxima fila
                continue
            nodo = self.filas[fila].raiz
            while nodo != None:
                res[fila, nodo.valor[0]] = nodo.valor[1] * k
                nodo = nodo.siguiente
        return res'''
        return self * k #es lo mismo que lo anterior pero llamando al metodo???

    def __add__( self, other ):
        # Suma de matrices
        if self.shape != other.shape:
            raise Exception("Las matrices son de dimensiones diferentes")
        res = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res[i, j] = self[i, j] + other[i, j]
        return res

    def __sub__( self, other ):
        # Resta de matrices
        if self.shape != other.shape:
            raise Exception("Las matrices son de dimensiones diferentes")
        res = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                res[i, j] = self[i, j] - other[i, j]
        return res
    
    def __matmul__( self, other ):
        # Producto matricial
        if self.shape[1] != other.shape[0]:
            raise ValueError("Las dimensiones de las matrices no permite hacer el producto matricial")

        res = MatrizRala(self.shape[0], other.shape[1])
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                for k in range(self.shape[1]):
                    res[i, j] += self[i, k] * other[k, j]
        return res          

    def invertir_filas(self, fila1, fila2):
        # Intercambia dos filas de la matriz
        self.filas[fila1], self.filas[fila2] = self.filas[fila2], self.filas[fila1]
        
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

    #si las filas de A no son iguales a las filas de b, no se puede haver gauss jordan ya que no se puede hacer la matriz aumentada
    if A.shape[0] != b.shape[0]:
        raise ValueError("Las dimensiones de la matriz A y el vector b no son compatibles para buscar una solucion")
    
    #creamos la matriz aumentada, copiando los valores de A y agregando los valores de b
    matriz_aumentada = MatrizRala(A.shape[0], A.shape[1] + 1)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            matriz_aumentada[i, j] = A[i, j]
        matriz_aumentada[i, A.shape[1]] = b[i, 0]
    
    #hacemos gauss jordan
    for i in range(A.shape[0]): #para agarrar el pivote de cada fila
        #agarramos el pivote correspondiente a la fila i
        pivote = matriz_aumentada[i, i]
        if pivote == 0: #si es 0, verificamos que no haya otra fila con un valor distinto de 0 en la columna i. si lo hay, invertimos las filas para obtener el pivot en el lugar correcto
            for l in range(i+1, A.shape[0]):
                if matriz_aumentada[l, i] != 0:
                    matriz_aumentada.invertir_filas(l, j) 
                    #invierte las filas
                    pivote = matriz_aumentada[i, i] #actualizamos el pivote
                    break
                else:
                    raise ValueError("El sistema no tiene solucion unica") #pasamos a la proximo columna 

        #hacer 0 los demas elementos de la columna
        for fila in range(A.shape[0]):
            if fila == i: #estoy en pivote, no hago nada
                continue

            for j in range(A.shape[1] + 1):
                matriz_aumentada[i, j] = matriz_aumentada[i, j] / pivote #hacemos que el pivote sea 1

            for k in range(A.shape[0] + 1):
                if k != i:
                    factor = matriz_aumentada[k, i]
                    for j in range(A.shape[1] + 1):
                        matriz_aumentada[k, j] = matriz_aumentada[k, j] - matriz_aumentada[i, j] * factor

    #verificar si hay infinitas soluciones
    filas_en_cero = True
    for i in range(matriz_aumentada.shape[0]):
        for j in range(matriz_aumentada.shape[1]):
            if matriz_aumentada[i, j] != 0:
                filas_en_cero = False #si encuentra un valor distinto de 0, no hay infinitas soluciones
        if filas_en_cero: #si todas las filas son 0, hay infinitas soluciones
            raise ValueError("El sistema tiene infinitas soluciones")
    
    #verificar si no hay solucion
    fila_menos_solucion_cero = True
    for i in range(matriz_aumentada.shape[0]):
        for j in range(matriz_aumentada.shape[1]-1):
            if matriz_aumentada[i, j] != 0:
                fila_menos_solucion_cero = False
        if fila_menos_solucion_cero:
            if matriz_aumentada[i, matriz_aumentada.shape[1]-1] != 0: #si hay una fila con todos los valores 0 y el valor de la ultima columna (valor que representa b) es distinto de 0, no hay solucion
                raise ValueError("El sistema no tiene solucion")
        
    #devolver la solucion
    res = MatrizRala(A.shape[1], 1) #creamos una matriz de 1 columna y tantas filas como columnas de A para devolver la solucion
    for i in range(matriz_aumentada.shape[0]):
        res[i, 0] = matriz_aumentada[i, matriz_aumentada.shape[1]-1] / matriz_aumentada[i, i]
        #copiamos los valores de la ultima columna de la matriz aumentada (representa el b) divido el valor del pivote a la matriz de solucion
    print(res)
    return res