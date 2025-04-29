
import socket

#configuracion del cliente
HOST= '127.0.0.1'
PORT= 5000

# Crear socket
cliente = socket.socket()

# Conectarse al servidor
cliente.connect(('127.0.0.1', 5000))

# Enviar solicitud para listar archivo
cliente.send("listar archivos".encode())

# Recibir respuesta
respuesta = cliente.recv(1024).decode()
print("Archivos en el directorio 'entrada/':")
print(respuesta)

archivo_a_copiar = input("Introduce el nombre del archivo que deseas copiar a 'procesados/': ")

# Enviar el nombre del archivo al servidor
cliente.send(archivo_a_copiar.encode())

# Recibir confirmación del servidor
respuesta_copia = cliente.recv(1024).decode()
print(respuesta_copia)


cliente.close()