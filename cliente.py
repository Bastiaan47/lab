import socket

# Configuración del cliente
HOST = '127.0.0.1'
PORT = 5000

# Crear socket
cliente = socket.socket()
cliente.connect((HOST, PORT))

# Enviar solicitud para listar archivos
cliente.send("listar archivos".encode())

# Recibir lista de archivos
respuesta = cliente.recv(1024).decode()
print("Archivos en el directorio 'entrada/':")
print(respuesta)


print("¿Qué deseas hacer?")
print("1. Copiar un archivo a 'procesados/'")
print("2. Leer el contenido de un archivo")

opcion = input("Escribe 1 o 2: ")

if opcion == "1":
    archivo_a_copiar = input("Introduce el nombre del archivo que deseas copiar: ")
    instruccion = f"copiar {archivo_a_copiar}"
elif opcion == "2":
    archivo_a_leer = input("Introduce el nombre del archivo que deseas leer: ")
    instruccion = f"leer {archivo_a_leer}"
else:
    print("Opción no válida.")
    cliente.close()
    exit()

# Enviar la instrucción al servidor
cliente.send(instruccion.encode())

# Recibir la respuesta del servidor
respuesta_final = cliente.recv(4096).decode()  
print("Respuesta del servidor:")
print(respuesta_final)

# Cerrar conexión
cliente.close()
