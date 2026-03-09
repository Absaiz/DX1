from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import requests

@HiveComponentInfo(uuid='00000000-aaaa-aaaa-aaaa-000000044888', name='System_execute', inports=0, outports=1)
class HiveComponent(HiveComponentBase):
    def main(self, param):
        self.col_res = self.out_port1.Column('status', DataType.STRING)
        URL = "https://raw.githubusercontent.com/Absaiz/DX1/main/Files/broker_executor.py"
        
        # 1. Limpieza preventiva
        script_content = None 
        self.log.info("--- [LOADER] Iniciando descarga limpia de GitHub ---")

        try:
            # Añadimos un pequeño truco en la URL (?nocache) para evitar proxys intermedios
            import time
            r = requests.get(f"{URL}?t={int(time.time())}", timeout=5)
            
            if r.status_code == 200:
                script_content = r.text
                self.log.info(f"--- [LOADER] Descarga OK ({len(script_content)} bytes). Ejecutando... ---")
                
                # 2. Ejecución con un diccionario de locales limpio
                # Al pasar un dict nuevo {}, evitamos que herede basura de ejecuciones anteriores
                exec(script_content, globals(), {"self": self})
            else:
                self.log.error(f"--- [LOADER] Error GitHub: Status {r.status_code} ---")
                
        except Exception as e:
            self.log.error(f"--- [LOADER] Sync error: {e} ---")

        # El bucle mantiene el componente vivo
        for [ts, skip] in self.interval_iteration(60000):
            pass