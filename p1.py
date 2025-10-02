class G_F:
    '''
    Genera un cuerpo finito usando como polinomio irreducible el dado
    representado como un entero. Por defecto toma el polinomio del AES.
    Los elementos del cuerpo los representaremos por enteros 0<= n <= 255.
    '''

    def __init__(self, Polinomio_Irreducible = 0x11B):
        '''
        Entrada: un entero que representa el polinomio para construir el cuerpo
        Tabla_EXP y Tabla_LOG dos tablas, la primera tal que en la posici´on
        i-´esima tenga valor a=g**i y la segunda tal que en la posici´on a-´esima
        tenga el valor i tal que a=g**i. (g generador del cuerpo finito
        representado por el menor entero entre 0 y 255.)
        '''
        self.Polinomio_Irreducible
        self.Tabla_EXP
        self.Tabla_LOG
        self.g

    def xTimes(self, n):
        '''
        Entrada: un elemento del cuerpo representado por un entero entre 0 y 255
        Salida: un elemento del cuerpo representado por un entero entre 0 y 255
        que es el producto en el cuerpo de ’n’ y 0x02 (el polinomio X).
        '''

    def producto(self, a, b):
        '''
        Entrada: dos elementos del cuerpo representados por enteros entre 0 y 255
        Salida: un elemento del cuerpo representado por un entero entre 0 y 255
        que es el producto en el cuerpo de la entrada.
        Atenci´on: Se valorar´a la eficiencia. No es lo mismo calcularlo
        usando la definici´on en t´erminos de polinomios o calcular
        usando las tablas Tabla_EXP y Tabla_LOG.
        '''

    def inverso(self, n):
        '''
        Entrada: un elementos del cuerpo representado por un entero entre 0 y 255
        Salida: 0 si la entrada es 0,
        el inverso multiplicativo de n representado por un entero entre
        1 y 255 si n <> 0.
        Atenci´on: Se valorar´a la eficiencia.
        '''

class AES:
    '''
    Documento de referencia:
    Federal Information Processing Standards Publication (FIPS) 197: Advanced Encryption
    Standard (AES) https://doi.org/10.6028/NIST.FIPS.197-upd1
    El nombre de los m´etodos, tablas, etc son los mismos (salvo capitalizaci´on)
    que los empleados en el FIPS 197
    '''

    def __init__(self, key, Polinomio_Irreducible = 0x11B):
        '''
        Entrada:
        key: bytearray de 16 24 o 32 bytes
        Polinomio_Irreducible: Entero que representa el polinomio para construir
        el cuerpo
        SBox: equivalente a la tabla 4, p´ag. 14
        InvSBOX: equivalente a la tabla 6, p´ag. 23
        Rcon: equivalente a la tabla 5, p´ag. 17
        InvMixMatrix : equivalente a la matriz usada en 5.3.3, p´ag. 24
        '''
        self.Polinomio_Irreducible
        self.SBox
        self.InvSBox
        self.Rcon
        self.InvMixMatrix

    def SubBytes(self, State):
        '''
        5.1.1 SUBBYTES()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def InvSubBytes(self, State):
        '''
        5.3.2 INVSUBBYTES()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def ShiftRows(self, State):
        '''
        5.1.2 SHIFTROWS()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def InvShiftRows(self, State):
        '''
        5.3.1 INVSHIFTROWS()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def MixColumns(self, State):
        '''
        5.1.3 MIXCOLUMNS()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def InvMixColumns(self, State):
        '''
        5.3.3 INVMIXCOLUMNS()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def AddRoundKey(self, State, roundKey):
        '''
        5.1.4 ADDROUNDKEY()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def KeyExpansion(self, key):
        '''
        5.2 KEYEXPANSION()
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def Cipher(self, State, Nr, Expanded_KEY):
        '''
        5.1 Cipher(), Algorithm 1 p´ag. 12
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def InvCipher(self, State, Nr, Expanded_KEY):
        '''
        5. InvCipher()
        Algorithm 3 p´ag. 20 o Algorithm 4 p´ag. 25. Son equivalentes
        FIPS 197: Advanced Encryption Standard (AES)
        '''

    def encrypt_file(self, fichero):
        '''
        Entrada: Nombre del fichero a cifrar
        Salida: Fichero cifrado usando la clave utilizada en el constructor
        de la clase.
        Para cifrar se usar´a el modo CBC, con IV correspondiente a los 16
        primeros bytes obtenidos al aplicar el sha256 a la concatenaci´on
        de "IV" y la clave usada para cifrar. Por ejemplo:
        Key 0x0aba289662caa5caaa0d073bd0b575f4
        IV asociado 0xeb53bf26511a8c0b67657ccfec7a25ee
        Key 0x46abd80bdcf88518b2bec4b7f9dee187b8c90450696d2b995f26cdf2fe058610
        IV asociado 0x4fe68dfd67d8d269db4ad2ebac646986
        El padding usado ser´a PKCS7.
        El nombre de fichero cifrado ser´a el obtenido al a~nadir el sufijo .enc
        al nombre del fichero a cifrar: NombreFichero --> NombreFichero.enc
        '''

    def decrypt_file(self, fichero):
        '''
        Entrada: Nombre del fichero a descifrar
        Salida: Fichero descifrado usando la clave utilizada en el constructor
        de la clase.
        Para descifrar se usar´a el modo CBC, con el IV usado para cifrar.
        El nombre de fichero descifrado ser´a el obtenido al a~nadir el sufijo .dec
        al nombre del fichero a descifrar: NombreFichero --> NombreFichero.dec
        '''
