from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import urllib.request
import json
import time

@HiveComponentInfo(uuid='00000000-aaaa-aaaa-aaaa-123567654611', name='Orquestador_Cj', inports=0, outports=1)
class HiveComponent(HiveComponentBase):
    
    def call_api(self, action):
        # Mantenemos tus variables de configuración
        TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
        API_URL = "http://127.0.0.1:8120/ext_api/v1/components"
        CJ_ID = "g6MQvWWHTM-lCAjG0WS77Q"
        
        url = f"{API_URL}/{action}"
        payload = json.dumps({"component_ids": [CJ_ID]}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', TOKEN)
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    msg = f"🕒 [{time.strftime('%H:%M:%S')}] CJ {action.upper()} OK"
                    self.log.info(f"--- [BROKER] L3: {msg} ---")
                    self.col_res.insert(msg)
                else:
                    self.log.error(f"--- [BROKER] L3: Error API {r.status} ---")
        except Exception as e:
            self.log.error(f"--- [BROKER] L4: Exception en API: {str(e)} ---")

    def main(self, param):
        # 1. Inicializamos la columna de resultados (importante en componentes oficiales)
        self.col_res = self.out_port1.Column('status', DataType.STRING)
        self.log.info("--- [BROKER] L1: Entrando en función de ciclo ---")

        # 2. Como Synapse a veces filtra 'threading', usamos su propio bucle principal
        # Esto hace exactamente lo mismo que tu loop pero de forma nativa.
        
        estado_actual = None
        # Tiempo de referencia para los ciclos
        start_loop = time.time()

        # El componente ejecutará este bucle cada 1 segundo (1000ms)
        for [ts, skip] in self.interval_iteration(1000):
            ahora = time.time()
            # Ciclo total de 30 segundos (10 ON + 20 OFF)
            posicion_ciclo = (ahora - start_loop) % 30

            if posicion_ciclo < 10:
                if estado_actual != "START":
                    self.log.info("--- [BROKER] L6: Iniciando 10s (ON) ---")
                    self.call_api("start")
                    estado_actual = "START"
            else:
                if estado_actual != "STOP":
                    self.log.info("--- [BROKER] L7: Iniciando 20s (OFF) ---")
                    self.call_api("stop")
                    estado_actual = "STOP"

    def stop(self):
        # Por seguridad, si el componente se para, mandamos un STOP al PLC
        self.log.info("--- [BROKER] Stop de seguridad ---")
        self.call_api("stop")