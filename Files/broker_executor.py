# broker_executor.py - VERSIÓN 013 (ELIMINANDO SCOPE ERRORS)
import threading
import socket

# Definimos la IP de tu PC fuera para que sea fácil de cambiar
MI_PC = "192.168.171.156"

self.log.info("--- [LOG 013] BLINDANDO FUNCIONES ---")

def servidor_total(comp, ip_destino):
    import socket
    import time

    def log_externo(texto):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_destino, 23))
            s.sendall(f"DX1_LOG: {texto}\n".encode())
            s.close()
        except:
            pass

    log_externo("INICIANDO HILO DE RED 013")
    
    try:
        # Intentamos abrir el puerto 1888
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 1888))
        server.listen(5)
        log_externo("EXITO: Puerto 1888 abierto")
        comp.log.info("!!! PUERTO 1888 ONLINE !!!")
        
        while True:
            conn, addr = server.accept()
            log_externo(f"CONEXION ENTRANTE DESDE {addr}")
            conn.close()
    except Exception as e:
        msg_err = f"ERROR CRITICO: {str(e)}"
        comp.log.error(msg_err)
        log_externo(msg_err)

# Lanzamos el hilo y le pasamos el componente 'self' y la IP de tu PC
t = threading.Thread(target=servidor_total, args=(self, MI_PC), daemon=True)
t.start()

self.col_res.insert("LOG 013: Blindaje OK")