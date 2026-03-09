# broker_executor.py - VERSIÓN 005 (DIAGNÓSTICO POR ETAPAS)
import os
import sys

self.log.info("--- [DEBUG 005] INICIANDO SECUENCIA ---")

# Etapa 1: Verificar Capacidad de Ejecución de Comandos
try:
    import subprocess
    res = subprocess.check_output("id", shell=True).decode().strip()
    self.log.info(f"ID de Proceso: {res}")
except Exception as e:
    self.log.error(f"Etapa 1 (Subprocess) falló: {e}")

# Etapa 2: Verificar Red (Socket)
try:
    import socket
    self.log.info("Librería 'socket' cargada correctamente.")
    # Test de puerto rápido (no bloqueante)
    test_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    test_s.settimeout(1)
    self.log.info("Socket creado para test.")
    test_s.close()
except Exception as e:
    self.log.error(f"Etapa 2 (Socket) falló: {e}")

# Etapa 3: Intento de Broker en Puerto Alto (Evitar Permission Denied)
# Si no somos root, el 1883 fallará. Probamos el 1888.
def start_broker(comp):
    try:
        import socket
        import threading
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        puerto = 1888 # Puerto alternativo para evitar bloqueos
        comp.log.info(f"Intentando Bind en puerto {puerto}...")
        s.bind(('0.0.0.0', puerto))
        s.listen(1)
        comp.log.info(f"!!! [EXITO] PUERTO {puerto} ABIERTO !!!")
        
        while True:
            c, a = s.accept()
            comp.log.info(f"Conexión desde {a}")
            c.close()
    except Exception as e:
        comp.log.error(f"Error en Hilo Broker: {e}")

try:
    import threading
    t = threading.Thread(target=start_broker, args=(self,), daemon=True)
    t.start()
    self.log.info("Hilo lanzado.")
except Exception as e:
    self.log.error(f"Etapa 3 (Threading) falló: {e}")

self.col_res.insert("Check 005 Finalizado")