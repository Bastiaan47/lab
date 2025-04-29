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


archivoCopiar = conn.recv(1024).decode().strip()
print(f"El cliente pidió copiar el archivo: {archivoCopiar}")

ruta_origen = os.path.join(Directorio_Entrada, archivoCopiar)
ruta_destino = os.path.join(Directorio_Procesados, archivoCopiar)

if os.path.exists(ruta_origen):
    shutil.copy(ruta_origen, ruta_destino)
    conn.send(f"Archivo '{archivoCopiar}' copiado correctamente a 'procesados/'".encode())
else:
    conn.send(f"El archivo '{archivoCopiar}' no existe en 'entrada/'".encode())



conn.close()
servidor.close()


