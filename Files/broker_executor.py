# broker_executor.py - VERSIÓN 012 (FIX SCOPE & HERCULES)
import threading
import time

# Forzamos el log local para saber que hemos arrancado
self.log.info("--- [LOG 012] REPARANDO SCOPE Y CONECTANDO A HÉRCULES ---")

def send_hercules(msg):
    import socket # Import local para evitar 'not defined'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("192.168.171.156", 23))
        s.sendall(f"DX1_SUDO: {msg}\n".encode())
        s.close()
    except:
        pass

def broker_loop(comp):
    import socket # Import local vital
    comp.log.info("Iniciando bucle de red en 1888...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 1888))
        s.listen(5)
        send_hercules("!!! PUERTO 1888 ABIERTO EN DX1 !!!")
        
        while True:
            conn, addr = s.accept()
            msg = f"CONEXION DESDE: {addr}"
            send_hercules(msg)
            comp.log.info(msg)
            conn.close()
    except Exception as e:
        error_msg = f"ERROR BROKER: {str(e)}"
        comp.log.error(error_msg)
        send_hercules(error_msg)

# Lanzar el hilo pasando el componente (self)
t = threading.Thread(target=broker_loop, args=(self,), daemon=True)
t.start()

send_hercules("SISTEMA 012 ONLINE - ESPERANDO CONEXIONES")
self.col_res.insert("LOG 012: Hercules 23")