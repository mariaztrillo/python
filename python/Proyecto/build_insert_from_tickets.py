# Autor: Maria Zamora
# Git: https://github.com/mariaztrillo
import os
import re
import sys
from datetime import datetime

def generar_esquema_bd():
    sql = """-- =============================================
-- BASE DE DATOS: SUPERMERCADO
-- =============================================

CREATE DATABASE IF NOT EXISTS supermercado;
USE supermercado;

CREATE TABLE IF NOT EXISTS sucursal (
    id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    cif VARCHAR(20),
    telefono VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    codigo_empleado VARCHAR(10) UNIQUE NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS producto (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) UNIQUE NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS ticket (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    numero_ticket VARCHAR(20) UNIQUE NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    id_empleado INT NOT NULL,
    id_sucursal INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE IF NOT EXISTS ticket_linea (
    id_linea INT AUTO_INCREMENT PRIMARY KEY,
    id_ticket INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad DECIMAL(10,3) NOT NULL,
    importe_linea DECIMAL(10,2) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ticket) REFERENCES ticket(id_ticket),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

CREATE TABLE IF NOT EXISTS pago (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_ticket INT NOT NULL,
    forma_pago VARCHAR(20) NOT NULL,
    autorizacion VARCHAR(50),
    FOREIGN KEY (id_ticket) REFERENCES ticket(id_ticket)
);

"""
    return sql

def leer_facturas(carpeta):
    facturas = {}
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.txt'):
            with open(os.path.join(carpeta, archivo), 'r', encoding='utf-8') as f:
                facturas[archivo] = f.read()
    return facturas

def procesar_facturas(facturas):
    empleados = {}
    productos = {}
    tickets = []
    
    for nombre_archivo, contenido in facturas.items():
        lineas = contenido.split('\n')
        ticket = {}
        
        for i, linea in enumerate(lineas):
            if 'Cajero:' in linea:
                match = re.search(r'Cajero:\s*(\d+)\s*-\s*(.+)', linea)
                if match:
                    codigo = match.group(1)
                    if codigo not in empleados:
                        empleados[codigo] = f"{codigo} - {match.group(2)}"
                    ticket['empleado'] = codigo
            
            elif 'Ticket:' in linea:
                match = re.search(r'Ticket:\s*(\d+)', linea)
                if match:
                    ticket['numero'] = match.group(1)
            
            elif 'Fecha:' in linea:
                fecha_match = re.search(r'Fecha:\s*(\d{2}/\d{2}/\d{4})', linea)
                hora_match = re.search(r'Hora:\s*(\d{2}:\d{2})', linea)
                if fecha_match and hora_match:
                    try:
                        fecha_hora_str = f"{fecha_match.group(1)} {hora_match.group(1)}"
                        fecha_hora_obj = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M')
                        ticket['fecha'] = fecha_hora_obj.strftime('%Y-%m-%d')
                        ticket['hora'] = fecha_hora_obj.strftime('%H:%M')
                    except ValueError:
                        ticket['fecha'] = fecha_match.group(1)
                        ticket['hora'] = hora_match.group(1)
                else:
                    if fecha_match:
                        ticket['fecha'] = fecha_match.group(1)
                    if hora_match:
                        ticket['hora'] = hora_match.group(1)
            
            elif 'CANT  DESCRIPCIÓN' in linea:
                ticket['productos'] = []
                j = i + 2
                while j < len(lineas) and lineas[j].strip() and not lineas[j].startswith('---'):
                    match = re.match(r'(\d+\.?\d*)\s+(.+?)\s+(\d+\.\d{2})\s*€', lineas[j].strip())
                    if match:
                        cantidad = match.group(1)
                        descripcion = match.group(2).strip()
                        importe = match.group(3)
                        
                        # Calcular precio unitario
                        precio_unitario = round(float(importe) / float(cantidad), 2)
                        
                        if descripcion not in productos:
                            productos[descripcion] = precio_unitario
                        
                        ticket['productos'].append({
                            'descripcion': descripcion,
                            'cantidad': cantidad,
                            'importe': importe,
                            'precio_unitario': precio_unitario
                        })
                    j += 1
            
            elif 'SUBTOTAL' in linea:
                match = re.search(r'SUBTOTAL\s+(\d+\.\d{2})\s*€', linea)
                if match:
                    ticket['subtotal'] = match.group(1)
            
            elif 'IVA' in linea:
                match = re.search(r'IVA.*?(\d+\.\d{2})\s*€', linea)
                if match:
                    ticket['iva'] = match.group(1)
            
            elif 'TOTAL A PAGAR' in linea:
                match = re.search(r'TOTAL A PAGAR\s+(\d+\.\d{2})\s*€', linea)
                if match:
                    ticket['total'] = match.group(1)
            
            elif 'FORMA DE PAGO:' in linea:
                match = re.search(r'FORMA DE PAGO:\s*(.+)', linea)
                if match:
                    ticket['pago'] = match.group(1)
        
        if all(k in ticket for k in ['numero', 'fecha', 'subtotal', 'iva', 'total']):
            tickets.append(ticket)
    
    return empleados, productos, tickets

