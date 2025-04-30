import socket
import os

# Configuración del cliente:
HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 4096

#-------Configurar socket cliente-----------------------------
def conectar_servidor():
    cliente = socket.socket()
    try:
        cliente.connect((HOST, PORT))
    except Exception as e:
        print(f"No se pudo conectar con el servidor: {e}")
        exit()
    return cliente

#-----------Mostrar listado de archivos-------------------------
def listar_archivos(cliente):
    cliente.send("listar archivos".encode('utf-8'))
    respuesta = cliente.recv(BUFFER_SIZE).decode('utf-8')
    print("Archivos disponibles en el servidor:")
    print(respuesta)

#--------------------Transferir archivo del cliente al servidor---------------------
def subir_archivo(cliente):
    ruta_local = input("Introduce la ruta del archivo a subir: ").strip()
    if not os.path.exists(ruta_local):
        print("El archivo no existe.")
        return

    nombre_archivo = os.path.basename(ruta_local)
    cliente.send(f"subir {nombre_archivo}".encode('utf-8'))

    # Espera confirmación del servidor
    confirmacion = cliente.recv(BUFFER_SIZE).decode('utf-8')
    if confirmacion != "listo para recibir":
        print("Error en la sincronización.")
        return

    with open(ruta_local, 'rb') as f:
        while True:
            datos = f.read(BUFFER_SIZE)
            if not datos:
                break
            cliente.sendall(datos)
    cliente.send(b"_fin_archivo_")  # Fin del envío

    print("Archivo Transferido Correctamente.")

#------------Descargar archivos desde el servidor al cliente--------------------------
def descargar_archivo(cliente):
    nombre_archivo = input("Introduce el nombre del archivo a descargar: ").strip()
    cliente.send(f"descargar {nombre_archivo}".encode('utf-8'))

    # Espera si el servidor dice que existe el archivo
    respuesta = cliente.recv(BUFFER_SIZE).decode('utf-8')
    if respuesta == "archivo no encontrado":
        print("El archivo no existe en el servidor.")
        return
    else:
        # Ruta de descarga en la carpeta 'descargas/'
        ruta_descarga = os.path.join("/home/loki/Downloads", nombre_archivo)

        with open(ruta_descarga, 'wb') as f:
            while True:
                datos = cliente.recv(BUFFER_SIZE)
                if b"_fin_archivo_" in datos:
                    datos = datos.replace(b"_fin_archivo_", b"")
                    f.write(datos)
                    break
                f.write(datos)
        print(f"Archivo '{nombre_archivo}' Descargado Correctamente en 'Downloads/{nombre_archivo}'.")

#---------------Mostrar historial------------------------------------
def ver_logs(cliente):
    cliente.send("ver logs".encode('utf-8'))
    respuesta = cliente.recv(BUFFER_SIZE).decode('utf-8')
    print("Logs del servidor:")
    print(respuesta)

#---------------Copiar archivo remoto a procesados--------------------
def copiar_archivo_remoto(cliente):
    nombre_archivo = input("Introduce el nombre del archivo a copiar en el directorio procesados: ").strip()
    cliente.send(f"copiar {nombre_archivo}".encode('utf-8'))
    respuesta = cliente.recv(BUFFER_SIZE).decode('utf-8')
    print(respuesta)

#---------------Leer el contenido de un archivo remoto-----------------------------
def leer_archivo_remoto(cliente):
    nombre_archivo = input("Introduce el nombre del archivo remoto a leer: ").strip()
    cliente.send(f"leer {nombre_archivo}".encode('utf-8'))
    contenido = cliente.recv(BUFFER_SIZE).decode('utf-8')
    print("\nContenido del archivo:")
    print(contenido)

#----------------Interfaz menú-----------------------------
def menu():
    while True:
        print("\n<<<<<<<< MENU >>>>>>>>>")
        print("1.- Listar archivos del directorio entrada")
        print("2.- Subir archivo al directorio entrada")
        print("3.- Descargar archivo")
        print("4.- Ver logs")
        print("5.- Copiar archivo al directorio procesados")
        print("6.- Leer archivo remoto")
        print("7.- Salir y cerrar conexion")
        print("\n<<<<<<<<<<<>>>>>>>>>>>>>\n")

        opcion = input("Elige una opción: ").strip()
        cliente = conectar_servidor()

        if opcion == "1":
            listar_archivos(cliente)
        elif opcion == "2":
            subir_archivo(cliente)
        elif opcion == "3":
            descargar_archivo(cliente)
        elif opcion == "4":
            ver_logs(cliente)
        elif opcion == "5":
            copiar_archivo_remoto(cliente)
        elif opcion == "6":
            leer_archivo_remoto(cliente)
        elif opcion == "7":
            print("Saliendo...")
            cliente.close()
            break
        else:
            print("Opción inválida.")
        
        cliente.close()

if __name__ == "__main__":
    menu()
