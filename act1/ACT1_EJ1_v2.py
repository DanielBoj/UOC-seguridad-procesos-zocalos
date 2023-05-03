# Importamos la librería os que nos permite acceder a funcionalidades dependientes del Sistema Operativo
# manejando archivos y directorios.
import os

# Importamos la librería sys que nos permite acceder a algunas variables y funciones que interactuan
# con el interprete de Python.
import sys

# Inclusión personal: Añado un print que identifica el proceso padre por pantalla.
print("Padre", os.getpid())

# Creamos un pipe con la función pipe() de la librería os que nos permite manejar la comunicación
# entre procesos a través de file descriptors. La función pipe() devuelve una tupla de dos file
# descriptors que se asignan a las variables r y w, r para lectura y w para escritura.
r, w = os.pipe()

# Creamos un proceso hijo con la función fork() de la librería os que nos permite crear un proceso
# hijo que es una copia del padre. La función fork() devuelve un valor entero, 0 al
# proceso hijo y el PID del proceso hijo al proceso padre. Asignamos este valor a la variable
# processid.
processid = os.fork()
# Inclusión personal: Añadimos un printo del valor de processid para comprobar que el proceso
# padre y el hijo tienen valores distintos. Veremos que más adelante, coincide con el valor de
# que vamos a obtener llamando a la función getpid() de la librería os dentro del hijo.
print("Variable processid, coincidirá con el PID del hijo", processid)
# A través del bloque condicional if, podemos comprobar el el proceso es el padre o el hijo
# Si el proceso es el padre, el valor de processid será distinto de 0, que en Python se interpreta
# como un true, y se procederá a ejecutar el bloquede de instrucciones del padre.
if processid > 0: # Cambio personal: Cambio el operador de comparación de  a > porque incluyo un manejo de errores.
    # Cerramos el file descriptor de escritura del pipe.
    os.close(w)
    # Abrimos el file descriptor de lectura del pipe con la función fdopen() de la librería os
    # que nos permite abrir un file descriptor como un objeto de tipo file. Asignamos este objeto
    # a la variable r de nuestro pipe, es decir, el descriptor de lectura que abrimos en el pipe.
    r = os.fdopen(r)
    # Informamos por pantalla que el proceso es el padre y leemos el contenido del file descriptor
    # del pipe con la función read() de la librería sys que nos permite leer el contenido de un
    # objeto.
    print("Padre leyendo")
    # Leemos el contenido del file descriptor del pipe y lo asignamos a la variable str.
    str = r.read()
    # Imprimimos por pantalla el contenido de la variable str, que es el texto que escribió el
    # proceso hijo en el pipe.
    print("texto:", str)
    # Añado a modo personal una línea de código para informar por pantalla que el proceso padre
    # ha finalizado.
    print("Padre Cierra")
    # Finalizamos el proceso con un código de salida 0, éxito.
    sys.exit(0)

# Si el proceso es el hijo, processid devuelve 0, que en Pyhon se interpreta como un false,
# y se procederá a ejecutar el bloque de instrucciones del hijo.
elif not processid: # Cambio personal: Cambio el operador de comparación a not porque incluyo un manejo de errores.
    # Inclusión personal: Añado un print que identifica el proceso hijo por pantalla.
    print("Hijo", os.getpid())
    # Cerramos el file descriptor de lectura del pipe.
    os.close(r)
    # Abrimos el descriptor de escritura del pipe con la función fdopen() de la librería os
    # que permite que abramos un descriptor como un objeto de tipo file y asignamos el objeto
    # a la variable w de nuestro pipe, es decir, el descriptor de escritura que abrimos en el pipe.
    # Además, indicamos que el acceso al archivo se hará en modo escritura, 'w', usando la
    # la función write().
    w = os.fdopen(w, 'w')
    # Informamos por pantalla que el proceso es el hijo y que estamos escribiendo en el pipe hijo.
    print("Hijo escribiendo")
    # Usamos la función de sys write() para escribir en el file descriptor w del pipe.
    # Escribimos el texto "Hello World", el cual será leído por el proceso padre.
    w.write("Hello World")
    # Cerramos el file descriptor de escritura del pipe.
    w.close()
    # Informamos por pantalla que el proceso hijo ha finalizado.
    print("Hijo Cierra")
    # Finalizamos el proceso con un código de salida 0, éxito.
    sys.exit(0)
else: # Cambio personal: Incluyo un manejo de errores.
    # Informamos por pantalla que el proceso no es ni el padre ni el hijo.
    print("Error en el proceso")
    # Finalizamos el proceso con un código de salida 1, error.
    sys.exit(1)