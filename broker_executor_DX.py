from speedbeesynapse.component.base import HiveComponentBase, HiveComponentInfo, DataType
import requests
import os

@HiveComponentInfo(uuid='00000000-aaaa-aaaa-aaaa-000000000777', name='DX1_GitHub_Loader', inports=0, outports=1)
class HiveComponent(HiveComponentBase):
    def main(self, param):
        self.col_res = self.out_port1.Column('status', DataType.STRING)
        
        # URL de tu script real en GitHub (formato RAW)
        # Asegúrate de que la URL termine en el archivo .py directamente
        GITHUB_RAW_URL = "https://raw.githubusercontent.com/Absaiz/DX1/main/Files/broker_executor.py"
        
        self.log.info(f"--- Iniciando Bootstrap desde GitHub ---")
        
        try:
            # 1. Descargamos el código dinámico
            response = requests.get(GITHUB_RAW_URL, timeout=10)
            if response.status_code == 200:
                code = response.text
                self.log.info("Código descargado correctamente. Ejecutando...")
                
                # 2. Ejecutamos el código descargado en el contexto del componente
                # Esto permite que el script de GitHub use self.log, self.col_res, etc.
                exec(code, globals(), locals())
                
                self.col_res.insert("Loader: Script GitHub Ejecutado")
            else:
                self.log.error(f"Error al descargar: Status {response.status_code}")
        except Exception as e:
            self.log.error(f"Fallo crítico en Bootstrap: {e}")

        # Mantener el componente vivo
        for [ts, skip] in self.interval_iteration(60000):
            pass