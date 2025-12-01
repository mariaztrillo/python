# Autor: Maria Zamora
# Git: https://github.com/mariaztrillo

# importamos librerias de python
import os 
import sys

# print(f"lectura del archivo {archivo}...:\n")
try:
    # obtenemos el nombre del archivo desde los argumentos de la línea de comandos
    archivo = sys.argv[1]
    # limpiar la pantalla
    os.system('cls' if os.name == 'nt' else 'clear')

    # abrimos el archivo en modo lectura, con codificación UTF-8
    with open(archivo, 'r', encoding='utf-8') as file:
        # enumeramos las líneas del archivo, obteniendo índice (número de línea) y contenido
        for indice,linea in enumerate (file, start=1):
            # imprimimos el número de línea con 4 dígitos y el contenido de la línea
            print(f"{indice:04d}: {linea}", end='')

# capturamos los errores de argumentos y de lectura de archivos             
except IndexError:
    print("Error: Debe proporcionar el nombre del archivo como argumento.")
except FileNotFoundError:
    print(f"El archivo '{archivo}' no existe.")
except Exception as e:
    print(f"Ocurrio un error al leer el archivo: {e}")


#python3 typefile.py archivo.txt para ejecutar en consola