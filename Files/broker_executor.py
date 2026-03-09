import os
import subprocess
import socket
import threading
import sys

# 1. Identificación de versión
self.log.info("--- [VERSIÓN 004: DEBUG MAESTRO] ---")

# 2. Verificación de Entorno (Diagnóstico)
try:
    # Verificamos qué Python y qué librerías tenemos
    self.log.info(f"Python Version: {sys.version}")
    self.log.info(f"CWD: {os.getcwd()}")
    
    # Listamos archivos en el directorio actual para ver si hay persistencia
    self.log.info(f"Archivos locales: {os.listdir('.')}")
    
    # Intentamos ver quién manda aquí
    who = subprocess.check_output("whoami", shell=True).decode().strip()
    self.log.info(f"Usuario ejecutando: {who}")
except Exception as e:
    self.log.error(f"Fallo en diagnóstico inicial: {e}")

# 3. El Broker con Logs Detallados
def start_broker(comp):
    comp.log.info("Iniciando hilo de red...")
    try:
        # Intentamos importar socket de nuevo dentro del hilo por si acaso
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Probamos el bind
        comp.log.info("Intentando bind en 0.0.0.0:1883")
        s.bind(('0.0.0.0', 1883))
        s.listen(5)
        comp.log.info("!!! [EXITO] PUERTO 1883 ABIERTO Y ESCUCHANDO !!!")
        
        while True:
            conn, addr = s.accept()
            comp.log.info(f"CONEXIÓN DETECTADA DESDE: {addr}")
            conn.close()
    except Exception as e:
        comp.log.error(f"Fallo crítico en el Broker: {e}")

# Lanzamos el proceso
try:
    t = threading.Thread(target=start_broker, args=(self,), daemon=True)
    t.start()
    self.log.info("Hilo del Broker lanzado correctamente.")
    self.col_res.insert("DEBUG 004: Hilo Lanzado")
except Exception as e:
    self.log.error(f"No se pudo lanzar el hilo: {e}")