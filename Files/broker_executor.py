import socket
import threading
import time

def gateway_total(comp):
    PLC_IP = "192.168.250.160"
    
    def start_bridge():
        try:
            # Forzamos el bindeo a 0.0.0.0 para que escuche en todas las interfaces
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', 9600))
            s.listen(5)
            comp.col_res.insert("🟢 BRIDGE PLC: Escuchando en 9600")
            
            while True:
                client_sock, addr = s.accept()
                def pipe(src, dst):
                    try:
                        while True:
                            d = src.recv(4096)
                            if not d: break
                            dst.sendall(d)
                    except: pass
                    finally:
                        try: src.close()
                        except: pass
                        try: dst.close()
                        except: pass

                try:
                    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_sock.settimeout(3)
                    remote_sock.connect((PLC_IP, 9600))
                    # Hilos bidireccionales
                    threading.Thread(target=pipe, args=(client_sock, remote_sock), daemon=True).start()
                    threading.Thread(target=pipe, args=(remote_sock, client_sock), daemon=True).start()
                except Exception as e:
                    comp.col_res.insert(f"🔴 Error conectando al PLC: {e}")
                    client_sock.close()
        except Exception as e:
            comp.col_res.insert(f"❌ Error crítico en Bridge: {e}")

    # Lanzamos el bridge en un hilo persistente
    t_bridge = threading.Thread(target=start_bridge, daemon=True)
    t_bridge.start()
    comp.col_res.insert("🚀 Hilo de Bridge lanzado")

# Ejecución
gateway_total(self)