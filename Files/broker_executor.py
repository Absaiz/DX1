# broker_executor.py - VERSIÓN 009 (CONTROL DE PERSISTENCIA)
import socket
import threading
import time
import subprocess

self.log.info("--- [LOG 009] INICIO DE VERIFICACIÓN DE ESTADO ---")

def monitor_broker(comp, server_socket):
    """ Función que verifica si el socket sigue vivo cada 10 segundos """
    while True:
        try:
            # Intentamos ver si el socket del sistema sigue ahí
            status = subprocess.check_output("netstat -tulnp | grep :1888", shell=True).decode()
            comp.log.info(f"[HEARTBEAT] Puerto 1888 activo: {status.strip()}")
        except:
            comp.log.error("[ALERTA] El puerto 1888 ha desaparecido del sistema")
        time.sleep(10)

def start_broker_service(comp):
    comp.log.info("Configurando Socket en 1888...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 1888))
        s.listen(10)
        comp.log.info("!!! [LOG 009] PUERTO 1888 ABIERTO Y LISTO !!!")
        
        # Lanzamos un hilo de monitorización para ver si se cae
        monitor_thread = threading.Thread(target=monitor_broker, args=(comp, s), daemon=True)
        monitor_thread.start()

        while True:
            conn, addr = s.accept()
            comp.log.info(f"--- [CONEXIÓN REAL] Cliente conectado desde: {addr} ---")
            conn.send(b"Hola desde el DX1 Sudo Broker\n")
            conn.close()
    except Exception as e:
        comp.log.error(f"Error crítico en el servicio: {e}")

# Ejecución del hilo principal
t = threading.Thread(target=start_broker_service, args=(self,), daemon=True)
t.start()

# 3. Verificación de Firewall (IPTABLES)
try:
    # Vamos a ver si hay reglas que bloqueen puertos nuevos
    rules = subprocess.check_output("iptables -L -n | grep 1888", shell=True).decode()
    self.log.info(f"Reglas de Firewall para 1888: {rules if rules else 'Ninguna (Abierto)'}")
except:
    self.log.info("No se pudo consultar iptables (¿Permisos o comando ausente?)")

self.col_res.insert("LOG 009: Running 1888")