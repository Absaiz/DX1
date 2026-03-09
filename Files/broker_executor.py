# broker_executor.py - VERSIÓN 020 (ADN 017 - VOLVIENDO A LO SEGURO)
import threading
import socket
import os
import time

MI_PC = "192.168.171.156"

def consola_total(comp, ip_dest):
    import socket
    import os  # Cargado aquí dentro para que no diga que no existe
    
    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_LOG_020: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESION 020: REGRESO AL CODIGO 017 ---")
    
    # 1. Puertos (Intentamos el 1889 directo para no perder tiempo)
    server = None
    for p in [1889, 1890, 1891, 1892]:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', p))
            server.listen(1)
            log_h(f"PUERTO {p} ABIERTO")
            break
        except:
            server.close()

    # 2. Listado de archivos (Simplificado al máximo)
    try:
        path = "/opt/speedbeesynapse-data/"
        if os.path.exists(path):
            files = os.listdir(path)
            log_h(f"DATA_FILES: {str(files)}")
        else:
            log_h("Ruta no encontrada")
    except Exception as e:
        log_h(f"Error archivos: {str(e)}")

    # 3. Bucle de escucha
    if server:
        while True:
            try:
                conn, addr = server.accept()
                log_h(f"ENTRADA EN PUERTO DESDE {addr}")
                conn.close()
            except: pass

# Lanzamiento igual que en la 017
t = threading.Thread(target=consola_total, args=(self, MI_PC), daemon=True)
t.start()

self.col_res.insert("LOG 020: DNA 017")