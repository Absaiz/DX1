def iniciar_ciclo_colector(contexto):
    # IMPORTANTE: Importamos dentro para evitar el NameError en el entorno exec()
    import threading
    import time
    import json
    import urllib.request

    contexto.log.info("--- [BROKER] L1: Entrando en función de ciclo ---")
    
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
    API_URL = "http://127.0.0.1:8120/ext_api/v1/components"
    CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q"
    
    def call_api(action):
        import json
        import urllib.request
        import time as t_lib
        
        url = f"{API_URL}/{action}"
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    msg = f"🕒 [{t_lib.strftime('%H:%M:%S')}] CJ {action.upper()} OK"
                    contexto.log.info(f"--- [BROKER] L3: {msg} ---")
                    contexto.col_res.insert(msg)
                else:
                    contexto.log.error(f"--- [BROKER] L3: Error API {r.status} ---")
        except Exception as e:
            contexto.log.error(f"--- [BROKER] L4: Exception en API: {str(e)} ---")

    def loop():
        import time as t_loop
        contexto.log.info("--- [BROKER] L5: Hilo loop iniciado ---")
        while True:
            call_api("start")
            contexto.log.info("--- [BROKER] L6: Espera 10s (ON) ---")
            t_loop.sleep(10)
            
            call_api("stop")
            contexto.log.info("--- [BROKER] L7: Espera 20s (OFF) ---")
            t_loop.sleep(20)

    try:
        contexto.log.info("--- [BROKER] L8: Intentando lanzar thread con import local ---")
        t = threading.Thread(target=loop, daemon=True)
        t.start()
        contexto.log.info("--- [BROKER] L9: Thread lanzado correctamente ---")
    except Exception as e:
        # Si esto falla, ahora nos dirá exactamente por qué
        contexto.log.error(f"--- [BROKER] L10: Error final: {str(e)} ---")

# --- ARRANQUE ---
try:
    # Buscamos self en el diccionario de locales inyectado por el Loader
    obj_self = locals().get('self') or globals().get('self')
    if obj_self:
        iniciar_ciclo_colector(obj_self)
except Exception as e:
    print(f"Error bootstrap: {e}")