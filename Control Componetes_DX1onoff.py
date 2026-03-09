from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import urllib.request
import json
import time

@HiveComponentInfo(uuid='00000000-aaaa-aaaa-aaaa-123567654611', name='Orquestador_Cj', inports=0, outports=1)
class HiveComponent(HiveComponentBase):

    def call_api(self, action):
        """Función de control vía API interna"""
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
                    self.log.info(f"--- [BROKER] {msg} ---")
                    self.col_res.insert(msg)
        except Exception as e:
            self.log.error(f"--- [BROKER] Error API: {str(e)} ---")

    def main(self, param):
        # Inicialización de la columna en la interfaz
        self.col_res = self.out_port1.Column('status', DataType.STRING)
        self.log.info("--- [BROKER] L1: Orquestador Nativo Iniciado ---")

        # Variables de control de tiempo
        ultimo_cambio = 0
        estado_actual = "OFF" # Empezamos asumiendo que está parado
        
        # El loop nativo de Synapse (revisamos cada 1 segundo)
        for [ts, skip] in self.interval_iteration(1000):
            ahora = time.time()
            
            # Lógica de conmutación
            if estado_actual == "OFF":
                # Si han pasado 20 segundos desde el último cambio, encendemos
                if (ahora - ultimo_cambio) >= 20:
                    self.log.info("--- [BROKER] L6: Han pasado 20s. Encendiendo (START) ---")
                    self.call_api("start")
                    estado_actual = "ON"
                    ultimo_cambio = ahora
            
            elif estado_actual == "ON":
                # Si han pasado 10 segundos desde el último cambio, apagamos
                if (ahora - ultimo_cambio) >= 10:
                    self.log.info("--- [BROKER] L7: Han pasado 10s. Apagando (STOP) ---")
                    self.call_api("stop")
                    estado_actual = "OFF"
                    ultimo_cambio = ahora

    def stop(self):
        # Aseguramos que el PLC se apaga si paramos el componente
        self.log.info("--- [BROKER] Stop de seguridad ejecutado ---")
        try:
            self.call_api("stop")
        except:
            pass