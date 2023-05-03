""" Este programa demuestra cómo se pueden ejecutar tareas en multihilo con Python. """
# Importamos las librerías necesarias
# Threading permite manejar los hilos implementando por detrás _thread.
import threading
# Time nos permite controlar el tiempo durante el que se va a ejecutar un hilo.
import time
# Datetime nos permite controlar el tiempo de ejecución de los hilos.
import datetime
# Queue nos permite manejar las colas de los hilos.
import queue


def Buscar_Llave():
    """ Esta función representa la tarea de buscar la llave. """
    # La primera tarea que se ejecutará tiene el tiempo de ejecución más alto, esto significa que deberemos manejar
    # la ejecución de los hilos para ser capaces de ordenar la ejecución del proceso de forma correcta. Así, deberemos
    # asegurarnos de que el resto de procesos esperen a que este proceso finalice antes de iniciarse, para ello usaremos
    # join()
    time.sleep(0.9)
    # Imprimimos por pantalla que estamos buscando la llave.
    print('1.Busco la llave.')

def Encontrar_Llave(res: queue.Queue, key: bool):
    """ Esta función representa la tarea de encontrar la llave. Solo podemos encontrar la llave si aún no la tenemos en
    nuestro bolsillo. """
    # Esta tarea un tiempo de ejecución menor a la anterior, por lo que tenemos que asegurarnos de que se ejecuta antes la
    # tarea anterior para comenzar esta, además, tiene un tiempo de ejecución mayor que la siguiente, por lo que la siguiente
    # tarea no debe finalizar antes que esta.
    time.sleep(0.7)
    if not key:
        # Imprimimos por pantalla que hemos encontrado la llave.
        print('2.Ya he encontrado la llave.')
        # Añadimos un valor a la cola para indicar que hemos encontrado la llave. Luego capturaremos la cola en el programa
        # main y podremos cambiar los valores de los booleanos de control. La funcion se comportará así como una función
        # pura con un valor de return.
        res.put(True)
        # Salimos de la función para que no se ejecute el resto de código.
        return
    # Si ya tenemos la llave, no es necesario encontrala de nuevo.
    print('2.No puedo encontrar la llave porque ya la tengo!.')

def Abrir_Puerta(res: queue.Queue, key: bool):
    """ Esta función representa la tarea de abrir la puerta. Solo podemos abrir la puerta si tenemos la llave.
    Para poder abrir la puerta, tenemos que tener la llave. """
    # Esta tarea tiene un tiempo de ejecución menor que la anterior, por lo que deberemos asegurarnos de que la anterior ha
    # finalizado su ejecución antes de iniciarla, y tiene un tiempo de ejecución menor que la siguiente, por lo que acabará de
    # ejecutarse antes, aún así, mantendremos el control secuencia de ejecución de los hilos para poder asignar correctamente
    # la variable con la que trabajamos antes de iniciar la siguiente tarea.
    time.sleep(0.3)
    # Comprobamos que tengamos la llave para poder abrir la puerta.
    if key:
        # Imprimimos por pantalla que hemos abierto la puerta.
        print('3.Abro la puerta.')
        # Añadimos un valor a la cola para indicar que hemos abierto la puerta. Luego capturaremos la cola en el programa
        # main y podremos cambiar los valores de los booleanos de control. La funcion se comportará así como una función
        # pura con un valor de return.
        res.put(True)
        # Salimos de la función para que no se ejecute el resto de código.
        return
    # Si no tenemos la llave, no podemos abrir la puerta.
    print('3. No puedo abrir la puerta, no tengo la llave!')
    # Añadimos un valor a la cola para indicar que no hemos abierto la puerta. Luego capturaremos la cola en el programa
    # main y podremos cambiar los valores de los booleanos de control. La funcion se comportará así como una función
    # pura con un valor de return.
    res.put(False)

