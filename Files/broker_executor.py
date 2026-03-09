# broker_executor.py - VERSIÓN 011 (LOGS A HÉRCULES)
import socket
import threading
import time
import subprocess

# Configuración de tu PC
PC_IP = "192.168.171.156"
PC_PORT = 23

def send_to_hercules(message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((PC_IP, PC_PORT))
        s.sendall(f"[DX1-LOG] {message}\n".encode())
        s.close()
    except:
        pass # Si el Hércules no escucha, no bloqueamos el script

self.log.info("--- [LOG 011] ENVIANDO TELEMETRÍA A HÉRCULES ---")
send_to_hercules("CONEXIÓN ESTABLECIDA CON EL DX1")

def start_broker_service(comp):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 1888))
        s.listen(5)
        send_to_hercules("PUERTO 1888 ABIERTO EN DX1")
        
        while True:
            conn, addr = s.accept()
            msg = f"CONEXIÓN ENTRANTE DESDE: {addr}"
            send_to_hercules(msg)
            comp.log.info(msg)
            conn.close()
    except Exception as e:
        send_to_hercules(f"ERROR EN BROKER: {e}")

# Lanzamos el broker y enviamos diagnóstico de red
try:
    ifaces = subprocess.check_output("ip addr | grep eth", shell=True).decode()
    send_to_hercules(f"INTERFACES DX1: {ifaces.strip()}")
except:
    send_to_hercules("No se pudo obtener IP local")

t = threading.Thread(target=start_broker_service, args=(self,), daemon=True)
t.start()

self.col_res.insert("LOG 011: Enviando a Hercules")