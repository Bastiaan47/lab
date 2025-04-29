import socket
import os
import shutil

#configuracion del servidor host 0.0.0.0 esta a la espera de señales
HOST= '0.0.0.0'
PORT= 5000
Directorio_Entrada='/home/loki/servidor_archivos/entrada/'
Directorio_Procesados='/home/loki/servidor_archivos/procesados/'


servidor = socket.socket()

# Asociar a una IP y puerto con bind
servidor.bind(('0.0.0.0', 5000))

# Escuchar conexiones
servidor.listen(1)
print("Esperando conexión...")

# Aceptar una conexión
conn, addr = servidor.accept()
print(f"Conectado con {addr}")

# Recibir mensaje
mensaje = conn.recv(1024).decode()
print("Cliente dijo:", mensaje)

#si recibe el mensaje de listar archivos , lo hara en el directorio entrada
if mensaje.lower() == 'listar archivos':
    try:
        archivos=os.listdir(Directorio_Entrada)
        if archivos:
            respuesta = "\n".join(archivos) + "\n"
        else:
            respuesta="no hay archivos en el directorio de entrada"
    except FileNotFoundError:
        respuesta = f"El directorio '{Directorio_Entrada}' no existe."
    
    conn.send(respuesta.encode())


instruccion = conn.recv(1024).decode().strip()
print(f"Instrucción recibida: {instruccion}")

if instruccion.startswith("copiar "):
    archivo_a_copiar = instruccion[7:]
    ruta_origen = os.path.join(Directorio_Entrada, archivo_a_copiar)
    ruta_destino = os.path.join(Directorio_Procesados, archivo_a_copiar)

    if os.path.exists(ruta_origen):
            shutil.copy(ruta_origen, ruta_destino)
            conn.send(f"Archivo '{archivo_a_copiar}' copiado correctamente a 'procesados/'".encode())
    else:
            conn.send(f"El archivo '{archivo_a_copiar}' no existe en 'entrada/'".encode())

elif instruccion.startswith("leer "):
    archivo_a_leer = instruccion[5:]
    ruta_archivo = os.path.join(Directorio_Entrada, archivo_a_leer)

    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as f:
            contenido = f.read()
        conn.send(contenido.encode())
    else:
        conn.send(f"El archivo '{archivo_a_leer}' no existe en 'entrada/'".encode())




conn.close()
servidor.close()


