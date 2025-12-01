# Autor: Maria Zamora
# Git: https://github.com/mariaztrillo

# importamos librerias de python
import sys 

# validamos los argumentos
# comprobamos que el usuario haya pasado al menos 2 argumentos además del nombre del script
if len(sys.argv) < 3: 
    print("Debe proporcionar el nombre del archivo y el texto a buscar como argumentos.")
     # si no hay suficientes argumentos, mostramos el modo de uso y terminamos el programa
    sys.exit(1)

# guardamos en variables los argumentos pasados por consola
archivo = sys.argv[1] # nombre del archivo a leer
texto = sys.argv[2] # texto que queremos buscar dentro del archivo

# abrimos el archivo en modo lectura, con codificación UTF-8
try:
    with open(archivo, "r", encoding="utf-8") as f:
        # leemos todo el contenido del archivo
        contenido = f.read() 
        # contamos cuántas veces aparece el texto
        cantidad = contenido.count(texto)
        # imprimimos el resultado
        print(f"{texto} : {cantidad}")

# aquí capturamos los errores de argumentos y de lectura de archivos 
except FileNotFoundError:
    print(f"Error: El archivo '{archivo}' no existe.")
except Exception as e:
    print(f"Ocurrió un error al leer el archivo: {e}")


#python3 findfile.py archivo.txt MAR para ejecutar en consola
#python3 findfile.py
#python3 findfile.py noexiste.txt 
#python3 findfile.py python.txt Este es mi contenido
