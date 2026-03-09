import threading
import time
import json
import urllib.request

def orquestador_cj_api(comp):
    # --- CONFIGURACIÓN ---
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    # Probamos con 8120 que es el que nos dio el 200 OK antes
    API_BASE = "http://127.0.0.1:8120/ext_api/v1/components"
    CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q" 
    
    T_ON = 10
    T_OFF = 20

    def call_api(action):
        url = f"{API_BASE}/{action}"
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    icon = "🟢 START" if action == "start" else "🔴 STOP"
                    comp.col_res.insert(f"[{time.strftime('%H:%M:%S')}] CJ -> {icon}")
                else:
                    comp.col_res.insert(f"❌ API {action} Status: {r.status}")
        except Exception as e:
            comp.col_res.insert(f"⚠️ Error en llamada API: {e}")

    def loop_secuencial():
        comp.col_res.insert("🎮 SECUENCIADOR ON: 10s / 20s")
        while True:
            # ENCENDER CJ
            call_api("start")
            time.sleep(T_ON)
            
            # APAGAR CJ
            call_api("stop")
            time.sleep(T_OFF)

    # Ahora sí, threading está definido arriba
    t = threading.Thread(target=loop_secuencial, daemon=True)
    t.start()

# Ejecución
orquestador_cj_api(self)