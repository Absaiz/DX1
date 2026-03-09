from speedbeesynapse.component.base import HiveComponentBase, DataType
import threading
import time
import json
import urllib.request

class HiveComponent(HiveComponentBase):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBY2Nlc3NUb2tlbiIsImV4cCI6MTgwNDYyMjc4NywidG9rZW5fbmFtZSI6Ijk3ZWE1ZjRlLWJiMjAtNDAxMS1iNjQ5LWI1YWZmMTRlZWZhMiJ9.0ClFN7s-kMjLIiH7vNdlzbg9_JuJ-4ZDWSTBnRiroC4"
        self.api_url = "http://127.0.0.1:8120/ext_api/v1/components"
        self.cj_id = "g6MQvWWHTM-lCAjG0WS77Q"

    def call_api(self, action):
        url = f"{self.api_url}/{action}"
        payload = json.dumps({"component_ids": [self.cj_id]}).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='PUT')
        req.add_header('X-hive-api-key', self.token)
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                if r.status == 200:
                    self.log.info(f"--- [PRO] CJ {action.upper()} OK ---")
        except Exception as e:
            self.log.error(f"--- [PRO] Error API: {e} ---")

    def loop(self):
        while not self.stop_event.is_set():
            self.call_api("start")
            if self.stop_event.wait(timeout=10): break
            self.call_api("stop")
            if self.stop_event.wait(timeout=20): break

    def main(self, param):
        self.log.info("--- [PRO] Iniciando Orquestador Empaquetado ---")
        self.stop_event.clear()
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
        
        for [ts, skip] in self.interval_iteration(60000):
            if self.stop_event.is_set(): break

    def stop(self):
        self.stop_event.set()
        self.call_api("stop")