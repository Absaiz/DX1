import threading
import time
import json
import urllib.request

def iniciar_ciclo_colector(contexto):
    # Usamos el logger nativo del componente
    contexto.log.info("--- [BROKER] L1: Entrando en función de ciclo ---")
    
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    API_URL = "http://127.0.0.1:8120/ext_api/v1/components"
    CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q"
    
    def call_api(action):
        contexto.log.info(f"--- [BROKER] L2: API Request -> {action.upper()} ---")
        url = f"{API_URL}/{action}"
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    msg = f"🕒 [{time.strftime('%H:%M:%S')}] CJ {action.upper()} OK"
                    contexto.log.info(f"--- [BROKER] L3: {msg} ---")
                    contexto.col_res.insert(msg)
                else:
                    contexto.log.error(f"--- [BROKER] L3: Error API {r.status} ---")
        except Exception as e:
            contexto.log.error(f"--- [BROKER] L4: Exception en API: {str(e)} ---")

    def loop():
        contexto.log.info("--- [BROKER] L5: Hilo loop iniciado ---")
        while True:
            call_api("start")
            contexto.log.info("--- [BROKER] L6: Espera 10s (ON) ---")
            time.sleep(10)
            
            call_api("stop")
            contexto.log.info("--- [BROKER] L7: Espera 20s (OFF) ---")
            time.sleep(20)

    try:
        contexto.log.info("--- [BROKER] L8: Intentando lanzar thread ---")
        t = threading.Thread(target=loop, daemon=True)
        t.start()
        contexto.log.info("--- [BROKER] L9: Thread lanzado correctamente ---")
    except Exception as e:
        contexto.log.error(f"--- [BROKER] L10: Error al lanzar thread: {str(e)} ---")

# --- ARRANQUE DESDE EL EXEC() ---
try:
    # Capturamos el objeto self inyectado por el Loader
    obj_self = locals().get('self') or globals().get('self')
    
    if obj_self:
        obj_self.log.info("--- [BROKER] Contexto 'self' detectado con éxito ---")
        iniciar_ciclo_colector(obj_self)
    else:
        # Aquí no podemos usar self.log porque no lo hemos encontrado
        print("--- [BROKER] ERROR CRITICO: No se encuentra 'self' en el scope ---")
except Exception as e:
    print(f"--- [BROKER] ERROR EN BOOTSTRAP: {str(e)} ---")