def generar_sql(empleados, productos, tickets):
    sql = generar_esquema_bd()
    
    sql += "-- =============================================\n"
    sql += "-- INSERCIÓN DE DATOS DESDE FACTURAS\n"
    sql += "-- =============================================\n\n"
    
    sql += "INSERT INTO sucursal (nombre, direccion, cif, telefono) VALUES\n"
    sql += "('SUPERMERCADOS EL AHORRO', 'Av. Principal #123 - Madrid', 'B12345678', '910123456');\n\n"
    
    sql += "INSERT INTO empleado (codigo_empleado, nombre_completo) VALUES\n"
    emp_values = []
    for codigo, nombre in empleados.items():
        emp_values.append(f"('{codigo}', '{nombre}')")
    sql += ",\n".join(emp_values) + ";\n\n"
    
    sql += "INSERT INTO producto (descripcion, precio_unitario) VALUES\n"
    prod_values = []
    for descripcion, precio in productos.items():
        desc_escape = descripcion.replace("'", "''")
        prod_values.append(f"('{desc_escape}', {precio})")
    sql += ",\n".join(prod_values) + ";\n\n"
    
    sql += "INSERT INTO ticket (numero_ticket, fecha, hora, id_empleado, id_sucursal, subtotal, iva, total) VALUES\n"
    ticket_values = []
    for ticket in tickets:
        fecha_sql = f"'{ticket['fecha']}'"
        ticket_values.append(
            f"('{ticket['numero']}', {fecha_sql}, '{ticket['hora']}', "
            f"(SELECT id_empleado FROM empleado WHERE codigo_empleado = '{ticket['empleado']}'), "
            f"1, {ticket['subtotal']}, {ticket['iva']}, {ticket['total']})"
        )
    sql += ",\n".join(ticket_values) + ";\n\n"
    
    sql += "INSERT INTO ticket_linea (id_ticket, id_producto, cantidad, importe_linea, precio_unitario) VALUES\n"
    linea_values = []
    for ticket in tickets:
        for producto in ticket['productos']:
            desc_escape = producto['descripcion'].replace("'", "''")
            linea_values.append(
                f"((SELECT id_ticket FROM ticket WHERE numero_ticket = '{ticket['numero']}'), "
                f"(SELECT id_producto FROM producto WHERE descripcion = '{desc_escape}'), "
                f"{producto['cantidad']}, {producto['importe']}, {producto['precio_unitario']})"
            )
    sql += ",\n".join(linea_values) + ";\n\n"
    
    sql += "INSERT INTO pago (id_ticket, forma_pago, autorizacion) VALUES\n"
    pago_values = []
    for ticket in tickets:
        autorizacion = 'NULL'
        pago_values.append(
            f"((SELECT id_ticket FROM ticket WHERE numero_ticket = '{ticket['numero']}'), "
            f"'{ticket['pago']}', {autorizacion})"
        )
    sql += ",\n".join(pago_values) + ";\n"
    
    return sql

def main():
    if len(sys.argv) != 2:
        print("Uso: python build_insert_from_tickets.py <carpeta_facturas>")
        return
    
    carpeta = sys.argv[1]
    
    try:
        facturas = leer_facturas(carpeta)
        
        if not facturas:
            print("\n no se encontraron facturas\n")
            return
        
        empleados, productos, tickets = procesar_facturas(facturas)
        
        sql = generar_sql(empleados, productos, tickets)
        
        with open('InsertUnderlineTicket.sql', 'w', encoding='utf-8') as f:
            f.write(sql)
        
        print(f"\n se procesaron {len(tickets)} tickets:")
        print(f" - {len(empleados)} empleados")
        print(f" - {len(productos)} productos")
        print(" archivo SQL generado correctamente\n")
        
    except Exception as e:
        print(f"\n error: {e}\n")

if __name__ == "__main__":
    main()
    