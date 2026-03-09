# broker_executor.py - VERSIÓN 016 (HÉRCULES CONSOLE)
import threading
import socket
import subprocess
import os
import sys

MI_PC = "192.168.171.156"
PORT_H = 23

def sudo_console(comp, ip_dest):
    import socket
    import time

    def log_h(msg):
        """ Envía cualquier texto al Hércules inmediatamente """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, PORT_H))
            s.sendall(f"DX1_LOG_016: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESIÓN 016 INICIADA (MODO CONSOLA TOTAL) ---")
    
    # 1. Diagnóstico de Puertos (Netstat)
    try:
        log_h("Escaneando puertos activos en el sistema...")
        net_data = subprocess.check_output("netstat -plnt", shell=True).decode()
        log_h(f"ESTADO DE RED:\n{net_data}")
    except Exception as e:
        log_h(f"Error en netstat: {e}")

    # 2. Listado de Archivos Sensibles
    try:
        path = "/opt/speedbeesynapse-data/"
        log_h(f"Explorando directorio: {path}")
        if os.path.exists(path):
            files = os.listdir(path)
            log_h(f"CONTENIDO DE DATA: {str(files)}")
            # Si existe la DB, buscamos su ruta real
            db_path = os.path.join(path, "sdts.db")
            if os.path.exists(db_path):
                log_h(f"DB ENCONTRADA: {db_path} ({os.path.getsize(db_path)} bytes)")
        else:
            log_h("Ruta /opt/speedbeesynapse-data/ no encontrada.")
    except Exception as e:
        log_h(f"Error explorando archivos: {e}")

    # 3. Servidor de Eco (Puerto 1889 para evitar conflicto con el 1888 zombi)
    try:
        test_port = 1889 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', test_port))
        server.listen(1)
        log_h(f"EXITO: Escuchando ahora en puerto {test_port} (el 1888 sigue ocupado por el zombi 012)")
        
        while True:
            c, a = server.accept()
            log_h(f"CONEXIÓN ENTRANTE DESDE {a}")
            c.send(b"Hola desde la consola 016\n")
            c.close()
    except Exception as e:
        log_h(f"Error en Servidor 1889: {e}")

# Arrancamos el hilo
t = threading.Thread(target=sudo_console, args=(self, MI_PC), daemon=True)
t.start()

self.col_res.insert("LOG 016: Consola Hércules OK")