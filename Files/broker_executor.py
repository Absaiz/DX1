# broker_executor.py - VERSIÓN 022 (MQTT FOCUS)
import threading
import socket
import time

MI_PC = "192.168.171.156"

def mqtt_focus(comp, ip_dest):
    def log_h(msg):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip_dest, 23))
            s.sendall(f"DX1_MQTT: {msg}\n".encode())
            s.close()
        except: pass

    log_h("--- SESION 022: FOCO EN T  RÁFICO    MQTT ---")
    
    # Intentamos abrir el 18833 (MQTT estándar alternativo)
    # Así no chocamos con el 1883 de Omron y es un puerto 'oficial'
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', 18833))
        server.listen(5)
        log_h("EXITO: Broker Sudo escuchando en 18833")
        
        while True:
            conn, addr = server.accept()
            log_h(f"¡CONEXIÓN MQTT DETECTADA! Cliente: {addr}")
            
            # Simulamos un mensaje MQTT simple de conexión aceptada (CONNACK)
            # 20 02 00 00 -> Protocolo MQTT conexión aceptada
            conn.send(b'\x20\x02\x00\x00')
            conn.close()
            log_h("Respuesta CONNACK enviada y sesión cerrada (Test OK)")
            
    except Exception as e:
        log_h(f"Fallo en puerto 18833: {str(e)}")

# Lanzamiento
t = threading.Thread(target=mqtt_focus, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 022: MQTT 18833")