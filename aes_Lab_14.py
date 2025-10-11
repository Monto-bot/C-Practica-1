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
        self.g = 0x02 
        self.Tabla_EXP = [0] * 512
        self.Tabla_LOG = [0] * 256
        self.Tabla_EXP[0] = 1
        self.Tabla_LOG[1] = 0

        while not gFound:
            exp_val = 1
            valid = True
            for i in range(1, 255):
                exp_val = self.productoPolinomico(exp_val, self.g)
                if exp_val == 1 and i < 254:
                    valid = False
                    break
                self.Tabla_EXP[i] = exp_val
                self.Tabla_LOG[exp_val] = i
            
            exp_val = self.productoPolinomico(exp_val, self.g) # exp_val es g^255
            if valid and exp_val == 0x01:
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
        if a == 0 or b == 0:
            return 0
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
    InvMixMatrix: equivalente a la matriz usada en 5.3.3, pág. 24
    '''
    def __init__(self, key, Polinomio_Irreducible = 0x11B):
        self.key = key
        self.Polinomio_Irreducible = Polinomio_Irreducible
        self.GF = G_F(self.Polinomio_Irreducible)

        self.SBox = [0]*256
        for i in range(len(self.SBox)):
            b = self.GF.inverso(i)
            for j in range(8):
                bi = (b >> j) & 1
                bi4 = (b >> (j + 4)%8) & 1
                bi5 = (b >> (j + 5)%8) & 1
                bi6 = (b >> (j + 6)%8) & 1
                bi7 = (b >> (j + 7)%8) & 1
                ci = (0x63 >> j) & 1
                bit = bi^bi4^bi5^bi6^bi7^ci
                self.SBox[i] |= bit << j

        self.InvSBox = [0]*256
        for i in range(len(self.InvSBox)):
            self.InvSBox[self.SBox[i]] = i

        self.Rcon = [[0x01, 0x00, 0x00, 0x00], [0x02, 0x00, 0x00, 0x00],
                    [0x04, 0x00, 0x00, 0x00], [0x08, 0x00, 0x00, 0x00],
                    [0x10, 0x00, 0x00, 0x00], [0x20, 0x00, 0x00, 0x00],
                    [0x40, 0x00, 0x00, 0x00], [0x80, 0x00, 0x00, 0x00],
                    [0x1b, 0x00, 0x00, 0x00], [0x36, 0x00, 0x00, 0x00]]

        self.InvMixMatrix = [0x0e, 0x0b, 0x0d, 0x09,
                             0x09, 0x0e, 0x0b, 0x0d,
                             0x0d, 0x09, 0x0e, 0x0b,
                             0x0b, 0x0d, 0x09, 0x0e]

    '''
    5.1.1 SUBBYTES()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def SubBytes(self, State):
        for i in range(len(State)):
            r = State[i] >> 4
            c = State[i] & 0x0F
            State[i] = self.SBox[r*16 + c]
        return State

    '''
    5.3.2 INVSUBBYTES()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvSubBytes(self, State):
        for i in range(len(State)):
            r = State[i] >> 4
            c = (State[i] & 0x0F)
            State[i] = self.InvSBox[r*16 + c]
        return State

    '''
    5.1.2 SHIFTROWS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def ShiftRows(self, State):
        newState = [0]*16
        for i in range(16):
            r = int(i/4)
            c = i%4
            newState[r + c*4] = State[r + ((c + r)%4)*4] # State ordenado por columnas
        return newState

    '''
    5.3.1 INVSHIFTROWS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvShiftRows(self, State):
        newState = [0]*16
        for i in range(16):
            r = int(i/4)
            c = i%4
            newState[r + c*4] = State[r + ((c - r)%4)*4] # State ordenado por columnas
        return newState

    '''
    5.1.3 MIXCOLUMNS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def MixColumns(self, State):
        newState = [0]*16
        for c in range(4):  # Para cada columna
            s0, s1, s2, s3 = State[0 + c*4], State[1 + c*4], State[2 + c*4], State[3 + c*4]
            newState[0 + c*4] = self.auxMixColumns(s0, s1, s2, s3)
            newState[1 + c*4] = self.auxMixColumns(s1, s2, s3, s0)
            newState[2 + c*4] = self.auxMixColumns(s2, s3, s0, s1)
            newState[3 + c*4] = self.auxMixColumns(s3, s0, s1, s2)
        return newState
    
    def auxMixColumns(self,s0,s1,s2,s3):
        return (self.GF.producto(0x02, s0) ^
                self.GF.producto(0x03, s1) ^ 
                s2 ^ s3)

    '''
    5.3.3 INVMIXCOLUMNS()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvMixColumns(self, State):
        newState = [0]*16
        for c in range(4):  # Para cada columna
            s0, s1, s2, s3 = State[0 + c*4], State[1 + c*4], State[2 + c*4], State[3 + c*4]
            newState[0 + c*4] = self.auxInvMixColumns(s0, s1, s2, s3)
            newState[1 + c*4] = self.auxInvMixColumns(s1, s2, s3, s0)
            newState[2 + c*4] = self.auxInvMixColumns(s2, s3, s0, s1)
            newState[3 + c*4] = self.auxInvMixColumns(s3, s0, s1, s2)
        return newState
    
    def auxInvMixColumns(self, s0, s1, s2, s3):  #Crec que es mes elegant que multiplicar matrius
        return (self.GF.producto(0x0e, s0) ^ 
                self.GF.producto(0x0b, s1) ^ 
                self.GF.producto(0x0d, s2) ^ 
                self.GF.producto(0x09, s3))

    '''
    5.1.4 ADDROUNDKEY()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def AddRoundKey(self, State, roundKey):
        newState = [0] * 16
        for i in range(16): 
            r = i//4
            c = i%4
            index = r + c * 4
            newState[index] = State[index] ^ roundKey[index]
        return newState
    
    '''
    5.2 KEYEXPANSION()
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def KeyExpansion(self, key):
        size = len(key)
        if size == 16:
            Nk, Nr = 4, 10
        elif size == 24:
            Nk, Nr = 6, 12
        else: # size == 32
            Nk, Nr = 8, 14

        w = []
        for i in range(Nk):
            w.append([key[4*i], key[4*i + 1], key[4*i + 2], key[4*i + 3]])

        for i in range(Nk, 4*(Nr + 1)):
            temp = w[i - 1][:]
            if i % Nk == 0:
                temp = temp[1:] + temp[:1]  #RotWord
                temp = [self.SBox[b] for b in temp] #SubWord
                rcon = self.Rcon[(i // Nk) - 1] #Rcon[i/Nk]
                temp = [temp[j] ^ rcon[j] for j in range(4)]
            elif Nk > 6 and i % Nk == 4:
                temp = [self.SBox[b] for b in temp] #SubWord

            ant = w[i - Nk]
            w.append([ant[j] ^ temp[j] for j in range(4)])

        eKey = []
        for r in range(Nr + 1):
            for c in range(4):
                eKey.extend(w[r*4 + c])
        return eKey

    '''
    5.1 Cipher(), Algorithm 1 pág. 12
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def Cipher(self, State, Nr, Expanded_KEY):
        State = self.AddRoundKey(State, Expanded_KEY[0:16])
        for round in range(1, Nr):
            State = self.SubBytes(State)
            State = self.ShiftRows(State)
            State = self.MixColumns(State)
            State = self.AddRoundKey(State, Expanded_KEY[round*16:(round+1)*16])
        
        State = self.SubBytes(State)
        State = self.ShiftRows(State)
        State = self.AddRoundKey(State, Expanded_KEY[Nr*16:(Nr+1)*16])
        return State    
    
    '''
    5. InvCipher()
    Algorithm 3 pág. 20 o Algorithm 4 pág. 25. Son equivalentes
    FIPS 197: Advanced Encryption Standard (AES)
    '''
    def InvCipher(self, State, Nr, Expanded_KEY):
        State = self.AddRoundKey(State, Expanded_KEY[Nr*16:(Nr+1)*16])
        for round in range(Nr-1,0,-1):
            State = self.InvShiftRows(State)
            State = self.InvSubBytes(State)
            State = self.AddRoundKey(State, Expanded_KEY[round*16:(round+1)*16])
            State = self.InvMixColumns(State)
        State = self.InvShiftRows(State)
        State = self.InvSubBytes(State)
        State = self.AddRoundKey(State, Expanded_KEY[0:16])
        return State

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
        pass
    '''
    Entrada: Nombre del fichero a descifrar.
    Salida: Fichero descifrado usando la clave utilizada en el constructor de la clase.
    Para descifrar se usará el modo CBC, con el IV usado para cifrar. El nombre de
    fichero descifrado será el obtenido al añadir el sufijo .dec al nombre del fichero
    a descifrar: NombreFichero --> NombreFichero.dec
    '''
    def decrypt_file(self, fichero):
        pass
