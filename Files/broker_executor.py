# broker_executor.py - VERSIÓN 015 (LIMPIEZA Y AUDITORÍA)
import threading
import socket
import subprocess
import os
import time

MI_PC = "192.168.171.156"

def auditoria_sistema(comp, ip_destino):
    def log_h(texto):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_destino, 23))
            s.sendall(f"DX1_LOG_015: {texto}\n".encode())
            s.close()
        except: pass

    # --- PASO 0: LIMPIEZA DE RESIDUOS ---
    log_h("Iniciando limpieza de procesos previos...")
    try:
        # Matamos cualquier proceso que esté escuchando en el 1888 para liberar el puerto
        # (fuser -k enviaría señal SIGKILL a lo que use ese puerto)
        subprocess.call("fuser -k 1888/tcp", shell=True)
        time.sleep(1) # Esperamos a que el SO libere el recurso
    except:
        pass

    log_h("--- INICIO AUDITORÍA 015 ---")
    
    # 1. ¿Quién ocupa el 1883? (Netstat detallado)
    try:
        net = subprocess.check_output("netstat -plnt", shell=True).decode()
        log_h(f"RED ACTUAL:\n{net}")
    except:
        log_h("Fallo al ejecutar netstat")

    # 2. Exploración de archivos en /opt/speedbeesynapse-data/
    try:
        path = "/opt/speedbeesynapse-data/"
        if os.path.exists(path):
            archivos = os.listdir(path)
            log_h(f"ARCHIVOS EN {path}: {archivos}")
            
            # Si vemos el db, miramos su tamaño para ver si tiene chicha
            if 'sdts.db' in archivos:
                size = os.path.getsize(path + 'sdts.db')
                log_h(f"DATABASE DETECTADA: sdts.db ({size} bytes)")
        else:
            log_h(f"La ruta {path} no existe en este contexto.")
    except Exception as e:
        log_h(f"Error accediendo a data: {e}")

    # 3. Levantar el puerto 1888 limpio
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 1888))
        server.listen(5)
        log_h("EXITO: Puerto 1888 re-abierto y limpio.")
        while True:
            conn, addr = server.accept()
            log_h(f"CONEXION EN 1888 DESDE: {addr}")
            conn.close()
    except Exception as e:
        log_h(f"Error Socket 1888: {e}")

# Ejecución
t = threading.Thread(target=auditoria_sistema, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 015: Clean & Audit")