import socket
import threading

def modo_broker_central(comp):
    MQTT_PORT = 1883
    # Usaremos el 9000 como entrada desde Tailscale para saltar el bloqueo
    EXTERNAL_PORT = 9000 
    
    def start_broker():
        try:
            # Socket del Broker
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', MQTT_PORT))
            s.listen(15)
            comp.col_res.insert(f"🧠 BROKER INTERNO: Activo en {MQTT_PORT}")
            
            while True:
                client, addr = s.accept()
                def handle_mqtt(c):
                    try:
                        data = c.recv(1024)
                        if data and data[0] == 0x10: # CONNECT
                            c.sendall(b'\x20\x02\x00\x00') # CONNACK
                            # Aquí se mantendría la sesión activa para PUB/SUB
                    except: pass
                threading.Thread(target=handle_mqtt, args=(client,), daemon=True).start()
        except Exception as e:
            comp.col_res.insert(f"❌ Error Broker: {e}")

    def start_bridge():
        # Este puente permite que tu Ryzen conecte al 9000 y llegue al 1883 interno
        try:
            b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            b.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            b.bind(('0.0.0.0', EXTERNAL_PORT))
            b.listen(15)
            comp.col_res.insert(f"🌉 ACCESO MQTT: 100.117.214.15:{EXTERNAL_PORT}")
            
            while True:
                c, a = b.accept()
                def pipe(src, dst):
                    try:
                        while True:
                            d = src.recv(4096)
                            if not d: break
                            dst.sendall(d)
                    except: pass
                
                try:
                    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target.connect(('127.0.0.1', MQTT_PORT))
                    threading.Thread(target=pipe, args=(c, target), daemon=True).start()
                    threading.Thread(target=pipe, args=(target, c), daemon=True).start()
                except: c.close()
        except Exception as e:
            comp.col_res.insert(f"❌ Error Bridge: {e}")

    threading.Thread(target=start_broker, daemon=True).start()
    threading.Thread(target=start_bridge, daemon=True).start()

modo_broker_central(self)