# broker_executor.py - VERSIÓN 021 (DB INSPECTOR)
import threading
import socket
import os

MI_PC = "192.168.171.156"

def consola_total(comp, ip_dest):
    import socket
    import os
    
    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_LOG_021: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESION 021: INSPECCION DE BASE DE DATOS ---")
    
    # 1. Saltamos al puerto 1893 para estar limpios
    server = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 1893))
        server.listen(1)
        log_h("PUERTO 1893 ABIERTO")
    except:
        log_h("Fallo al abrir puerto 1893, reintenta.")

    # 2. Análisis de sdts.db
    try:
        db_path = "/opt/speedbeesynapse-data/sdts.db"
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            log_h(f"TAMAÑO DE DB: {size} bytes")
            
            # Intentamos leer los primeros 100 bytes (la cabecera)
            with open(db_path, "rb") as f:
                header = f.read(100)
                # Si empieza por 'SQLite format 3', es una base de datos estándar
                log_h(f"CABECERA DB: {header[:20]}")
        else:
            log_h("No encuentro el archivo sdts.db")
    except Exception as e:
        log_h(f"Error leyendo DB: {str(e)}")

    if server:
        while True:
            try:
                conn, addr = server.accept()
                conn.close()
            except: pass

t = threading.Thread(target=consola_total, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 021: DB Inspect")