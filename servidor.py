import socket
import os
import shutil

#configuracion del servidor host 0.0.0.0 esta a la espera de señales
HOST = '0.0.0.0'
PORT = 5000
Directorio_Entrada = '/home/batman/Laboratorio/entrada/'
Directorio_Procesados = '/home/batman/Laboratorio/procesados/'
Archivo_Logs= '/home/batman/Laboratorio/logs.txt'
BUFFER_SIZE= 4096 #tamaño de bytes para transferencias por socket

#funcion para agregar mensajes al archivo de logs
def escribir_log(mensaje):
    with open(Archivo_Logs, 'a') as f:
        f.write(mensaje + "\n")

#crear socket
servidor = socket.socket()
servidor.bind((HOST, PORT))
servidor.listen(1)
print("Esperando conexión...")

#-------------Manejar conexiones entrantes, procesa solicitudes del cliente y maneja errores---------------------
while True:
    conn, addr = servidor.accept()
    print(f"Conectado con {addr}")

    try:
        mensaje = conn.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Mensaje recibido: {mensaje}")

        if mensaje.lower() == 'listar archivos':
            try:
                archivos = os.listdir(Directorio_Entrada)
                if archivos:
                    respuesta = "\n".join(archivos) + "\n"
                else:
                    respuesta = "No hay archivos en el directorio de entrada."
            except FileNotFoundError:
                respuesta = f"El directorio '{Directorio_Entrada}' no existe."
            conn.send(respuesta.encode('utf-8'))
            escribir_log(f"[{addr}] Listó archivos")

        elif mensaje.startswith("copiar "):
            archivo_a_copiar = mensaje[7:].strip()
            ruta_origen = os.path.join(Directorio_Entrada, archivo_a_copiar)
            ruta_destino = os.path.join(Directorio_Procesados, archivo_a_copiar)

            if os.path.exists(ruta_origen):
                shutil.copy(ruta_origen, ruta_destino)
                conn.send(f"Archivo '{archivo_a_copiar}' copiado correctamente a 'procesados/'.".encode('utf-8'))
                escribir_log(f"[{addr}] Copió archivo '{archivo_a_copiar}'")
            else:
                conn.send(f"El archivo '{archivo_a_copiar}' no existe en 'entrada/'.".encode('utf-8'))

        elif mensaje.startswith("leer "):
            archivo_a_leer = mensaje[5:].strip()
            ruta_archivo = os.path.join(Directorio_Entrada, archivo_a_leer)

            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r') as f:
                    contenido = f.read()
                conn.send(contenido.encode('utf-8'))
                escribir_log(f"[{addr}] Leyó archivo '{archivo_a_leer}'")
            else:
                conn.send(f"El archivo '{archivo_a_leer}' no existe en 'entrada/'.".encode('utf-8'))

        elif mensaje.startswith("subir "):
            nombre_archivo = mensaje[6:].strip()
            ruta_destino = os.path.join(Directorio_Entrada, nombre_archivo)

            conn.send("listo para recibir".encode('utf-8'))

            with open(ruta_destino, 'wb') as f:
                while True:
                    datos = conn.recv(BUFFER_SIZE)
                    if b"_fin_archivo_" in datos:
                        datos = datos.replace(b"_fin_archivo_", b"")
                        f.write(datos)
                        break
                    f.write(datos)
            escribir_log(f"[{addr}] Subio archivo '{nombre_archivo}'")
            print(f"Archivo '{nombre_archivo}' recibido y guardado.")

        elif mensaje.startswith("descargar "):
            nombre_archivo = mensaje[10:].strip()
            ruta_origen = os.path.join(Directorio_Entrada, nombre_archivo)

            if os.path.exists(ruta_origen):
                conn.send("archivo encontrado".encode('utf-8'))
                with open(ruta_origen, 'rb') as f:
                    while True:
                        datos = f.read(BUFFER_SIZE)
                        if not datos:
                            break
                        conn.sendall(datos)
                conn.send(b"_fin_archivo_")
                escribir_log(f"[{addr}] Descargo archivo '{nombre_archivo}'")
            else:
                conn.send("archivo no encontrado".encode('utf-8'))

        elif mensaje.lower() == "ver logs":
            if os.path.exists(Archivo_Logs):
                with open(Archivo_Logs, 'r') as f:
                    contenido_logs = f.read()
                if not contenido_logs:
                    contenido_logs = "El archivo de logs está vacio."
                conn.send(contenido_logs.encode('utf-8'))
            else:
                conn.send("El archivo de logs no existe.".encode('utf-8'))
            escribir_log(f"[{addr}] Solicito ver logs")

        else:
            conn.send("Instruccion no reconocida.".encode('utf-8'))

    except Exception as e:
        print(f"Error durante la comunicación: {e}")

    conn.close()
    print("Conexión cerrada.")
