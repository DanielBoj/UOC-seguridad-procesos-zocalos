""" _summary_ : Simular la entrada y salida de coches de un parking de 300 plazas. """

# Importamso la librería time para poder simular procesos con un tiempo de ejecución concreto.
import time
# Importamos la librería multiprocessing para poder crear procesos.
import multiprocessing

""" El principal problema de este código es que la variable coches que van a compartir los procesos no se encuentra bloqueda, por lo que puede ocurrir que se produzca una condición de carrera. Es decir, que los procesos en ejecución paralela cambien el valor de la variable coches de forma inesperada. """
def entrada(coches):
    """ _summary_ : Simula la entrada de coches al parking. """
    #simulamos la entrada de 200 coches
    for i in range(200):
        # Simulamos el tiempo de entrada de cada coche.
        time.sleep(0.01)
        # Aumentamos el contador de coches denro del parking.
        coches.value = coches.value + 1

def salida(coches):
    """ _summary_ : Simula la salida de coches del parking."""
    #simulamos la salida de 200 coches
    for i in range(200):
        # Simulamos el tiempo de salida de cada coche.
        time.sleep(0.01)
        # Disminuimos el contador de coches denro del parking.
        coches.value = coches.value - 1

# Creamos el proceso principal.
if __name__ == '__main__':
    # Creamos la variable coches que va a ser compartida por los procesos.
    coches = multiprocessing.Value('i', 300)
    # Creamos los procesos de entrada y salida de coches pasándole la variable coches como argumento.
    entrada_coche = multiprocessing.Process(target=entrada, args=(coches,))
    salida_coche = multiprocessing.Process(target=salida, args=(coches,))

    # Iniciamos los procesos. Como hemos comentado, estos no realizan el bloqueo de la variable.
    entrada_coche.start()
    salida_coche.start()

    # Esperamos a que los procesos terminen su ejecución. Veremos que el resultado no es el esperado.
    entrada_coche.join()
    salida_coche.join()
    
    # Mostramos la variable por pantalla para comprobar que el resultado no es el esperado.
    print("Coches dentro del parking: ", coches.value)