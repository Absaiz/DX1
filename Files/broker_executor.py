# broker_executor.py - VERSIÓN 006 (SILENT BOOT)
import sys
import os

self.log.info("--- [LOG 007] INICIO DE DIAGNÓSTICO ---")

def diagnostic(comp):
    try:
        import socket
        comp.log.info("Libreria 'socket': OK")
        import threading
        comp.log.info("Libreria 'threading': OK")
        import subprocess
        who = subprocess.check_output("whoami", shell=True).decode().strip()
        comp.log.info(f"Contexto de usuario: {who}")
        
        # Intentamos abrir el puerto 1883 de forma controlada
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(('0.0.0.0', 1883))
            s.listen(1)
            comp.log.info("!!! PUERTO 1883 ABIERTO CORRECTAMENTE !!!")
        except Exception as bind_err:
            comp.log.error(f"Error en BIND (1883): {bind_err}")
        finally:
            s.close()
            
    except Exception as e:
        comp.log.error(f"Falla en diagnostico: {e}")

# Ejecutamos el diagnostico en el contexto actual
diagnostic(self)
self.col_res.insert("Check 006: Finalizado")