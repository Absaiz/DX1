import socket
import threading

def start_broker(comp):
    try:
        # Usamos el puerto 23 porque sabemos que el firewall lo permite
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 23))
        s.listen(5)
        # Log para saber que hemos "secuestrado" el puerto
        comp.col_res.insert("MQTT_BROKER: Activo en Puerto 23")
        
        while True:
            conn, addr = s.accept()
            # Si recibimos algo, respondemos como un Broker MQTT
            data = conn.recv(1024)
            if data:
                # Enviamos CONNACK (Conexión aceptada)
                conn.send(b'\x20\x02\x00\x00')
            conn.close()
    except Exception as e:
        comp.col_res.insert(f"Error Broker: {str(e)}")

# Lanzamos el hilo para que no bloquee el DX1
t = threading.Thread(target=start_broker, args=(self,), daemon=True)
t.start()