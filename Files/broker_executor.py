# broker_executor.py en GitHub
import socket
import threading

def start_broker(component):
    component.log.info("--- [SUDO GITHUB] INICIANDO BROKER ---")
    
    # Abrimos el socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        s.bind(('0.0.0.0', 1883))
        s.listen(5)
        component.log.info("--- [SUDO GITHUB] PUERTO 1883 OPEN ---")
        
        while True:
            conn, addr = s.accept()
            component.log.info(f"Conexión desde: {addr}")
            conn.close()
    except Exception as e:
        component.log.error(f"Fallo en el Broker: {e}")

# Ejecutamos el hilo usando el objeto 'self' que nos pasa el cargador
# Como el cargador hace exec(code), 'self' está disponible
t = threading.Thread(target=start_broker, args=(self,), daemon=True)
t.start()

self.col_res.insert("GITHUB_OK: 1883 Listening")