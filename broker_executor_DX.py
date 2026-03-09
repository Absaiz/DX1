import socket
import threading
import time
import json
import urllib.request

def master_broker_dx1(comp):
    # --- CONFIGURACIÓN ---
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    API_URL = "http://127.0.0.1:8120/ext_api/v1/components/status"
    MQTT_PORT = 1883
    EXT_PORT = 9000

    def check_system():
        """Consulta la API local para ver si todo está OK"""
        try:
            req = urllib.request.Request(API_URL)
            req.add_header('X-hive-api-key', TOKEN)
            with urllib.request.urlopen(req) as r:
                data = json.loads(r.read().decode())
                # Buscamos el estado de la VPN
                for c in data['components']:
                    if c['name'] == 'VPN' and c['status'] != 'Running':
                        comp.col_res.insert("⚠️ ALERTA: VPN no está en Running")
        except: pass

    def start_mqtt():
        """Broker MQTT minimalista"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', MQTT_PORT))
            s.listen(20)
            comp.col_res.insert("🧠 MQTT BROKER: Online (1883)")
            while True:
                c, a = s.accept()
                d = c.recv(1024)
                if d and d[0] == 0x10: c.sendall(b'\x20\x02\x00\x00')
                c.close()
        except: pass

    def start_bridge():
        """Puente para acceso desde casa"""
        try:
            b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            b.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            b.bind(('0.0.0.0', EXT_PORT))
            b.listen(20)
            comp.col_res.insert(f"🌉 ACCESO DESDE CASA: {EXT_PORT} -> {MQTT_PORT}")
            while True:
                c, a = b.accept()
                def pipe(src, dst):
                    try:
                        while True:
                            data = src.recv(8192)
                            if not data: break
                            dst.sendall(data)
                    except: pass
                
                try:
                    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target.connect(('127.0.0.1', MQTT_PORT))
                    threading.Thread(target=pipe, args=(c, target), daemon=True).start()
                    threading.Thread(target=pipe, args=(target, c), daemon=True).start()
                except: c.close()
        except: pass

    # Lanzar todo
    threading.Thread(target=start_mqtt, daemon=True).start()
    threading.Thread(target=start_bridge, daemon=True).start()
    
    # Hilo de monitorización cada 5 minutos
    def monitor():
        while True:
            check_system()
            time.sleep(300)
    threading.Thread(target=monitor, daemon=True).start()

master_broker_dx1(self)