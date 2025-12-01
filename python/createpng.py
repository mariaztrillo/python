# Autor: Maria Zamora
# Git: https://github.com/mariaztrillo

# importamos librerías de Python
import os
import sys
import string
import random

try:
    # obtenemos el nombre de la carpeta y el número de archivos desde los argumentos de la línea de comandos
    nombre_carpeta = sys.argv[1]
    numero_archivos = int(sys.argv[2])

    # limpiar la pantalla
    os.system('cls' if os.name == 'nt' else 'clear')

    # crear la carpeta si no existe
    if not os.path.exists(nombre_carpeta):
        os.mkdir(nombre_carpeta)

    # definimos los caracteres posibles para los nombres aleatorios
    CARACTERES = string.ascii_letters + string.digits
    LONGITUD = 15  # longitud de cada nombre de archivo

    # lista para guardar los nombres de archivos creados
    archivos_creados = []

    # generamos los archivos con nombres aleatorios
    for _ in range(numero_archivos):
        while True:
            # generamos un nombre aleatorio + extensión .png
            nombre = ''.join(random.choice(CARACTERES) for _ in range(LONGITUD)) + ".png"
            if nombre not in archivos_creados:  
                archivos_creados.append(nombre)
                break

        
        ruta_completa = os.path.join(nombre_carpeta, nombre)
        with open(ruta_completa, 'w'):
            pass

    # mostramos los archivos creados
    print(f"\nSe han creado {len(archivos_creados)} archivos en '{nombre_carpeta}':\n")
    for nombre in archivos_creados:
        print(nombre)

# capturamos errores de argumentos y otros posibles errores
except IndexError:
    print("Error: Debe proporcionar el nombre de la carpeta y el número de archivos como argumentos.")
except ValueError:
    print("Error: El número de archivos debe ser un valor entero.")
except Exception as e:
    print(f"Ocurrió un error al crear los archivos: {e}")


# python3 createpng.py carpeta 10  