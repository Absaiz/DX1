from speedbeesynapse.component.base import HiveComponentBase, DataType

class HiveComponent(HiveComponentBase):
    def __init__(self):
        super().__init__()

    def main(self, param):
        # Creamos una columna de salida para ver algo en el monitor
        self.col_status = self.out_port1.Column('debug', DataType.STRING)
        self.log.info("--- [RESCATE] Componente Hola Mundo cargado ---")
        
        # Bucle mínimo para que el componente esté en 'Run' sin consumir CPU
        for [ts, skip] in self.interval_iteration(5000):
            self.col_status.insert("Sistema Sano")

    def stop(self):
        self.log.info("--- [RESCATE] Deteniendo componente ---")