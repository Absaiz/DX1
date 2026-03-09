from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import threading
import time
import requests
import json

@HiveComponentInfo(uuid='00000000-aaaa-aaaa-aaaa-000567654611', name='Orquestador_Cj', inports=0, outports=1)
class HiveComponent(HiveComponentBase):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        # Configuración de la API local
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
        self.api_base = "http://127.0.0.1:8120/ext_api/v1/components"
        self.target_id = "g6MQvWWHTM-lCAjG0WS77Q" # ID del componente 'cj'
        self.headers = {
            "X-hive-api-key": self.token,
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    def control_cj(self, action):
        """Envía START o STOP al componente 'cj' vía WebAPI"""
        url = f"{self.api_base}/{action}"
        payload = {"component_ids": [self.target_id]}
        try:
            # Usamos PUT según la documentación de Synapse para start/stop
            response = requests.put(url, headers=self.headers, data=json.dumps(payload), timeout=5)
            if response.status_code == 200:
                msg = "🚀 CJ INICIADO" if action == "start" else "🛑 CJ DETENIDO"
                self.col_res.insert(f"[{time.strftime('%H:%M:%S')}] {msg}")
                self.outports[0].send(action.upper())
            else:
                self.col_res.insert(f"❌ Error API ({action}): {response.status_code} - {response.text}")
        except Exception as e:
            self.col_res.insert(f"⚠️ Fallo de conexión API: {e}")

    def main(self, param):
        self.col_res.insert(f"🎮 Iniciando Control Secuencial sobre 'cj' (10s/20s)")
        self.stop_event.clear()

        while not self.stop_event.is_set():
            # Fase ON: Arrancar componente 'cj' durante 10 segundos
            self.control_cj("start")
            if self.stop_event.wait(timeout=10): 
                break
            
            # Fase OFF: Parar componente 'cj' durante 20 segundos
            self.control_cj("stop")
            if self.stop_event.wait(timeout=20): 
                break

    def stop(self):
        """Al parar este orquestador, nos aseguramos de parar el PLC 'cj'"""
        self.stop_event.set()
        self.control_cj("stop")
        self.col_res.insert("⏹️ Orquestador finalizado.")