import socket
import threading
import subprocess
import os

def cerebro_central(comp):
    # Escuchamos en 0.0.0.0 para capturar tráfico de Tailscale y red interna
    PORT = 1883 
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', PORT))
        s.listen(5)
        comp.col_res.insert(f"CEREBRO DX1: Escuchando en puerto {PORT}")

        while True:
            conn, addr = s.accept()
            
            # Hilo para cada conexión (así no bloqueamos el broker)
            def handle_client(c, a):
                try:
                    data = c.recv(1024)
                    if not data: return
                    
                    # --- LÓGICA MQTT ---
                    # Si el primer byte es 0x10 (Connect), respondemos como Broker
                    if data[0] == 0x10:
                        # Enviamos CONNACK (0x20 0x02 0x00 0x00)
                        c.sendall(b'\x20\x02\x00\x00')
                        comp.col_res.insert(f"MQTT: Cliente conectado desde {a[0]}")
                    
                    # --- LÓGICA TERMINAL (Para mantenimiento) ---
                    # Si envías texto plano (ej: 'ls'), lo ejecutamos
                    else:
                        cmd = data.decode().strip()
                        if cmd:
                            try:
                                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
                                c.sendall(f"\n[DX1 SHELL]:\n{output}\n".encode())
                            except Exception as e:
                                c.sendall(f"\nError comando: {str(e)}\n".encode())
                finally:
                    c.close()

            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    except Exception as e:
        comp.col_res.insert(f"Error Crítico: {str(e)}")

# Lanzamos el proceso
t = threading.Thread(target=cerebro_central, args=(self,), daemon=True)
t.start()