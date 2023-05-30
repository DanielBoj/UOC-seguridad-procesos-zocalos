""" _summary_ : Simular la entrada y salida de coches de un parking de 300 plazas. """

# Importamos la librería time para poder simular procesos con un tiempo de ejecución concreto.
import time
# Importamos la librería multiprocessing para poder crear procesos.
import multiprocessing

""" Refactorizamos el código para evitar el efecto carrera.
Para ello, realizaremos el bloqueo del estado dentro dentro de nuestras funciones para asegurar la consistencia de la variable compartida por los subprocesos. """

""" Añadimos como parámetro un locker para bloquearla. """


def entrada(coches, locker):
    """ _summary_ : Simula la entrada de coches al parking. """
    # Bloqueamos la variable coches.
    locker.acquire()
    # Informamos del número de coches dentro del parking.
    print("Coches dentro del parking: ", coches.value)
    # Simulamos la entrada de 200 coches
    # Informamos el inicio de la simulación.
    print("Muchos coches entrando...")
    for i in range(200):
        # Simulamos el tiempo de entrada de cada coche.
        time.sleep(0.01)
        # Aumentamos el contador de coches denro del parking.
        coches.value = coches.value + 1
    # Mostramos por pantalla el número de coches dentro del parking.
    print("Coches dentro del parking tras la entrada: ", coches.value)
    # Liberamos la variable coches.
    locker.release()


""" Añadimos como parámetro un locker para bloquearla. """


def salida(coches, locker):
    """ _summary_ : Simula la salida de coches del parking."""
    # Bloqueamos la variable coches.
    locker.acquire()
    # Informamos de los coches dentro del parking.
    print("Coches dentro del parking: ", coches.value)
    # Simulamos la salida de 200 coches
    # Informamos del inicio de la simulación.
    print("Muchos coches saliendo...")
    for i in range(200):
        # Simulamos el tiempo de salida de cada coche.
        time.sleep(0.01)
        # Disminuimos el contador de coches denro del parking.
        coches.value = coches.value - 1
    # Mostramos por pantalla el número de coches dentro del parking.
    print("Coches dentro del parking tras la salida: ", coches.value)
    # Liberamos la variable coches.
    locker.release()


# Creamos el proceso principal.
if __name__ == '__main__':
    # Variable compartida por nuestros procesos.
    coches = multiprocessing.Value('i', 300)
    # Creamos el locker para bloquear la variable coches.
    locker = multiprocessing.Lock()
    # Creamos los procesos de entrada y salida de coches pasándole la variable coches como argumento.
    entrada_coche = multiprocessing.Process(
        target=entrada, args=(coches, locker))
    salida_coche = multiprocessing.Process(
        target=salida, args=(coches, locker))

    # Iniciamos los procesos. Como hemos comentado, estos no realizan el bloqueo de la variable.
    entrada_coche.start()
    salida_coche.start()

    # Esperamos a que los procesos terminen su ejecución. Veremos que el resultado no es el esperado.
    entrada_coche.join()
    salida_coche.join()

    """ Vamos a jugar un poco con la omniscencia del programador.
    Así haremos más divertido el proceso. Sabemos que si entran 200 coches y
    salen 200 coches, debemos mantener los 300 coches dentro del parking.
    Así que comprobaremos que lso datos son correctos y no se ha 
    producido el efecto carrera. """
    if coches.value == 300:
        print("""Has conseguido que el programa funcione correctamente.
              Felicidades, eres un buen programador.
              LVL UP!""")
    else:
        print("""Has conseguido que el programa funcione incorrectamente.
              Debes mejorar tus habilidades de programación.
              LVL DOWN!""")
