# broker_executor.py - VERSIÓN 007 (OCUPACIÓN DE PUERTOS)
import socket
import threading
import subprocess

self.log.info("--- [SUDO] ANALIZANDO COMPETENCIA ---")

# 1. ¿Quién ocupa el 1883? (Vamos a lanzar un netstat o lsof)
try:
    # Intentamos ver qué proceso tiene el puerto 1883
    cmd = "netstat -tulnp | grep :1883"
    proceso = subprocess.check_output(cmd, shell=True).decode().strip()
    self.log.info(f"Ocupante del 1883: {proceso}")
except:
    self.log.info("No se pudo identificar al ocupante del 1883 (netstat no disponible?)")

# 2. Abrimos nuestro Broker en el 1888 (Este no fallará)
def run_mqtt_1888(comp):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 1888))
        s.listen(10)
        comp.log.info("!!! [SUCCESS] BROKER SUDO ONLINE EN PUERTO 1888 !!!")
        
        while True:
            c, a = s.accept()
            comp.log.info(f"Conexión MQTT Sudo desde: {addr}")
            c.close()
    except Exception as e:
        comp.log.error(f"Fallo en el puerto 1888: {e}")

# Lanzamos el broker en el 1888
t = threading.Thread(target=run_mqtt_1888, args=(self,), daemon=True)
t.start()

self.col_res.insert("Escuchando en 1888")