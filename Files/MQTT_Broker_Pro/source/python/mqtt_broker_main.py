from speedbeesynapse.component.base import HiveComponentBase, DataType
import socket
import threading
import time

class HiveComponent(HiveComponentBase):
    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.running = False
        self.clients = []
        self.port = 1883

    def server_loop(self):
        # Creamos un socket TCP estándar
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Escuchamos en todas las interfaces del DX1
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            self.log.info(f"--- [MQTT] Broker activo y escuchando en puerto {self.port} ---")
            
            while self.running:
                self.server_socket.settimeout(1.0)
                try:
                    client_sock, addr = self.server_socket.accept()
                    self.log.info(f"--- [MQTT] Conexión aceptada desde {addr} ---")
                    self.clients.append(client_sock)
                    # Mantenemos el socket vivo para la prueba inicial
                except socket.timeout:
                    continue
                except Exception:
                    break
        except Exception as e:
            self.log.error(f"--- [MQTT] Error Crítico de Socket: {e} ---")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def main(self, param):
        self.col_res = self.out_port1.Column('status', DataType.STRING)
        self.log.info("--- [MQTT] Lanzando Servicio Nativo... ---")
        
        self.running = True
        self.broker_thread = threading.Thread(target=self.server_loop, daemon=True)
        self.broker_thread.start()
        
        self.col_res.insert(f"Broker escuchando en puerto {self.port}")

        # Mantener el componente vivo en Synapse
        for [ts, skip] in self.interval_iteration(60000):
            if not self.running:
                break

    def stop(self):
        self.log.info("--- [MQTT] Apagando Broker ---")
        self.running = False
        for c in self.clients:
            try: c.close()
            except: pass
        if self.server_socket:
            self.server_socket.close()