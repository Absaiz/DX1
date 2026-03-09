import threading
import time
import json
import urllib.request

def iniciar_ciclo_colector(contexto):
    # --- CONFIGURACIÓN ---
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    API_URL = "http://127.0.0.1:8120/ext_api/v1/components"
    CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q"
    
    contexto.col_res.insert("🚀 [BROKER] Lógica iniciada correctamente")

    def call_api(action):
        url = f"{API_URL}/{action}"
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    icon = "🟢" if action == "start" else "🔴"
                    contexto.col_res.insert(f"🕒 [{time.strftime('%H:%M:%S')}] {icon} CJ {action.upper()}")
        except Exception as e:
            contexto.col_res.insert(f"⚠️ Error API: {e}")

    def loop():
        while True:
            call_api("start")
            time.sleep(10)
            call_api("stop")
            time.sleep(20)

    # Lanzar hilo independiente
    threading.Thread(target=loop, daemon=True).start()

# --- VALIDACIÓN DE CONTEXTO ---
# Buscamos 'self' en el scope que genera tu Loader
try:
    # Intentamos obtener 'self' de locals() que es donde lo inyecta tu exec()
    obj_self = locals().get('self', globals().get('self'))
    if obj_self:
        iniciar_ciclo_colector(obj_self)
    else:
        print("No se detectó 'self' en el contexto del exec")
except Exception as e:
    print(f"Error al arrancar lógica: {e}")