def Cerrar_Puerta(res: queue.Queue, door: bool):
    """ Esta función representa la tarea de cerrar la puerta. Solo podemos cerrar la puerta si la hemos abierto. """
    # Esta tarea tiene un tiempo de ejecución mayor a la anterior, por lo que tardaría más en ejecutarse que la anterior,
    # y así veríamos finalizado el proceso de abrir la puerta antes del de cerrar la puerta.
    # Aún así, como hemos incluido el trabajo con las variables de control, necesitamos que la tarea anteriror finalice
    # para tener seteada la variable de forma correcta, por lo tanto, mantenemos el control secuencial de las tareas.
    time.sleep(0.5)
    # Comprobamos que hayamos abierto la puerta para poder cerrarla.
    if door:
        # Imprimimos por pantalla que hemos cerrado la puerta.
        print('4.Cierro la puerta.')
        # Añadimos un valor a la cola para indicar que hemos cerrado la puerta. Luego capturaremos la cola en el programa
        # main y podremos cambiar los valores de los booleanos de control. La funcion se comportará así como una función
        # pura con un valor de return.
        res.put(False)
        # Salimos de la función para que no se ejecute el resto de código.
        return
    # Si no hemos abierto la puerta, no podemos cerrarla.
    print('4.No puedo cerrar la puerta porque no la he abierto todavía!.')
    # Añadimos un valor a la cola para indicar que no hemos cerrado la puerta. Luego capturaremos la cola en el programa
    # main y podremos cambiar los valores de los booleanos de control. La funcion se comportará así como una función
    # pura con un valor de return.
    res.put(True)

def Guardar_Llave(res : queue.Queue, key: bool):
    """ Esta función representa la tarea de guardar la llave. Solo podemos guardar la llave si la hemos encontrado. """
    time.sleep(0.1)
    if key:
        print('5.Guardo la llave.')
        res.put(False)
        return
    print('5.No puedo guardar la llave porque no la he encontrado todavía!.')
    res.put(True)

def __main__():
    # Variables para que sea más interactivo y divertido
    Is_Key = False
    Is_Open = False
    # Cola para guardar los resultados del hilo
    res = queue.Queue()

    tiempo_ini = datetime.datetime.now()

    #proceos 1
    t_Buscar_Lave = threading.Thread(target = Buscar_Llave)
    t_Buscar_Lave.start()
    t_Buscar_Lave.join()
    #proceso 2
    t_Encontrar_Llave = threading.Thread(target = Encontrar_Llave, args = (res, Is_Key))
    t_Encontrar_Llave.start()
    t_Encontrar_Llave.join()
    Is_Key = res.get()
    # EncontrarLlave()
    #proceso 3
    t_Abrir_Puerta = threading.Thread(target = Abrir_Puerta, args = (res, Is_Key))
    t_Abrir_Puerta.start()
    t_Abrir_Puerta.join()
    Is_Open = res.get()
    # AbrirPuerta()
    #proceso 4
    t_Cerrar_Puerta = threading.Thread(target = Cerrar_Puerta, args = (res, Is_Open))
    t_Cerrar_Puerta.start()
    # Como se trata de la última tarea, no es necesario hacer un join, ya que no hay más tareas que ejecutar.	
    
    Is_Open = res.get()
    # CerrarPuerta()
    #proceso 5
    t_Guardar_Llave = threading.Thread(target = Guardar_Llave, args = (res, Is_Key))
    t_Guardar_Llave.start()
    t_Guardar_Llave.join()
    Is_Key = res.get()

    if not Is_Key and not Is_Open:
        print('La puerta está cerrada y la llave en nuestro bolsillo.')
    else:
        print('No hemos podido abrir esa puerta!')
    tiempo_fin = datetime.datetime.now()
    print('Tiempo total de ejecución:',str(tiempo_fin.second - tiempo_ini.second))

# Ejecutar el programa principal mediante una función main
if __name__ == '__main__':
    __main__()
