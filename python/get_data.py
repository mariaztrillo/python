# Autor: Maria Zamora
# Git: https://github.com/mariaztrillo

import requests
from bs4 import BeautifulSoup

def obtener_html(url):
    respuesta = requests.get(url, timeout=10)
    respuesta.raise_for_status()
    respuesta.encoding = 'utf-8'
    return respuesta.text

def analizar_precios(html):
    documento = BeautifulSoup(html, "html.parser")
    tabla = documento.find("table", class_="table-products")
    
    if not tabla:
        return None
    
    filas = tabla.find("tbody").find_all("tr")
    analisis = []
    
    for fila in filas:
        celdas = fila.find_all("td")
        if len(celdas) >= 3:
            nombre = fila.find("th").text.strip()
            tamaño = celdas[1].text.strip()
            precio = celdas[2].text.strip()
            
            # Extraer los ml
            if "ml" in tamaño:
                ml = int(tamaño.replace("ml", "").strip())
                precio_num = float(precio.replace(",", "."))
                
                if ml > 0:
                    precio_ml = precio_num / ml
                    analisis.append({
                        'nombre': nombre,
                        'precio_ml': round(precio_ml, 3)
                    })
    
    return analisis

# URL de tu página
url = "http://localhost:8000/productos.php"

try:
    html = obtener_html(url)
    resultados = analizar_precios(html)

    if resultados:
        print(f"\n tienes {len(resultados)} productos analizados:\n")
        for producto in resultados:
            print(f"{producto['nombre']}: €{producto['precio_ml']} por ml")
        print("\n terminado\n")
    else:
        print("\n no encontré productos\n")

except requests.Timeout:
    print("\n la página tardó demasiado en responder.\n")

except requests.ConnectionError:
    print("\n no puedo conectar, verifica que esté activo el servidor\n")

except requests.HTTPError as e:
    print(f"\n hubo un problema http: {e}\n")

except Exception as e:
    print(f"\n pasó algo inesperado: {e}\n")