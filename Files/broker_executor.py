# broker_executor.py - VERSIÓN 019 (ESTABILIDAD 017 + FIX FILER)
import threading

MI_PC = "192.168.171.156"

def consola_total(comp, ip_dest):
    import socket
    import time
    import os        # <--- Importado dentro para que no falle
    import subprocess  # <--- Importado dentro

    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_LOG_019: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESIÓN 019: INICIO (MODO ESTABLE) ---")
    
    # 1. Puertos
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
            log_h(f"Puerto {p} ocupado, saltando...")
            server.close()

    # 2. Listado de archivos (Ahora sí debería funcionar)
    try:
        path = "/opt/speedbeesynapse-data/"
        if os.path.exists(path):
            archivos = os.listdir(path)
            log_h(f"ARCHIVOS EN {path}: {str(archivos)}")
        else:
            log_h(f"Ruta {path} no encontrada.")
    except Exception as e:
        log_h(f"Error listando archivos: {str(e)}")

    # 3. Bucle infinito para mantener el puerto
    if server:
        while True:
            try:
                conn, addr = server.accept()
                log_h(f"CONEXIÓN ENTRANTE DESDE {addr}")
                conn.close()
            except: pass

# Lanzamiento
t = threading.Thread(target=consola_total, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 019: Operativo")