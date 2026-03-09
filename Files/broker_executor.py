# broker_executor.py - VERSIÓN 023 (BACK TO STABLE)
import threading
import socket
import os

MI_PC = "192.168.171.156"

def consola_total(comp, ip_dest):
    import socket
    import os
    import time
    
    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_LOG_023: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESION 023: RECUPERANDO CANAL ESTABLE ---")
    
    # 1. Buscamos puerto libre empezando desde el 1894 para evitar zombis
    server = None
    for p in range(1894, 1900):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', p))
            server.listen(1)
            log_h(f"CONECTADO EN PUERTO {p}")
            break
        except:
            if server: server.close()

    # 2. Solo listado de archivos básico (sin abrir nada)
    try:
        path = "/opt/speedbeesynapse-data/"
        if os.path.exists(path):
            files = os.listdir(path)
            log_h(f"FILES: {str(files)}")
        else:
            log_h("Ruta DATA no encontrada")
    except Exception as e:
        log_h(f"Error: {str(e)}")

    # 3. Mantener el hilo vivo
    if server:
        while True:
            try:
                conn, addr = server.accept()
                log_h(f"TEST CONEXION DESDE {addr}")
                conn.close()
            except: pass

# Lanzamiento limpio
t = threading.Thread(target=consola_total, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 023: Estable")