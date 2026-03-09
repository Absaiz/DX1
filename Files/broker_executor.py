import socket
import threading
import time
import json
import urllib.request

def orquestador_cj_api(comp):
    # --- CONFIGURACIÓN ---
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    API_BASE = "http://127.0.0.1:8120/ext_api/v1/components"
    CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q" # El ID del componente 'cj'
    
    T_ON = 10
    T_OFF = 20

    def call_api(action):
        """ Envía PUT /start o /stop al componente 'cj' """
        url = f"{API_BASE}/{action}"
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    status_icon = "🟢 RUN" if action == "start" else "🔴 STOP"
                    comp.col_res.insert(f"[{time.strftime('%H:%M:%S')}] CJ -> {status_icon}")
                else:
                    comp.col_res.insert(f"❌ Error API {action}: {r.status}")
        except Exception as e:
            comp.col_res.insert(f"⚠️ Fallo conexión API: {e}")

    def loop_secuencial():
        comp.col_res.insert("🎮 SECUENCIADOR ACTIVO: 10s ON / 20s OFF")
        while True:
            # ENCENDER
            call_api("start")
            time.sleep(T_ON)
            
            # APAGAR
            call_api("stop")
            time.sleep(T_OFF)

    # Lanzamos en un hilo para que el broker_executor no se quede bloqueado
    t = threading.Thread(target=loop_secuencial, daemon=True)
    t.start()

# Ejecución
orquestador_cj_api(self)