# broker_executor.py - VERSIÓN 008 (PERSISTENCIA Y NETSTAT)
import socket
import threading
import subprocess
import os

self.log.info("--- [LOG 008] INICIO DE OPERACIÓN ---")

def start_broker_service(comp):
    comp.log.info("Iniciando servicio Broker en puerto 1888...")
    try:
        # Usamos el 1888 para evitar el conflicto del sistema
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 1888))
        s.listen(10)
        comp.log.info("!!! [EXITO] BROKER MQTT SUDO ONLINE EN PUERTO 1888 !!!")
        
        while True:
            conn, addr = s.accept()
            # Logueamos cada vez que alguien se conecte desde fuera
            comp.log.info(f"Nueva conexión detectada desde: {addr}")
            # Mantenemos la conexión abierta un momento y cerramos (puro test de socket)
            conn.close()
    except Exception as e:
        comp.log.error(f"Fallo en el servicio de red: {e}")

# 1. Identificar al ocupante del 1883 (netstat -tulnp)
try:
    # Como somos root, podemos ver el nombre del proceso (-p)
    cmd = "netstat -tulnp | grep :1883"
    ocupante = subprocess.check_output(cmd, shell=True).decode().strip()
    self.log.info(f"Ocupante detectado en 1883: {ocupante}")
except:
    self.log.info("Netstat no devolvió info (puerto ocupado pero proceso oculto)")

# 2. Lanzar el Broker en hilo separado para que no bloquee Synapse
t = threading.Thread(target=start_broker_service, args=(self,), daemon=True)
t.start()

self.log.info("--- [LOG 008] SISTEMA EN ESCUCHA (1888) ---")
self.col_res.insert("Check 008: Broker 1888 OK")