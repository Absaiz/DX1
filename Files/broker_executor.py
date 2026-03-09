import socket
import threading
import os
import subprocess

# 1. Identificacion (Para confirmar que ha actualizado)
self.log.info("--- [GITHUB VERSION 0.1] ---")

def run_broker(comp):
    try:
        # Abrimos el puerto 1883 de forma real
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 1883))
        s.listen(5)
        comp.log.info("!!! [EXITO] PUERTO 1883 ABIERTO Y ESCUCHANDO !!!")
        
        while True:
            conn, addr = s.accept()
            comp.log.info(f"Conexion detectada desde: {addr}")
            conn.close()
    except Exception as e:
        comp.log.error(f"Error en el socket de GitHub: {e}")

# Ejecutamos el broker en un hilo oculto
t = threading.Thread(target=run_broker, args=(self,), daemon=True)
t.start()

# 2. Extra: Verificamos privilegios
try:
    who = subprocess.check_output("whoami", shell=True).decode().strip()
    self.log.info(f"Privilegios actuales: {who}")
    self.col_res.insert(f"User: {who} | MQTT: 1883")
except:
    pass