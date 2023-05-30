""" 
_summary_ Programa sencillo para demostrar la encriptación RSA. 
_author_  : Daniel Boj dboj@uoc.edu
_version_ : 1.0
"""
import random

# Declaramos los número primos que serán la base de nuestro código
prime_list = []
# Declaramos la llave pública y privada, serán tuplas de dos valores
public_key = None
private_key = None


def sieve_of_eratosthenes(n):
    """ Función para calcular los números primos menores que n que
    se basa en el algoritmo de la Sieve de Eratóstenes.
    Devuelve una lista con los números primos menores que n. 
    Tenemos que crear un array con n elementos marcados todos como True.
    El primer número primo es el 2, por lo que empezamos a marcar como False
    los múltiplos de 2 hasta n.
    El siguiente número primo es el 3, por lo que empezamos a marcar como False
    los múltiplos de 3 hasta n.
    El siguiente número primo es el 5, por lo que empezamos a marcar como False
    los múltiplos de 5 hasta n.
    Y así sucesivamente hasta que llegamos a la raíz cuadrada de n.
    """
    prime_list = [True for i in range(n + 1)]
    prime_list[0] = False
    prime_list[1] = False

    # Vamos a incluir en la lista todos los número de 2048 bits
    prime = 2 ** (2048 - 1)
    while prime * prime <= n:
        if prime_list[prime]:
            # Marcamos como False todos los múltiplos de prime
            for i in range(prime * 2, n, prime):
                prime_list[i] = False
        prime += 1

    # Creamos una lista con los números primos
    return [p for p in range(2, n) if prime_list[p]]


# Pasamos el ceiling de la lista de números de 2048 bits
prime_list = sieve_of_eratosthenes((2048 ** 2) - 1)


def mcd(a, b):
    """ Función para calcular el máximo común divisor de dos números.
    Podmeos usar una función recursiva gracias al algoritmo de Euclides. """
    if a == 0:
        return b
    return mcd(b % a, a)


def get_e(e, phi):
    """ Función para calcular el valor de e. """
    # Para mejorar la seguridad escogeremos un valor random de una lista de valores posibles
    e_list = []
    while e < phi:
        if mcd(e, phi) == 1:
            e_list.append(e)
            e += 1
        else:
            e += 1
    # Escogemos un valor random de la lista de valores posibles
    e = random.choice(e_list)
    return int(e)


def get_d(d, e, phi):
    """ Función para calcular el valor de d. """
    while True:
        if (d * e) % phi == 1:
            break
        else:
            d += 1
    return d


def compress(text):
    """ Función para comprimir un texto. """
    return text.encode('utf-8').hex()


def decompress(text):
    """ Función para descomprimir un texto. """
    return bytes.fromhex(text).decode('utf-8')


def set_keys():
    """ Función para crear las llaves de encriptación pública y privada. """
    global prime_list, public_key, private_key
    p = random.choice(prime_list)
    prime_list.remove(p)
    q = random.choice(prime_list)
    p, q = 151, 5  # get_random_prime(), get_random_prime()
    # Calculamos n, el producto de p y q que sirve como base para la encriptación
    n = p * q

    # Calculamos phi, el producto de p-1 y q-1 que sirve para calcular la llave privada
    # y que se basa en el teorema de Euler
    phi = (p - 1) * (q - 1)

    # e es un número primo que es menor que phi y que no tiene factores comunes con phi
    # se usa para calcular la llave pública
    e = 2

    # Procedemos a buscar el MCD de e y phi, si es mayor que 1, entonces no son primos relativos
    # y debemos aumentar e hasta que lo sean, podemos ver que e se modifica en el proceso
    e = get_e(e, phi)

    # Calculamos d, de decrypt, el inverso multiplicativo de e módulo phi, d debe cumplir que
    # (d * e) % phi = 1 o lo que es lo mismo, (d * e) = 1 + k * phi
    # donde k es un entero cualquiera
    k = 2
    d = (k * phi + 1) // e
    d = get_d(d, e, phi)

    print(f"e: {e}, d: {d}")

    # Asignamos los valores de las llaves
    public_key = (e, n)
    private_key = (d, n)


def encrypt(message):
    """ Función para encriptar un mensaje. La fórmula base es la siguiente:
    C = M ^ e mod n, donde C es el mensaje encriptado, M es el mensaje original,
    e es la llave pública y n es el producto de p y q.
    """
    global public_key
    # Destructuring de la llave pública
    e, n = public_key
    return pow(message, e, n)


def decrypt(message):
    """ Función para desencriptar un mensaje. La fórmula base es la siguiente:
    M = C ^ d mod n, donde M es el mensaje original, C es el mensaje encriptado,
    d es la llave privada y n es el producto de p y q.
    """
    global private_key
    # Destructuring de la llave privada
    d, n = private_key
    return pow(message, d, n)


def text_to_ascii(text):
    """ Función para convertir texto a ascii. """
    return [ord(char) for char in text]


def ascii_to_text(ascii_list):
    """ Función para convertir ascii a texto. """
    return ''.join(map(chr, ascii_list))


if __name__ == "__main__":
    # Capturamos el mensaje a encriptar
    message = input("Ingrese el mensaje a encriptar: ")
    # Convertimos el mensaje a ascii
    ascii_list = text_to_ascii(message)
    # Creamos las llaves
    set_keys()
    # Encriptamos el mensaje
    encrypted_message = [encrypt(char) for char in ascii_list]
    print(f"Mensaje encriptado: {encrypted_message}")
    print(f"Mensaje encriptado en texto: {ascii_to_text(encrypted_message)}")
    readeable_encrypted_message = compress(ascii_to_text(encrypted_message))
    print(
        f"Mensaje encriptado en texto legible: {readeable_encrypted_message}")
    # Desencriptamos el mensaje
    decrypted_message = [decrypt(char) for char in encrypted_message]
    print(f"Mensaje desencriptado: {decrypted_message}")
    # Convertimos el mensaje desencriptado a texto
    decrypted_message = ascii_to_text(decrypted_message)
    print(f"Mensaje desencriptado en texto: {decrypted_message}")
