import os
import threading
import time
from threading import Semaphore, Lock
import shutil

# Rutas
Directorio_Entrada = '/home/loki/servidor_archivos/entrada/'
Directorio_Procesados = '/home/loki/servidor_archivos/procesados/'
Archivo_Logs = '/home/loki/servidor_archivos/logs/registro.log'

# Sincronización
lock_log = Lock()
semaforo = Semaphore()

# Guardar nombres de archivos existentes al arrancar
archivos_existentes = set(os.listdir(Directorio_Entrada))

def escribir_log(mensaje):
    with lock_log:
        with open(Archivo_Logs, 'a') as f:
            f.write(mensaje + '\n')

def procesar_archivo(nombre_archivo):
    ruta_origen = os.path.join(Directorio_Entrada, nombre_archivo)
    ruta_destino = os.path.join(Directorio_Procesados, nombre_archivo)

    with semaforo:
        try:
            if os.path.exists(ruta_origen):
                shutil.move(ruta_origen, ruta_destino)
                escribir_log(f"[Demonio] Archivo '{nombre_archivo}' procesado y movido a 'procesados/'.")
        except Exception as e:
            escribir_log(f"[Demonio] Error procesando '{nombre_archivo}': {e}")

def demonio():
    print("[Demonio] Iniciado. Monitoreando archivos nuevos cada 10 segundos...")
    while True:
        time.sleep(10)
        archivos_actuales = set(os.listdir(Directorio_Entrada))
        nuevos_archivos = archivos_actuales - archivos_existentes

        for archivo in nuevos_archivos:
            t = threading.Thread(target=procesar_archivo, args=(archivo,))
            t.start()
            archivos_existentes.add(archivo)

if __name__ == "__main__":
    demonio()
