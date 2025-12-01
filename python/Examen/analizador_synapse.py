# Autor: Maria Zamora
# Examen: Analizador de Partidas - Synapse Game

import sys

def leer_y_procesar_archivo(nombre_archivo):
    """
    Lee el archivo y procesa los datos de partidas.
    Retorna un diccionario con las estadísticas calculadas.
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        # Inicializar variables para estadísticas
        total_partidas = 0
        jugadores = set()
        suma_puntos = 0
        mejores_puntajes = {}
        
        # Procesar cada línea del archivo
        for linea in lineas:
            linea = linea.strip()
            if not linea:  # Saltar líneas vacías
                continue
            
            try:
                # Separar los datos por punto y coma
                datos = linea.split(';')
                
                # Validar que tenga los 4 campos requeridos
                if len(datos) != 4:
                    print(f"Advertencia: línea con formato incorrecto: {linea}")
                    continue
                
                nickname = datos[0]
                nivel = datos[1]
                puntaje_str = datos[2]
                minutos_str = datos[3]
                
                # Convertir puntaje a número
                puntaje = int(puntaje_str)
                
                # Actualizar estadísticas
                total_partidas += 1
                jugadores.add(nickname)
                suma_puntos += puntaje
                
                # Actualizar mejor puntaje del jugador
                if nickname in mejores_puntajes:
                    if puntaje > mejores_puntajes[nickname]:
                        mejores_puntajes[nickname] = puntaje
                else:
                    mejores_puntajes[nickname] = puntaje
                    
            except ValueError:
                print(f"Advertencia: datos no válidos en línea: {linea}")
                continue
            except Exception as e:
                print(f"Advertencia: error procesando línea: {linea} - {e}")
                continue
        
        # Calcular puntuación media
        if total_partidas > 0:
            media_puntos = suma_puntos / total_partidas
        else:
            media_puntos = 0
        
        # Retornar resultados
        return {
            'total_partidas': total_partidas,
            'total_jugadores': len(jugadores),
            'puntuacion_media': round(media_puntos, 2),
            'mejores_puntajes': mejores_puntajes,
            'exito': True
        }
        
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return {'exito': False, 'error': 'Archivo no encontrado'}
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return {'exito': False, 'error': str(e)}

def generar_archivo_resumen(resultados, nombre_archivo='resumen_general.txt'):
    """Genera el archivo resumen_general.txt con las estadísticas."""
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("RESUMEN GENERAL SYNAPSE GAME\n")
            archivo.write("----------------------------\n")
            archivo.write(f"Total de partidas: {resultados['total_partidas']}\n")
            archivo.write(f"Total de jugadores distintos: {resultados['total_jugadores']}\n")
            archivo.write(f"Puntuación media global: {resultados['puntuacion_media']}\n")
        print(f"✓ Archivo '{nombre_archivo}' generado correctamente.")
        return True
    except Exception as e:
        print(f"✗ Error al generar archivo '{nombre_archivo}': {e}")
        return False

def generar_archivo_ranking(resultados, nombre_archivo='ranking_jugadores.txt'):
    """Genera el archivo ranking_jugadores.txt con los jugadores ordenados."""
    try:
        # Ordenar jugadores por puntaje (de mayor a menor)
        ranking = sorted(
            resultados['mejores_puntajes'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("RANKING DE JUGADORES\n")
            archivo.write("--------------------\n")
            
            for posicion, (jugador, puntaje) in enumerate(ranking, 1):
                archivo.write(f"{posicion}) {jugador} - {puntaje} puntos\n")
        
        print(f"✓ Archivo '{nombre_archivo}' generado correctamente.")
        return True
    except Exception as e:
        print(f"✗ Error al generar archivo '{nombre_archivo}': {e}")
        return False

def mostrar_resultados_en_pantalla(resultados):
    """Muestra los resultados en pantalla para verificación."""
    print("\n" + "="*50)
    print("RESULTADOS DEL ANÁLISIS")
    print("="*50)
    print(f"Total de partidas: {resultados['total_partidas']}")
    print(f"Jugadores distintos: {resultados['total_jugadores']}")
    print(f"Puntuación media: {resultados['puntuacion_media']}")
    
    print("\n" + "-"*40)
    print("RANKING DE MEJORES PUNTAJES")
    print("-"*40)
    
    ranking = sorted(
        resultados['mejores_puntajes'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for pos, (jugador, puntos) in enumerate(ranking, 1):
        print(f"{pos:2d}. {jugador:20} - {puntos:4d} puntos")

# ============================================================================
# PROGRAMA PRINCIPAL - VERSIÓN CORREGIDA (PIDE ARCHIVO POR TECLADO)
# ============================================================================

print("="*60)
print("ANALIZADOR DE PARTIDAS - SYNAPSE GAME")
print("="*60)

# PEDIR ARCHIVO POR TECLADO (COMO DICE EL ENUNCIADO)
archivo_entrada = input("Introduce el nombre del archivo a leer: ")
print(f"Procesando archivo: {archivo_entrada}")
print("-"*60)

try:
    # 1. Leer y procesar archivo
    resultados = leer_y_procesar_archivo(archivo_entrada)
    
    if not resultados.get('exito', False):
        print("\n✗ No se pudo procesar el archivo. Saliendo del programa.")
        sys.exit(1)
    
    # 2. Mostrar resultados en pantalla
    mostrar_resultados_en_pantalla(resultados)
    
    # 3. Generar archivo resumen_general.txt
    print("\n" + "-"*60)
    print("Generando archivos de salida...")
    print("-"*60)
    
    archivo1_ok = generar_archivo_resumen(resultados)
    
    # 4. Generar archivo ranking_jugadores.txt
    archivo2_ok = generar_archivo_ranking(resultados)
    
    # 5. Mensaje final
    print("\n" + "="*60)
    if archivo1_ok and archivo2_ok:
        print("¡PROCESO COMPLETADO EXITOSAMENTE!")
        print("Archivos generados:")
        print("  • resumen_general.txt")
        print("  • ranking_jugadores.txt")
    else:
        print("PROCESO COMPLETADO CON ALGUNOS ERRORES")
    print("="*60)
    
except KeyboardInterrupt:
    print("\n\nPrograma interrumpido por el usuario.")
except Exception as e:
    print(f"Error inesperado: {e}")