import os
import shutil
import threading
import time

# Rutas
Directorio_Entrada = '/home/hmarin/servidor_archivos/entrada/'
Directorio_Procesados = '/home/hmarin/servidor_archivos/procesados/'
Directorio_Logs = '/home/hmarin/servidor_archivos/logs/'
Log_File = os.path.join(Directorio_Logs, 'registro.log')

# Lock para sincronizar el acceso al registro.log
log_lock = threading.Lock()

def procesar_archivo(nombre_archivo):
    origen = os.path.join(Directorio_Entrada, nombre_archivo)
    destino = os.path.join(Directorio_Procesados, nombre_archivo)
    
    # Verificar si el archivo aún existe (podría haber sido movido)
    if not os.path.exists(origen):
        return

    # Mover el archivo a procesados
    shutil.move(origen, destino)

    # Registrar la operación
    with log_lock:
        with open(Log_File, 'a') as log:
            log.write(f"{time.ctime()}: Archivo '{nombre_archivo}' movido a 'procesados/'\n")
    print(f"Procesado: {nombre_archivo}")

def demonio():
    print("Demonio iniciado, monitoreando 'entrada/' cada 10 segundos...")
    archivos_procesados = set()

    while True:
        archivos_actuales = set(os.listdir(Directorio_Entrada))

        nuevos_archivos = archivos_actuales - archivos_procesados

        for archivo in nuevos_archivos:
            t = threading.Thread(target=procesar_archivo, args=(archivo,))
            t.start()

        archivos_procesados = archivos_actuales

        time.sleep(10)

if __name__ == "__main__":
    demonio()
