'''
Genera un cuerpo finito usando como polinomio irreducible el dado representado como un
entero. Por defecto toma el polinomio del AES. Los elementos del cuerpo los
representaremos por enteros 0 <= n <= 255.
'''
class G_F:
    '''
    Entrada: un entero que representa el polinomio para construir el cuerpo Tabla_EXP
    y Tabla_LOG dos tablas, la primera tal que en la posición i-ésima tenga valor
    a=g**i y la segunda tal que en la posición a-ésima tenga el valor i tal que a=g**i
    (g generador del cuerpo finito representado por el menor entero entre 0 y 255).
    Se usa una optimización típica en algoritmos de GF(2^8): duplicamos Tabla_EXP
    para permitir indexación sin tener que calcular el módulo.
    '''
    def __init__(self, Polinomio_Irreducible = 0x11B):
        self.Polinomio_Irreducible = Polinomio_Irreducible

        gFound = False
        self.g = 0x2
        while not gFound:
            self.Tabla_EXP = [0]*512
            self.Tabla_LOG = [0]*256
            self.Tabla_EXP[0] = 1
            self.Tabla_LOG[1] = 0
            gi = self.g
            for i in range(1, 255):
                self.Tabla_EXP[i] = gi
                self.Tabla_LOG[gi] = i
                gi = self.productoPolinomico(gi, self.g)
            if gi == 0x1:
                gFound = True
            else:
                self.g += 1
        # Duplicamos Tabla_EXP
        for i in range(255, 512):
            self.Tabla_EXP[i] = self.Tabla_EXP[i - 255]

    '''
    Entrada: dos elementos del cuerpo representados por enteros entre 0 y 255.
    Salida: un elemento del cuerpo representado por un entero entre 0 y 255 que es el
    producto en el cuerpo de la entrada.
    Se calcula usando la definición en términos de polinomios ya que se usa para
    construir las tablas Tabla_EXP y Tabla_LOG (y por tanto estas no se pueden usar).
    '''
    def productoPolinomico(self, a, b):
        res = 0
        while b:
            if b & 1:
                res ^= a
            a = self.xTimes(a)
            b >>= 1
        return res

    '''
    Entrada: un elemento del cuerpo representado por un entero entre 0 y 255.
    Salida: un elemento del cuerpo representado por un entero entre 0 y 255 que es el
    producto en el cuerpo de 'n' y 0x02 (el polinomio X).
    '''
    def xTimes(self, n):
        result = n << 1 # multiplicar por x = desplazar a la izquierda
        if n & 0x80:
            result ^= self.Polinomio_Irreducible
        return result & 0xFF

    '''
    Entrada: dos elementos del cuerpo representados por enteros entre 0 y 255.
    Salida: un elemento del cuerpo representado por un entero entre 0 y 255 que es el
    producto en el cuerpo de la entrada.
    Se calcula usando la definición en términos de Tabla_EXP y Tabla_LOG.
    '''
    def producto(self, a, b):
        logA = self.Tabla_LOG[a]
        logB = self.Tabla_LOG[b]
        return self.Tabla_EXP[logA + logB]
        # no hace falta hacer el módulo (logA + logB)%255 gracias a la optimización
        # de duplicar Tabla_EXP que hemos hecho en la función __init__

    '''
    Entrada: un elementos del cuerpo representado por un entero entre 0 y 255.
    Salida: 0 si la entrada es 0, el inverso multiplicativo de n representado por un
    entero entre 1 y 255 si n <> 0.
    Se calcula usando la definición en términos de Tabla_EXP y Tabla_LOG.
    '''
    def inverso(self, n):
        if n == 0:
            return 0
        
        logN = self.Tabla_LOG[n]
        return self.Tabla_EXP[255 - logN]

'''
Documento de referencia: Federal Information Processing Standards Publication (FIPS)
197: Advanced Encryption Standard (AES) https://doi.org/10.6028/NIST.FIPS.197-upd1.
El nombre de los métodos, tablas, etc son los mismos (salvo capitalización) que los
empleados en el FIPS 197.
'''
class AES:
    '''
    Entrada:
      key: bytearray de 16 24 o 32 bytes
      Polinomio_Irreducible: Entero que representa el polinomio para construir el cuerpo
      SBox: equivalente a la tabla 4, pág. 14
      InvSBOX: equivalente a la tabla 6, pág. 23
      Rcon: equivalente a la tabla 5, pág. 17
      InvMixMatrix : equivalente a la matriz usada en 5.3.3, pág. 24
    '''
    def __init__(self, key, Polinomio_Irreducible = 0x11B):
        self.Polinomio_Irreducible
        self.SBox
        self.InvSBox
        self.Rcon
        self.InvMixMatrix

    '''
    5.1.1 SUBBYTES()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def SubBytes(self, State):

    '''
    5.3.2 INVSUBBYTES()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvSubBytes(self, State):

    '''
    5.1.2 SHIFTROWS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def ShiftRows(self, State):

    '''
    5.3.1 INVSHIFTROWS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvShiftRows(self, State):

    '''
    5.1.3 MIXCOLUMNS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def MixColumns(self, State):

    '''
    5.3.3 INVMIXCOLUMNS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvMixColumns(self, State):

    '''
    5.1.4 ADDROUNDKEY()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def AddRoundKey(self, State, roundKey):

    '''
    5.2 KEYEXPANSION()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def KeyExpansion(self, key):

    '''
    5.1 Cipher(), Algorithm 1 pág. 12
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def Cipher(self, State, Nr, Expanded_KEY):

    '''
    5. InvCipher()
    Algorithm 3 pág. 20 o Algorithm 4 pág. 25. Son equivalentes
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvCipher(self, State, Nr, Expanded_KEY):

    '''
    Entrada: Nombre del fichero a cifrar.
    Salida: Fichero cifrado usando la clave utilizada en el constructor de la clase.
    Para cifrar se usará el modo CBC, con IV correspondiente a los 16 primeros bytes
    obtenidos al aplicar el sha256 a la concatenación de "IV" y la clave usada para
    cifrar. Por ejemplo:
      Key 0x0aba289662caa5caaa0d073bd0b575f4
      IV asociado 0xeb53bf26511a8c0b67657ccfec7a25ee
      Key 0x46abd80bdcf88518b2bec4b7f9dee187b8c90450696d2b995f26cdf2fe058610
      IV asociado 0x4fe68dfd67d8d269db4ad2ebac646986
    El padding usado será PKCS7. El nombre de fichero cifrado será el obtenido al añadir
    el sufijo .enc al nombre del fichero a cifrar: NombreFichero --> NombreFichero.enc
    '''
    def encrypt_file(self, fichero):

    '''
    Entrada: Nombre del fichero a descifrar.
    Salida: Fichero descifrado usando la clave utilizada en el constructor de la clase.
    Para descifrar se usará el modo CBC, con el IV usado para cifrar. El nombre de
    fichero descifrado será el obtenido al añadir el sufijo .dec al nombre del fichero
    a descifrar: NombreFichero --> NombreFichero.dec
    '''
    def decrypt_file(self, fichero):
