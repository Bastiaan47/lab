import socket
import os

#Configuracion del cliente:
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

#--------------------Tansferir archivo del cliente al servidor---------------------
def subir_archivo(cliente):
    ruta_local = input("Introduce la ruta del archivo a subir: ").strip()
    if not os.path.exists(ruta_local):
        print("El archivo no existe.")
        return

    nombre_archivo= os.path.basename(ruta_local)
    cliente.send(f"subir {nombre_archivo}".encode('utf-8'))

    #espera confirmacion del servidor
    confirmacion = cliente.recv(BUFFER_SIZE).decode('utf-8')
    if confirmacion != "listo para recibir":
        print("Error en la sincronizacion.")
        return

    with open(ruta_local, 'rb') as f:
        while True:
            datos= f.read(BUFFER_SIZE)
            if not datos:
                break
            cliente.sendall(datos)
    cliente.send(b"_fin_archivo_")  #fin del envio

    print("Archivo Transferido Correctamente.")

#------------Descargar archivos desde el sevidor al cliente--------------------------
def descargar_archivo(cliente):
    nombre_archivo= input("Introduce el nombre del archivo a descargar: ").strip()
    cliente.send(f"descargar {nombre_archivo}".encode('utf-8'))

    #espera si el servidor dice que existe el archivo
    respuesta= cliente.recv(BUFFER_SIZE).decode('utf-8')
    if respuesta == "archivo no encontrado":
        print("El archivo no existe en el servidor.")
        return
    else:
        with open(nombre_archivo, 'wb') as f:
            while True:
                datos= cliente.recv(BUFFER_SIZE)
                if b"_fin_archivo_" in datos:
                    datos= datos.replace(b"_fin_archivo_", b"")
                    f.write(datos)
                    break
                f.write(datos)
        print(f"Archivo '{nombre_archivo}' Descargado Correctamente.")

#---------------Mostrar historial------------------------------------
def ver_logs(cliente):
    cliente.send("ver logs".encode('utf-8'))
    respuesta= cliente.recv(BUFFER_SIZE).decode('utf-8')
    print("Logs del servidor:")
    print(respuesta)

#----------------Interfaz menu-----------------------------
def menu():
    while True:
        print("\n------ Opciones ------")
        print("1.- [Listar archivos]")
        print("2.- [Subir archivo]")
        print("3.- [Descargar archivo]")
        print("4.- [Ver logs]")
        print("5.- [Salir]")
        print("\n----------------------")
        
        opcion= input("Elige una opcion: ").strip()
        cliente= conectar_servidor()
#--------------------------------------
        if opcion == "1":
            listar_archivos(cliente)
        elif opcion == "2":
            subir_archivo(cliente)
        elif opcion == "3":
            descargar_archivo(cliente)
        elif opcion == "4":
            ver_logs(cliente)
        elif opcion == "5":
            print("Saliendo...")
            cliente.close()
            break
        else:
            print("Opcion inválida.")
#---------------------------------------
        cliente.close()

if __name__ == "__main__":
    menu()
