import time

def orquestador_cj_api_debug(comp):
    comp.col_res.insert("🔍 [STEP 1]: Entrando en la función principal...")
    
    try:
        import threading
        import json
        import urllib.request
        import time as t_lib
        comp.col_res.insert("✅ [STEP 2]: Imports realizados con éxito.")
    except Exception as e:
        comp.col_res.insert(f"❌ [ERROR]: Fallo en Imports: {e}")
        return

    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    API_BASE = "http://127.0.0.1:8120/ext_api/v1/components"
    CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q" 
    
    def call_api(action):
        url = f"{API_BASE}/{action}"
        comp.col_res.insert(f"🌐 [API]: Intentando {action} en {url}")
        
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                comp.col_res.insert(f"📡 [RESPUESTA]: Código HTTP {r.status}")
                if r.status == 200:
                    icon = "🟢 START" if action == "start" else "🔴 STOP"
                    comp.col_res.insert(f"🕒 [{t_lib.strftime('%H:%M:%S')}] CJ -> {icon}")
        except Exception as e:
            comp.col_res.insert(f"⚠️ [ERROR API]: {e}")

    def loop_secuencial():
        comp.col_res.insert("🔄 [THREAD]: Bucle de control iniciado.")
        try:
            while True:
                call_api("start")
                comp.col_res.insert("⏳ [ESPERA]: 10s ON...")
                t_lib.sleep(10)
                
                call_api("stop")
                comp.col_res.insert("⏳ [ESPERA]: 20s OFF...")
                t_lib.sleep(20)
        except Exception as e:
            comp.col_res.insert(f"❌ [CRÍTICO THREAD]: El bucle ha muerto: {e}")

    try:
        comp.col_res.insert("🧵 [STEP 3]: Intentando lanzar el hilo (threading.Thread)...")
        hilo = threading.Thread(target=loop_secuencial, daemon=True)
        hilo.start()
        comp.col_res.insert("🚀 [STEP 4]: Hilo lanzado correctamente.")
    except Exception as e:
        comp.col_res.insert(f"❌ [ERROR]: No se pudo lanzar el hilo: {e}")

# Ejecución
orquestador_cj_api_debug(self)